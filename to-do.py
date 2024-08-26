import argparse
import os

# -a or --add -> add a task
# -l or --list -> list today's tasks
# -lw or --list-weekly -> list this week's tasks
# -c or --complete -> complete a task
# -r or --remove -> remove a task

def create_parser():
    parser = argparse.ArgumentParser(description="Michelle's To-Do CLI app")
    parser.add_argument("-a", "--add", metavar="", help="Add a new task")
    parser.add_argument("-l", "--list", metavar="", help="List today's task")
    parser.add_argument("-lw", "--list-weekly", metavar="", help="List this week's tasks")
    parser.add_argument("-c", "--complete", metavar="", help="Complete a task")
    parser.add_argument("-r", "--remove", metavar="", help="Remove a task")

    return parser
