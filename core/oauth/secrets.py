import json


def load_file(secrets_file: str) -> dict[str:str]:
    return json.loads(secrets_file.read_text())
