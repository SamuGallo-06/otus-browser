"""Thin wrapper around the gocryptfs command line tool.

Passwords are sent to gocryptfs on stdin (never as arguments or environment
variables). The master key printed by `-init` is discarded and never logged.
"""

import os
import shutil
import subprocess
import tempfile
from pathlib import Path

DEFAULT_TIMEOUT = 30  # seconds

# Exit codes documented in `man gocryptfs` (EXIT CODES)
_EXIT_CIPHERDIR_NOT_EMPTY = 6
_EXIT_MOUNTPOINT_NOT_EMPTY = 10
_EXIT_WRONG_PASSWORD = 12
_EXIT_EMPTY_PASSWORD = 22
_EXIT_CONFIG_READ = 23
_EXIT_CONFIG_WRITE = 24

class GocryptfsError(Exception):
    """Base class for every error raised by this module."""


class GocryptfsNotInstalledError(GocryptfsError):
    """Raised when gocryptfs is not installed on the system."""


class MissingDependenciesError(GocryptfsError):
    """Raised when fusermount/fusermount3 or the FUSE device are not available."""


class InvalidPasswordError(GocryptfsError, ValueError):
    """Raised when the password is empty or contains characters that cannot be sent on stdin."""


class InvalidDirectoryError(GocryptfsError):
    """Raised when a directory is missing, not a directory, or not accessible."""


class DirectoryNotEmptyError(GocryptfsError):
    """Raised when a directory that must be empty is not."""


class ConfigFileError(GocryptfsError):
    """Raised when the config file already exists, is missing, or cannot be read/written."""


class WrongPasswordError(GocryptfsError):
    """Raised when gocryptfs rejects the password."""


class MountError(GocryptfsError):
    """Raised when a directory is already mounted or cannot be unmounted."""


class CommandError(GocryptfsError):
    """Raised when a command fails for a reason that has no more specific error."""

    def __init__(self, message: str, returncode: int | None = None, stderr: str = ""):
        super().__init__(message)
        self.returncode = returncode
        self.stderr = stderr


