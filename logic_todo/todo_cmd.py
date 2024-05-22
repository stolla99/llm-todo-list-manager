import re
import shlex
import subprocess
import time
from string import Template

# pre made commands
PREFIX = ["cmd", "/c"]

# patterns
PATTERN_POSITION = [
    r'\s(.*)\s\|'
]
PATTERN_TITLE = [
    r'\|\s(.*)\s⌛',
    r'\|\s(.*)\s★',
    r'\|\s(.*)\s#',
    r'\|\s(.*)\s\r',
    r'\|\s(.*)\r'
]

PATTERN_DEADLINE = [
    r'⌛(.*)\s★',
    r'⌛(.*)\s#',
    r'⌛(.*)\s\r',
    r'⌛(.*)\r'
]
PATTERN_PRIORITY = [
    r'★(.*)\s#',
    r'★(.*)\s\r',
    r'★(.*)\r'
]
PATTERN_CONTEXT = [
    r'#(.*)\s\r',
    r'#(.*)\r'
]

FUTURE_PATTERN_STARTS = [
    r'\[starts: (.*)\]'
]
FUTURE_PATTERN_TITLE = [
    r'\|\s(.*)\s⌛',
    r'\|\s(.*)\s★',
    r'\|\s(.*)\s#',
    r'\|\s(.*)\s\['
]
FUTURE_PATTERN_CONTEXT = [
    r'#(.*)\s\['
]
FUTURE_PATTERN_DEADLINE = [
    r'⌛(.*)\s★',
    r'⌛(.*)\s#',
    r'⌛(.*)\s\['
]
FUTURE_PATTERN_PRIORITY = [
    r'★(.*)\s#',
    r'★(.*)\s\['
]


def exec_command(command):
    """
    This function executes a given command in the shell and returns the output.

    Args:
        command (str or list[str]): The command to be executed. This can be a string or a list of strings.

    Returns:
        str: The output of the command.
    """
    p = subprocess.run(command, cwd="C:/Users", capture_output=True, shell=True)
    decoded = p.stdout.decode("utf-8")
    return decoded


def get_flat_todo_list():
    """
    This function retrieves a flat list of to-do items.

    Returns:
        str: The output of the 'todo --flat' command.
    """
    return exec_command(["todo", "--flat"])


def get_done_tasks():
    """
    This function retrieves a list of completed to-do items.

    Returns:
        str: The output of the 'todo search --done' command.
    """
    return exec_command(shlex.split("todo search '""' --done"))


def get_future_todo_list():
    """
    This function retrieves a list of future to-do items.

    Returns:
        str: The output of the 'todo future' command.
    """
    return exec_command(["todo", "future"])


def get_tidy_todo_list():
    """
    This function retrieves a tidy list of to-do items.

    Returns:
        str: The output of the 'todo --tidy' command.
    """
    return exec_command(["todo", "--tidy"])


def exec_command_list(command_list: list[str]):
    """
    This function executes a list of commands in the shell.

    Args:
        command_list (list[str]): The list of commands to be executed. Each command is a string.
    """
    for command_str in command_list:
        try:
            parsed_arguments = shlex.split(command_str)
            print(" 🔃 ", f"Executing command: {parsed_arguments}")
            exec_command(parsed_arguments)
        except (AttributeError, Exception):
            print(" 🔃 ", f"Error parsing command: {command_str}")


def get_current_datetime():
    """
    This function retrieves the current date and time.

    Returns:
        str: The current date and time in the format "YYYY-MM-DDTHH:MM:SS".
    """
    return time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())


def search_and_return(pattern, _task):
    """
    This function searches for a pattern in a given task and returns the first match.

    Args:
        pattern (list[str]): The list of patterns to be searched for. Each pattern is a string.
        _task (str): The task in which to search for the pattern.

    Returns:
        str: The first match of the pattern in the task. If no match is found, an empty string is returned.
    """
    for p in pattern:
        match = re.search(p, _task)
        if match:
            return match.group(1)
    return ""


# return always a tuple of (position, title, priority, context, deadline)
def compile_todo_list(todo_list: str):
    """
    This function compiles a to-do list into a generator of tuples.

    Args:
        todo_list (str): The to-do list to be compiled. Each to-do item is a string.

    Yields:
        tuple: A tuple containing the position, title, priority, context, and deadline of each to-do item.
    """
    todo_list_items = todo_list.split("\n")[:-1]
    for line in todo_list_items:
        position = search_and_return(PATTERN_POSITION, line)
        title = search_and_return(PATTERN_TITLE, line)
        deadline = search_and_return(PATTERN_DEADLINE, line)
        priority = "" if search_and_return(PATTERN_PRIORITY, line) == "" \
            else (search_and_return(PATTERN_PRIORITY, line))
        context = search_and_return(PATTERN_CONTEXT, line)
        yield position, title, priority, context, deadline


def compile_todo_list_with_starts(todo_list: str):
    """
    This function compiles a to-do list into a generator of tuples, including the start date for future tasks.

    Args:
        todo_list (str): The to-do list to be compiled. Each to-do item is a string.

    Yields:
        tuple: A tuple containing the position, title, priority, context, deadline, and start date of each to-do item.
    """
    todo_list_items = todo_list.split("\n")[:-1]
    for line in todo_list_items:
        position = search_and_return(PATTERN_POSITION, line)
        title = search_and_return(FUTURE_PATTERN_TITLE, line)
        deadline = search_and_return(FUTURE_PATTERN_DEADLINE, line)
        priority = "" if search_and_return(FUTURE_PATTERN_PRIORITY, line) == "" \
            else (search_and_return(FUTURE_PATTERN_PRIORITY, line))
        context = search_and_return(FUTURE_PATTERN_CONTEXT, line)
        starts = search_and_return(FUTURE_PATTERN_STARTS, line)
        yield position, title, priority, context, deadline, starts


def get_pretty_printed_todo_list(future=False, done=False) -> str:
    """
    This function retrieves a pretty printed version of the to-do list.

    Args:
        future (bool, optional): If True, the function retrieves future tasks. Defaults to False.
        done (bool, optional): If True, the function retrieves completed tasks. Defaults to False.

    Returns:
        str: A string containing the pretty printed to-do list. Each to-do item is represented as a tuple.
             If the 'future' argument is True, the tuples also include the start date of each task.
             If the 'done' argument is True, the tag "[PENDING]" is not included in the tuples.
    """
    output_pretty_list = ""
    tag = "[PENDING]" if not done else ""
    if not future:
        item_template = Template("($position, " + tag + " $title, $priority, $deadline, $context)")
        for position, title, priority, context, deadline in compile_todo_list(
                get_flat_todo_list() if not done else get_done_tasks()
        ):
            line = item_template.substitute(
                position=position, title=title,
                priority=priority, deadline=deadline, context=context
            )
            output_pretty_list = output_pretty_list + (line + "\n")
        if output_pretty_list == "":
            if not done:
                output_pretty_list = "No tasks in the todo list.\n"
            else:
                output_pretty_list = "No tasks have been completed yet.\n"
    else:
        item_template = Template("($position, $title, $priority, $deadline, $context, $starts)")
        for position, title, priority, context, deadline, starts in compile_todo_list_with_starts(
                get_future_todo_list()):
            line = item_template.substitute(
                position=position, title=title,
                priority=priority, deadline=deadline, context=context, starts=starts
            )
            output_pretty_list = output_pretty_list + (line + "\n")
        if output_pretty_list == "":
            output_pretty_list = "No future tasks in the todo list.\n"
    return output_pretty_list
