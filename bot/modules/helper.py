import logging
import json
import pathlib

LOGGER = logging.getLogger("bot")

def write_to_json_list(file_name: str, data: dict) -> None:
    file_path = pathlib.Path(file_name)
    
    if file_path.exists():
        with open(file_path, "r+", encoding="utf-8") as jsonf:
            json_data = json.load(jsonf)
    else:
        logging.info(f"{file_name} doesn't exist, new one will be created.")
        json_data = []
    
    json_data.append(data)

    with open(file_path, "w", encoding="utf-8") as jsonf:
        json.dump(json_data, jsonf, indent=4)

    logging.info(f"[JSON] Successfully wrote to {file_name}.")    



def read_json_list(file_name) -> list[dict] | None:
    file_path = pathlib.Path(file_name)

    if not file_path.exists():
        logging.error(f"{file_name} doesn't exist, yet we tried to we read from it.")
        return

    with open(file_path, "r+", encoding="utf-8") as jsonf:
        json_data = json.load(jsonf)
        return json_data