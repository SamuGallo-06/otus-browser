import os
from xml.etree import ElementTree as ET
import secrets, shutil, bcrypt
from pathlib import Path
import logging
from dataclasses import dataclass

from settings import *
from pygocryptfs import *

log = logging.getLogger(__name__)


def _ensure_profiles_registry() -> None:
    if PROFILES_XML_PATH.exists():
        return

    PROFILES_XML_PATH.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    ET.ElementTree(ET.Element("Profiles")).write(PROFILES_XML_PATH)


@dataclass
class OtusProfile:
    """Runtime representation of a profile registry entry."""

    uid: str
    name: str
    hidden: bool = False
    auth: str | None = None
    type: str | None = None
    deletable: bool = False
    protected: bool = False
    mountpoint: Path | None = None
    
    ## Properties
    ## - uid:          Unique identifier for the profile
    ## - name:         Name of the profile
    ## - hidden:       Whether the profile is hidden
    ## - auth:         Authentication information for the profile
    ## - type:         Type of the profile. It can be "Normal", "Nocturnal", or "Guest". Normal profiles are standard profiles, Nocturnal profiles are private or incognito, and Guest is a special profile for temporary use.
    ## - deletable:    Whether the profile is deletable through the GUI. 
    ## - protected:    Whether the profile is protected
    ## - mountpoint:   Path where the encrypted profile is mounted in case of encrypted profiles. It is None for unencrypted profiles.

    @property
    def encrypted(self) -> bool:
        return bool(self.auth)

    @property
    def cipher_path(self) -> Path:
        return PROFILES_DIR / self.uid

    @property
    def mount_path(self) -> Path:
        return Path(str(MOUNT_POINT).format(uid=self.uid))

    @property
    def storage_path(self) -> Path:
        if not self.encrypted:
            return self.cipher_path
        if self.mountpoint is None:
            raise RuntimeError(f"Encrypted profile is not mounted: {self.uid}")
        return self.mountpoint


def _profile_from_xml(element: ET.Element) -> OtusProfile | None:
    uid = element.findtext("uid")
    name = element.findtext("name")
    if not uid or not name:
        return None

    return OtusProfile(
        uid=uid,
        name=name,
        hidden=(element.findtext("hidden") or "").strip().lower() == "true",
        auth=element.findtext("auth") or None,
        type=element.findtext("type"),
        deletable=(element.findtext("deletable") or "").strip().lower() == "true",
        protected=(element.findtext("protected") or "").strip().lower() == "true",
    )


def get_profiles() -> dict[str, OtusProfile]:
    """"""
    _ensure_profiles_registry()
    tree = ET.parse(PROFILES_XML_PATH)
    root = tree.getroot()

    profiles: dict[str, OtusProfile] = {}

    for child in root.findall("Profile"):
        profile = _profile_from_xml(child)
        if profile is None:
            continue
        profiles[profile.uid] = profile
                    
    return profiles
    
def get_profile_by_name(profile_name: str) -> OtusProfile | None:
    profiles = get_profiles()
    for profile in profiles.values():
        if profile.name == profile_name:
            return profile
    return None

def get_profile_by_id(profile_id: str) -> OtusProfile | None:
    return get_profiles().get(profile_id)

def createProfile(profile_name: str, password: str | None = None) -> str:
    PROFILES_DIR.mkdir(parents=True, exist_ok=True, mode=0o700)

    while True:
        uid = secrets.token_hex(8)
        profile_path = PROFILES_DIR / uid
        try:
            profile_path.mkdir(mode=0o700) 
            break
        except FileExistsError:
            continue
    
    auth = hash_password(password) if password else None
    try:
        add_profile_to_registry(uid, profile_name, auth)
    except Exception:
        log.error("An error occurred while adding the profile to the registry. Cleaning up...")
        shutil.rmtree(profile_path, ignore_errors=True)
        raise

    if password:
        log.info("Setting profile password...")
        log.info("Encrypting Profile...")
        try:
            gfs = PyGocryptfs()
            conf = KEYS_DIR / f"{uid}.conf"
            cipher = PROFILES_DIR / uid     
            gfs.setup(conf, password, cipher)
        except GocryptfsError:
            log.error("An error occurred while encrypting the profile. Cleaning up...")
            shutil.rmtree(profile_path, ignore_errors=True)
            raise

    return uid

def hash_password(password: str) -> str:
    s = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), s)
    return hashed.decode()

def check_password(profile: OtusProfile, entered_pw: str) -> bool:
    if profile is not None:
        pw = profile.auth
        if pw:
            h = pw.encode("utf-8")
            return bcrypt.checkpw(entered_pw.encode("utf-8"), h)
    return False

def add_profile_to_registry(uid: str, name: str, auth: str | None):
    _ensure_profiles_registry()
    tree = ET.parse(PROFILES_XML_PATH)
    root = tree.getroot()
    
    profile_elem = ET.Element("Profile")
    uid_elem = ET.SubElement(profile_elem, "uid")
    uid_elem.text = uid
    name_elem = ET.SubElement(profile_elem, "name")
    name_elem.text = name
    hidden_elem = ET.SubElement(profile_elem, "hidden")
    hidden_elem.text = "false"
    auth_elem = ET.SubElement(profile_elem, "auth")
    auth_elem.text = auth if auth else ""
    type_elem = ET.SubElement(profile_elem, "type")
    type_elem.text = "Normal"
    deletable_elem = ET.SubElement(profile_elem, "deletable")
    deletable_elem.text = "True"
    root.append(profile_elem)
    tree.write(PROFILES_XML_PATH)