class PyGocryptfs:

    def __init__(self):
        self.gocryptfs = shutil.which("gocryptfs")
        if self.gocryptfs is None:
            raise GocryptfsNotInstalledError("gocryptfs is not installed on this system")

        self.fusermount = shutil.which("fusermount3") or shutil.which("fusermount")
        if self.fusermount is None:
            raise MissingDependenciesError("fusermount or fusermount3 is not installed on this system")

        if not os.access("/dev/fuse", os.R_OK | os.W_OK):
            raise MissingDependenciesError("/dev/fuse is not accessible (is FUSE available?)")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def version(self) -> str:
        """Return the output of `gocryptfs -version`."""
        try:
            result = subprocess.run(
                [self.gocryptfs, "-version"],                               #type: ignore because self.gocryptfs is guaranteed to be a string if we reach this point.
                capture_output=True,                                        # If was None, it would have raised GocryptfsNotInstalledError in __init__
                text=True, 
                timeout=DEFAULT_TIMEOUT,
            )                                                               
        except (subprocess.TimeoutExpired, OSError) as e:
            raise CommandError(f"Cannot run gocryptfs -version: {e}") from e
        return (result.stdout or result.stderr).strip()

    def setup(self, p_conf: Path | str, p_password: str, p_dir: Path | str) -> None:
        """Initialize an encrypted directory.

        p_conf: path of the config file to create (must not exist yet).
        p_dir:  directory that will hold the encrypted files; it is created if
                missing, and must be empty if it already exists.
        """
        conf = Path(p_conf).expanduser()
        directory = Path(p_dir).expanduser()
        self._check_password(p_password)

        if conf.exists() or conf.is_symlink():
            raise ConfigFileError(f"Config file already exists: {conf}")
        dir_existed = directory.exists()
        if dir_existed:
            self._require_empty_dir(directory)

        try:
            conf.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
            if not dir_existed:
                directory.mkdir(mode=0o700, parents=True)
        except OSError as e:
            raise InvalidDirectoryError(f"Cannot create directories: {e}") from e

        returncode, stderr = self._run(
            [self.gocryptfs, "-q", "-nosyslog", "-init", "-config", str(conf), str(directory)], #type: ignore
            password=p_password,
        )
        if returncode != 0:
            conf.unlink(missing_ok=True)  # remove a partially written config
            if not dir_existed:
                try:
                    directory.rmdir()
                except OSError:
                    pass
            raise self._error(returncode, stderr)

    def mount(self, p_conf: Path | str, p_dir: Path | str, p_mountpoint: Path | str, p_password: str) -> None:
        """Mount an encrypted directory on p_mountpoint (created if missing, must be empty)."""
        conf = Path(p_conf).expanduser()
        directory = Path(p_dir).expanduser()
        mountpoint = Path(p_mountpoint).expanduser()
        self._check_password(p_password)

        if not conf.is_file():
            raise ConfigFileError(f"Config file not found: {conf}")
        if not directory.is_dir():
            raise InvalidDirectoryError(f"Encrypted directory not found: {directory}")
        if self.is_mounted(mountpoint):
            raise MountError(f"Already mounted (or stale mount, see unmount(lazy=True)): {mountpoint}")

        mountpoint_existed = mountpoint.exists()
        if mountpoint_existed:
            self._require_empty_dir(mountpoint)
        else:
            try:
                mountpoint.mkdir(mode=0o700, parents=True)
            except OSError as e:
                raise InvalidDirectoryError(f"Cannot create mountpoint: {e}") from e

        # gocryptfs daemonizes: it returns 0 only once the filesystem is ready
        returncode, stderr = self._run(
            [self.gocryptfs, "-q", "-nosyslog", "-config", str(conf), str(directory), str(mountpoint)], #type: ignore
            password=p_password,
        )
        if returncode != 0:
            if not mountpoint_existed:
                try:
                    mountpoint.rmdir()
                except OSError:
                    pass
            raise self._error(returncode, stderr)

    def unmount(self, p_mountpoint: Path | str, lazy: bool = False) -> None:
        """Unmount a mountpoint. Use lazy=True to clean up a stale mount after a crash."""
        mountpoint = Path(p_mountpoint).expanduser()
        args = [self.fusermount, "-u"]
        if lazy:
            args.append("-z")
        args.append(str(mountpoint))

        returncode, stderr = self._run(args)
        if returncode != 0:
            raise MountError(f"Cannot unmount {mountpoint}: {stderr or 'unknown error'}")

    def is_mounted(self, p_mountpoint: Path | str) -> bool:
        """True if the path is a mountpoint. A stale FUSE mount (crashed daemon) counts as mounted."""
        try:
            return os.path.ismount(Path(p_mountpoint).expanduser())
        except OSError:
            return True

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------
    @staticmethod
    def _check_password(password: str) -> None:
        if not password:
            raise InvalidPasswordError("Password must not be empty")
        if any(c in password for c in ("\n", "\r", "\0")):
            raise InvalidPasswordError("Password must not contain line breaks or NUL characters")

    @staticmethod
    def _require_empty_dir(path: Path) -> None:
        if not path.is_dir():
            raise InvalidDirectoryError(f"Not a directory: {path}")
        try:
            if any(path.iterdir()):
                raise DirectoryNotEmptyError(f"Directory is not empty: {path}")
        except OSError as e:
            raise InvalidDirectoryError(f"Cannot read directory {path}: {e}") from e

    @staticmethod
    def _run(args: list[str], password: str | None = None, timeout: int = DEFAULT_TIMEOUT) -> tuple[int, str]:
        """Run a command; return (exit code, stderr). stdout is always discarded.

        stderr goes to a temporary file instead of a pipe, because the gocryptfs
        daemon would keep a pipe open and make subprocess.run wait for it.
        The password (if any) is sent as a single line on stdin: when stdin is
        not a terminal, gocryptfs does not ask for confirmation.
        """
        kwargs = {}
        if password is not None:
            kwargs["input"] = (password + "\n").encode("utf-8")
        else:
            kwargs["stdin"] = subprocess.DEVNULL

        with tempfile.TemporaryFile() as err:
            try:
                proc = subprocess.run(args, stdout=subprocess.DEVNULL, stderr=err, timeout=timeout, **kwargs)
            except subprocess.TimeoutExpired as e:
                raise CommandError(f"{Path(args[0]).name} timed out after {timeout} s") from e
            except OSError as e:
                raise CommandError(f"Cannot execute {args[0]}: {e}") from e
            err.seek(0)
            stderr = err.read().decode("utf-8", errors="replace").strip()
        return proc.returncode, stderr

    @staticmethod
    def _error(returncode: int, stderr: str) -> GocryptfsError:
        """Translate a gocryptfs exit code into the most specific exception."""
        message = stderr or "no error message"
        if returncode == _EXIT_WRONG_PASSWORD:
            return WrongPasswordError("Wrong password")
        if returncode in (_EXIT_CIPHERDIR_NOT_EMPTY, _EXIT_MOUNTPOINT_NOT_EMPTY):
            return DirectoryNotEmptyError(message)
        if returncode == _EXIT_EMPTY_PASSWORD:
            return InvalidPasswordError(message)
        if returncode in (_EXIT_CONFIG_READ, _EXIT_CONFIG_WRITE):
            return ConfigFileError(message)
        return CommandError(f"gocryptfs failed (exit code {returncode}): {message}", returncode, stderr)