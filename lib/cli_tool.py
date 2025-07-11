import argparse
import pickle
import os
from lib.models import Task, User

DATA_FILE = "users.pkl"

def load_users():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "rb") as f:
            return pickle.load(f)
    return {}

def save_users(users):
    with open(DATA_FILE, "wb") as f:
        pickle.dump(users, f)

def add_task(args):
    users = load_users()
    user = users.get(args.user)
    if not user:
        user = User(args.user)
        users[args.user] = user
    task = Task(args.title)
    user.add_task(task)
    save_users(users)

def complete_task(args):
    users = load_users()
    user = users.get(args.user)
    if user:
        for task in user.tasks:
            if task.title == args.title:
                task.complete()
                save_users(users)
                return
        print("❌ Task not found.")
    else:
        print("❌ User not found.")

def main():
    parser = argparse.ArgumentParser(description="Task Manager CLI")
    subparsers = parser.add_subparsers()

    add_parser = subparsers.add_parser("add-task", help="Add a new task")
    add_parser.add_argument("user")
    add_parser.add_argument("title")
    add_parser.set_defaults(func=add_task)

    complete_parser = subparsers.add_parser("complete-task", help="Complete a task")
    complete_parser.add_argument("user")
    complete_parser.add_argument("title")
    complete_parser.set_defaults(func=complete_task)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
