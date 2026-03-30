import os
import unicodedata

BASE_PATH = "static/images/teams"


def normalize_name(name: str) -> str:
    name = name.lower()
    name = unicodedata.normalize("NFKD", name)
    name = name.encode("ascii", "ignore").decode("ascii")
    name = name.replace(".", "")
    name = name.replace("-", " ")
    name = name.replace("  ", " ")
    return name.strip()


def find_logo(team_name: str):
    normalized = normalize_name(team_name)

    for root, dirs, files in os.walk(BASE_PATH):
        for file in files:
            filename = normalize_name(file.replace(".png", ""))

            if filename == normalized:
                path = os.path.join(root, file)
                return "/" + path.replace("\\", "/")

    return "/static/images/default.png"