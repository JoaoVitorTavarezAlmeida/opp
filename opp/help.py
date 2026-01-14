from importlib.resources import files
import json

def load_help() -> dict:
    path = files("opp").joinpath("help_opp.json")
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
