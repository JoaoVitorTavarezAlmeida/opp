from importlib.resources import files
import json


_HELP_PACKAGE = "opp.help"
_HELP_FILE = "help_opp.json"


def load_help() -> dict:
    path = files(_HELP_PACKAGE).joinpath(_HELP_FILE)

    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def print_help(data: dict) -> None:
    print(data.get("title", ""))
    print()
    print(data.get("introduction", ""))
    print()

    for section in data.get("sections", []):
        print(section.get("heading", ""))
        content = section.get("content")

        if isinstance(content, list):
            for item in content:
                print(f"  {item['command']:<30} {item['description']}")
        else:
            print(f"  {content}")

        print()
