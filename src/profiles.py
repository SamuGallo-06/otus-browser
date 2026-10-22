from xml.etree import ElementTree as ET
import secrets, shutil, bcrypt

from settings import PROFILES_DIR, PROFILES_XML_PATH

def get_profiles() -> dict:
    tree = ET.parse(PROFILES_XML_PATH)
    root = tree.getroot()

    profiles = {}

    for child in root.findall("Profile"):
        for elem in child:
            if(elem.tag == "uid"):
                uid = elem.text
                profiles[uid] = {}
                profiles[uid][elem.tag] = elem.text
            else:
                profiles[uid][elem.tag] = elem.text
                    
    return profiles
    
def get_profile_by_name(profile_name: str) -> dict | None:
    profiles = get_profiles()
    for profile in profiles.values():
        if profile["name"] == profile_name:
            return profile
    return None

def createProfile(profile_name: str, password: str | None = None) -> str:
    PROFILES_DIR.mkdir(parents=True, exist_ok=True, mode=0o700)

    while True:
        uid = secrets.token_hex(8)
        profile_path = PROFILES_DIR / uid
        try:
            profile_path.mkdir(mode=0o700)       # niente exist_ok
            break
        except FileExistsError:
            continue

    try:
        auth = hash_password(password) if password else None
        add_profile_to_registry(uid, profile_name, auth)
    except Exception:
        shutil.rmtree(profile_path, ignore_errors=True)
        raise

    return uid

def hash_password(password: str) -> str:
    s = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), s)
    return hashed.decode()

def check_password(profile_name:str, entered_pw: str):
    profile = get_profile_by_name(profile_name)
    if profile is not None:
        pw = profile.get("auth", None)
        if pw is not None and pw != "None":
            h = pw.encode("utf-8")
            return bcrypt.checkpw(entered_pw.encode("utf-8"), h)
    return False

def add_profile_to_registry(uid: str, name: str, auth: str | None):
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