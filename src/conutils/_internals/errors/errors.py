import json
import os


def ethrow(key: str, error_code: str):

    abs_dir = os.path.dirname(__file__)
    rel_path = "errorcodes.json"
    abs_file_path = os.path.join(abs_dir, rel_path)

    with open(abs_file_path) as json_file:
        errors = json.load(json_file)

    raise ConUtils_error(
        f"\033[1;31m{key}\033[22;39m\n\033[39m{errors[key][error_code]}\033[39m")


class ConUtils_error(Exception):

    def __init__(self, message: str):
        self.message = message.replace("\n", "\n >>> ")

        super().__init__(self.message)