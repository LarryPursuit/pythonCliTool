# cli_tool.py

import argparse

# Support both `python -m lib.cli_tool` (package import) and
# `python lib/cli_tool.py` (script run from the lib directory's path).
try:
    from lib.models import Task, User
except ModuleNotFoundError:
    from models import Task, User

# Global dictionary to store users and their tasks
users: dict[str, User] = {}


def _clean(value: str, field: str) -> str:
    """Strip whitespace and reject empty values with a helpful message."""
    cleaned = value.strip()
    if not cleaned:
        raise argparse.ArgumentTypeError(f"{field} cannot be empty.")
    return cleaned


def add_task(args: argparse.Namespace) -> None:
    """Create the user if needed, then add a new task to their list."""
    user = users.get(args.user)
    if user is None:
        user = User(args.user)
        users[args.user] = user
    user.add_task(Task(args.title))


def complete_task(args: argparse.Namespace) -> None:
    """Mark a user's task as complete, reporting if the user or task is missing."""
    user = users.get(args.user)
    if user is None:
        print("❌ User not found.")
        return

    task = user.get_task_by_title(args.title)
    if task is None:
        print("❌ Task not found.")
        return

    task.complete()


# CLI entry point
def main() -> None:
    parser = argparse.ArgumentParser(description="Task Manager CLI")
    subparsers = parser.add_subparsers()

    user_arg = {"type": lambda v: _clean(v, "User name"), "help": "Name of the user"}
    title_arg = {"type": lambda v: _clean(v, "Task title"), "help": "Title of the task"}

    # Subparser for adding tasks
    add_parser = subparsers.add_parser("add-task", help="Add a task for a user")
    add_parser.add_argument("user", **user_arg)
    add_parser.add_argument("title", **title_arg)
    add_parser.set_defaults(func=add_task)

    # Subparser for completing tasks
    complete_parser = subparsers.add_parser("complete-task", help="Complete a user's task")
    complete_parser.add_argument("user", **user_arg)
    complete_parser.add_argument("title", **title_arg)
    complete_parser.set_defaults(func=complete_task)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
