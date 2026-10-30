import xml.etree.ElementTree as ET
import tarfile
from shutil import copy2
from dataclasses import dataclass, field
from pathlib import Path
from settings import *
from zipfile import ZipFile
import tempfile

from PySide6.QtCore import QObject, Signal

## Base dir of a package is the manifest dir
## install dir is

@dataclass
class OtusPackage:
    id:str
    type: str
    name:str
    version:str
    meta: dict[str, str]
    authors: list[str]
    description: str
    license: str
    files: list[dict[str, str]] # {"source": src, "dest": dest}
    directories: list[dict[str, str]] # {"source": tar, "dest": directory}

class InvalidManifest(Exception):
    "Raised when a package manifest is invalid or cannot be parsed."
    pass

class CorruptedPackage(Exception):
    "Raised when a package is corrupted or cannot be installed."
    pass

class InstallError(Exception):
    "Raised when a package cannot be installed."
    pass

class PackageNotFound(Exception):
    "Raised when a package is not found in the registry."
    pass

class PackageManager(QObject):
    
    progressUpdated = Signal(str, int) #format: (message, percentage)
    
    def parse_manifest(self, manifest_path):
        tree = ET.parse(manifest_path)
        root = tree.getroot()
        
        if root.tag != "OtusPackageManifest":
            raise InvalidManifest("This is not an Otus Package Manifest")
        
        pkg_schema_version = root.attrib.get("schemaVersion")
        pkg_type = root.attrib.get("type")
        
        if pkg_schema_version is None or pkg_type is None:
            raise InvalidManifest("Package Manifest must contain both `schemaVersion` and `type` attributes")
        
        manifest = {}
        meta = {}
        authors = []
        files = []
        directories = []
        
        for child in root:
            if child.tag in {"Files", "Requires", "Requirements"}:
                continue
            if child.tag == "Authors":
                for author in child:
                    if author.text is not None:
                        authors.append(author.text)
                    else:
                        raise InvalidManifest("Missing author name in manifest")
                manifest[child.tag] = authors
            elif child.tag == "Meta":
                for key, value in child.attrib.items():
                    meta[key] = value
            else:
                if child.text is not None:
                    manifest[child.tag] = child.text
                else:
                    raise InvalidManifest(f"Missing value for {child.tag} in manifest")
        
        element = root.find("Files")
                
        if element is not None:
            for entry in element:
                source = entry.attrib.get("src")
                dest = entry.attrib.get("dest")
                sha256 = entry.attrib.get("sha256")

                if source is None or dest is None:
                    raise InvalidManifest(
                        f"Missing src or dest attributes for {entry.tag}"
                    )
                if sha256 is None:
                    raise InvalidManifest(f"Missing sha256 attribute for {entry.tag}")

                if entry.tag == "File":
                    if sha256 is None:
                        raise InvalidManifest("Missing sha256 attribute for File")
                    files.append({
                        "source": source,
                        "destination": dest,
                        "sha256": sha256,
                    })
                elif entry.tag == "Directory":
                    directories.append({
                        "source": source,
                        "destination": dest,
                        "sha256": sha256,
                    })
                else:
                    raise InvalidManifest(f"Unknown Files entry: {entry.tag}")
        
                
        pkg = OtusPackage(
            #type: ignore beacause we are sure it exists in the manifest, otherwise the manifest is invalid and we raised an exception. 
            # This check is done above, in the first for loop.
            id=manifest.get("Id"),                      #type: ignore beacause we are sure it exists in the manifest, otherwise the manifest is invalid and we raised an exception. 
            type=pkg_type,
            name = manifest.get("Name"),                #type: ignore
            meta=meta,
            version = manifest.get("Version"),          #type: ignore
            description = manifest.get("Description"),  #type: ignore
            authors = authors,
            license = manifest.get("License"),          #type: ignore
            files = files,
            directories = directories,
        )
        
        return pkg

    def install_package(self, pkg_path: str) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)

            #1 Extracting .otuspkg file
            try:
                with ZipFile(pkg_path, "r") as pkg_file:
                    pkg_file.extractall(temp_dir_path)
            except Exception as e:
                raise InstallError(
                    f"Impossibile estrarre l'archivio zip {pkg_path}: {e}"
                )

            manifest_path = temp_dir_path / "manifest.otus"

            if not manifest_path.exists():
                raise InstallError(f"Manifest non trovato in {pkg_path}")

            #2 Reading manifest and parsing package information
            self.progressUpdated.emit("Reading manifest...", 0)
            pkg = self.parse_manifest(manifest_path)
            package_source_dir = temp_dir_path

            #3 Calculating target directory based on package type
            if pkg.type == "language":
                pkg_dir = Path(LANGUAGES_PATH) / pkg.meta["lang_code"]
            elif pkg.type == "theme":
                pkg_dir = Path(THEMES_PATH) / pkg.id
            elif pkg.type == "homepage":
                pkg_dir = Path(HOME_PAGES_PATH) / pkg.id
            else:
                pkg_dir = Path(PACKAGES_PATH) / pkg.id

            #4 Computing total operations for progress tracking
            count = len(pkg.files) + len(pkg.directories)
            total_ops = count + 2
            completed_ops = 1  # manifest già letto

            def emit_progress(message: str) -> None:
                percentage = int((completed_ops / total_ops) * 100)
                self.progressUpdated.emit(message, percentage)

            #5 Copying files to the target directory
            for file in pkg.files:
                source = package_source_dir / file["source"]
                target = pkg_dir / file["destination"]
                target.parent.mkdir(parents=True, exist_ok=True)
                try:
                    copy2(source, target)
                except Exception as e:
                    raise InstallError(
                        f"Failed to copy file {source} to {target}: {e}"
                    )
                completed_ops += 1
                emit_progress(
                    f"Installed {file['source']} ({completed_ops - 1}/{count})"
                )

            #6 Extracting directories from tar archives to the target directory
            for directory in pkg.directories:
                source = package_source_dir / directory["source"]
                target = pkg_dir / directory["destination"]
                target.mkdir(parents=True, exist_ok=True)
                try:
                    self._extract_tar(source, target)
                except Exception as e:
                    raise InstallError(
                        f"Failed to extract directory {source} to {target}: {e}"
                    )
                completed_ops += 1
                emit_progress(
                    f"Extracted {directory['source']} ({completed_ops - 1}/{count})"
                )
            
            # Here, the temporary directory will be automatically cleaned up .

        #7 Finalizing installation and updating the package registry
        self.progressUpdated.emit("Finalizing package...", 99)
        self.update_registry(pkg, str(pkg_dir))
        completed_ops += 1
        self.progressUpdated.emit("Package installed", 100)

    def _extract_tar(self, archive_path: Path, destination: Path) -> None:
        with tarfile.open(archive_path, "r:*") as archive:
            members = archive.getmembers()
            destination_root = destination.resolve()

            for member in members:
                member_path = (destination / member.name).resolve()
                if not member_path.is_relative_to(destination_root):
                    raise InvalidManifest(
                        f"Unsafe path in directory archive: {member.name}"
                    )
                if member.issym() or member.islnk():
                    raise InvalidManifest(
                        f"Links are not allowed in directory archive: {member.name}"
                    )

            archive.extractall(destination, members=members)
            
    def update_registry(self, pkg: OtusPackage, dir:str) -> None:
        registry_path = PACKAGE_REGISTRY

        if not registry_path.exists():
            root = ET.Element("OtusPackageRegistry")
            tree = ET.ElementTree(root)
            tree.write(registry_path, encoding="utf-8", xml_declaration=True)

        tree = ET.parse(registry_path)
        root = tree.getroot()

        package_elem = ET.Element("Package", attrib={"type": pkg.type, "id": pkg.id})
        for key, value in pkg.meta.items():
            package_elem.set(key, value)
        package_elem.set("version", pkg.version)
        package_elem.set("name", pkg.name)
        package_elem.set("description", pkg.description)
        authors_elem = ET.SubElement(package_elem, "Authors")
        for author in pkg.authors:
            author_elem = ET.SubElement(authors_elem, "Author")
            author_elem.text = author
        package_elem.set("license", pkg.license)
        directory_elem = ET.SubElement(package_elem, "directory")
        directory_elem.text = dir

        root.append(package_elem)
        tree.write(registry_path, encoding="utf-8", xml_declaration=True)
        
    def uninstall_package(self, pkg_id: str) -> None:
        registry_path = PACKAGE_REGISTRY
        
        if not registry_path.exists():
            raise PackageNotFound("Package registry does not exist.")

        tree = ET.parse(registry_path)
        root = tree.getroot()

        package_elem = root.find(f"Package[@id='{pkg_id}']")
        if package_elem is None:
            raise PackageNotFound(f"Package with id '{pkg_id}' not found in registry.")

        directory_elem = package_elem.find("directory")
        pkg_dir = (
            Path(directory_elem.text)
            if directory_elem is not None and directory_elem.text
            else None
        )

        if pkg_dir is not None and pkg_dir.exists():
            self.rm_rf(pkg_dir)

        root.remove(package_elem)
        tree.write(registry_path, encoding="utf-8", xml_declaration=True)
        
    def rm_rf(self, path: Path) -> None:
        """Recursively remove a directory and its contents."""
        if path.is_dir():
            for item in path.iterdir():
                if item.is_dir():
                    self.rm_rf(item)
                else:
                    item.unlink()
            path.rmdir()
        elif path.is_file():
            path.unlink()
    