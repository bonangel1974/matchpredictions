import os

BASE_PATH = "static/images/teams"
DEFAULT_IMAGE = "/static/images/default.png"


def normalize_team_name(name: str) -> str:
    if not name:
        return ""

    value = name.strip().lower()

    replacements = {
        "ä": "ae",
        "ö": "oe",
        "ü": "ue",
        "é": "e",
        "è": "e",
        "à": "a",
        "ó": "o",
        "í": "i",
        "á": "a",
        "ñ": "n",
        ".": "",
        ",": "",
        "'": "",
        '"': "",
        "&": "and",
        "/": "-",
        "(": "",
        ")": "",
    }

    for old, new in replacements.items():
        value = value.replace(old, new)

    value = value.replace(" - ", "-")
    value = value.replace(" ", "-")
    value = value.replace("--", "-")
    return value.strip("-")


def build_possible_names(team_name: str):
    base = normalize_team_name(team_name)

    variants = {
        base,
        base.replace("fc-", ""),
        base.replace("1-fc-", ""),
        base.replace("tsg-1899-", "tsg-"),
        base.replace("vfb-", "vfb-"),
        base.replace("sv-", ""),
        base.replace("sc-", ""),
    }

    return list(variants)


def find_logo(team_name: str):
    if not os.path.exists(BASE_PATH):
        return DEFAULT_IMAGE

    possible_names = build_possible_names(team_name)

    for root, dirs, files in os.walk(BASE_PATH):
        for file_name in files:
            lower = file_name.lower()

            if not (lower.endswith(".png") or lower.endswith(".jpg") or lower.endswith(".jpeg") or lower.endswith(".webp")):
                continue

            file_base = os.path.splitext(lower)[0]
            normalized_file = normalize_team_name(file_base)

            if normalized_file in possible_names:
                full_path = os.path.join(root, file_name)
                return "/" + full_path.replace("\\", "/")

    return DEFAULT_IMAGE