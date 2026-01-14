#!/usr/bin/env python3

import sys
from opp.service import CommandService
from opp.help import load_help, print_help


service = CommandService()


def main():
    args = sys.argv[1:]

    if not args:
        show_help()
        return

    cmd = args[0]

    handlers = {
        "add": handle_add,
        "get": handle_get,
        "list": handle_list,
        "ls": handle_list,
        "id": handle_id,
        "rm": handle_remove,
        "remove": handle_remove,
        "ex": handle_execute,
        "execute": handle_execute,
        "upd": handle_update,
        "update": handle_update,
        "help": handle_help,
        "h": handle_help,
    }

    handler = handlers.get(cmd)

    if not handler:
        print("Invalid command or arguments.")
        return

    handler(args)


# ===== handlers =====

def show_help():
    data = load_help()
    print_help(data)


def handle_help(args):
    show_help()


def handle_add(args):
    if len(args) != 4:
        print("Usage: opp add <alias> <name> <command>")
        return

    alias, name, path = args[1:]
    cmd_id = service.register(alias, name, path)
    print(f"Command added with ID: {cmd_id}")


def handle_get(args):
    if len(args) != 2:
        print("Usage: opp get <alias>")
        return

    cmd = service.find(args[1])
    print_command(cmd)


def handle_list(args):
    for cmd in service.list():
        print_command(cmd)


def handle_id(args):
    try:
        cmd_id = int(args[1])
    except (IndexError, ValueError):
        print("Invalid ID.")
        return

    cmd = service.find_by_id(cmd_id)
    print_command(cmd)


def handle_remove(args):
    if len(args) != 2:
        print("Usage: opp rm <alias>")
        return

    if service.remove(args[1]):
        print("Command removed.")
    else:
        print("Command not found.")


def handle_execute(args):
    if len(args) != 2:
        print("Usage: opp ex <alias>")
        return

    if service.execute(args[1]):
        print("Command executed.")
    else:
        print("Command not found.")


def handle_update(args):
    if len(args) != 4:
        print("Usage: opp update <alias> <name> <command>")
        return

    if service.update(*args[1:]):
        print("Command updated.")
    else:
        print("Command not found.")


def print_command(cmd):
    if not cmd:
        print("Command not found.")
        return

    print(f"ID: {cmd.id}, Alias: {cmd.alias}, Name: {cmd.name}, Path: {cmd.path}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
