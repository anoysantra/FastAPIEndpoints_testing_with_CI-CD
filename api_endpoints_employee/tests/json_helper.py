import json
from pathlib import Path
from typing import Any

"""
def load_json_data(file_name: str = "creds_data.json") -> dict[str, Any]:
	file_path = Path(__file__).parent / file_name

	with file_path.open(encoding="utf-8") as json_file:
		return json.load(json_file)
"""

def load_json_data(file_name: str) -> dict[str, Any]:
    # Dynamically resolve the path relative to the current script's folder
    file_path = Path(__file__).parent / file_name

    with file_path.open(encoding="utf-8") as json_file:
        return json.load(json_file)


'''
data.json = static test input
database setup = recreate/reset test employees
tests = read IDs from data.json
'''