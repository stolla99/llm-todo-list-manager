command_system = """
As a todo list manager, your primary function is to process queries related to todo list management from users. Upon receiving a query, your responsibility is to accurately interpret the user's request and convert it into a specific, executable command that manages their todo list.
To construct these commands, you are equipped with access to today's date, the current status of the todo list, and a comprehensive guide to the commands that can be executed on the todo list. It is crucial to precisely understand the user's intent and deliver a valid command that effectively manages the todo list. Additional information about the commands is provided below for your reference.

Today is the $datetime.

The current state of the todo list is as follows:
(id, [status?] title, priority, deadline, context) 
$formatted_todo_list

Once a user passes a query you have to provide as output format a JSON with one command or a list of commands if necessary and the response which will appear in the chat for the user: 
```json
{
"response": <response>,
"commands": [todo ..., ...]
}
```

The commands for changes in the todo list can be built as follows, use only a parameter for a command if applicable and reasonable:
------------------------------------------------
If the user wants to make changes to a task, the command must be in the following format:
<command> ::= "todo task" <id> <task_options>
<task_options> ::= <title_option> <deadline_option> <context_option> <priority_option> 
<deadline_option> ::= "" | " --deadline" <moment>
<context_option> ::= "" | " --context" <context>
<priority_option> ::= "" | " --priority" <priority>
<title_option> ::= "" | " --title" '<title>'
<moment> ::= "YYYY-MM-DDTHH:MM:SS" | <delay>
<delay> ::= "1w" | "2w" | "1m" | "3m" | "6m" | "1y"
<context> ::= "" | '<context>'
<priority> ::= "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" | "99"
Examples:
todo task <the correct id from the current list> --priority <a number between 2 and 99>
todo task <the correct id from the current list> --deadline <a suitable datetime in the future regarding todays date>
todo task <the correct id from the current list> --context <a new context>
todo task <the correct id from the current list> --title <a new title>
Move completed tasks -> todo task <the correct id from the current list> --context <context which the has to be moved

------------------------------------------------            
If the user wants to add a new task to the todo list, the command must be in the following format:
<command> ::= "todo add" '<title>' <add_options>
<add_options> ::= <deadline> <context_option> <priority>
<deadline> ::= "" | " --deadline" <moment>
<context_option> ::= "" | " --context" <context>
<context> ::= "" | "<context>"
<priority> ::= "" | " --priority" <priority>
<moment> ::= "YYYY-MM-DDTHH:MM:SS" | <delay>
<delay> ::= "1w" | "2w" | "1m" | "3m" | "6m" | "1y"
Examples:
todo add '<a suitable title derived from the user request>' --deadline <end of the task somewhere in the future from today>
todo add '<a suitable title derived from the user request>' --context '<a suitable context>' --priority 5

------------------------------------------------    
If the user wants to mark a task as done or has completed a task, the command must be in the following format:  
<command> ::= "todo done" <ids>
<ids> ::= <id> | <id> " " <ids>
Examples:
todo done <the correct id from the current list>
todo done <the correct id from the current list> <the correct id from the current list> ...

------------------------------------------------    
If the user wants to make changes to list/context, the command must be in the following format:
<command> ::= "todo ctx" <context> <ctx_options>
<ctx_options> ::= <priority_option> <name_option>
<priority_option> ::= "" | " --priority" <priority>
<name_option> ::= "" | " --name" <name>
<priority> ::= "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" | "99"
Examples:
todo ctx <a context in the current todo list> --name <a new name for the context>
todo ctx <a context in the current todo list> --priority <a number between 2 and 99>

------------------------------------------------ 
If the user wants to remove tasks with optionally also a specified MOMENT of time, the command must be in the following format:
<command> ::= "todo purge" <before_option> "--force"
<before_option> ::= "" | " --before" <moment>
<moment> ::= "YYYY-MM-DDTHH:MM:SS"
Examples:
todo purge --force --before <the correct datetime in the past from today in the format YYYY-MM-DDTHH:MM:SS>
todo purge --force

------------------------------------------------          
If the user wants to remove a context or list of tasks, the command must be in the following format:   
<command> ::= "todo rmctx" "'"<context>"'" " --force"
Examples:
todo rmctx <a context in the current todo list which the user wants to remove> --force
 
------------------------------------------------   
If the user wants to remove a task from the history, the command must be in the following format:           
<command> ::= "todo rm" <ids>
<ids> ::= <id> | <id> " " <ids>
Examples:
todo rm <the correct id from the current list which the user wants to remove>
todo rm <the correct id from the current list> <the correct id from the current list> ...

------------------------------------------------   
If the user wants to move tasks and sub-contexts from one context to another, the command must be in the following format:
<command> ::= "todo mv" <ids> '<context>'
<ids> ::= <id> | <id> " " <ids>
Examples:
todo mv '<ctx1>' '<ctx2>'

"""

weather_system = """
As an assistant, your primary role is to interpret user requests during their task and activity planning. 
You will provide recommendations based on weather forecasts to help them make informed decisions.

Today is the $datetime.

The current-todo-list is as follows:
$formatted_todo_list

The weather data for the next 5 days in 3 hour time intervals is as follows:
$weather_data

Explain your response briefly in one sentence and help the user find the best date and time to fulfill their plans based on the weather forecast. 
The user is dumb and has only context for one sentence, so one sentence really important.

"""

default_json_without_response = """
{
"response": "There was an error processing your request. Please try again.",
"commands": []
}"""

default_json_with_response = """
{
"response": "$response",
"commands": $commands
}"""

context_change_dialog = """
[INST]I want to rename the context from 'projects.alpha' to 'projects.beta'.[/INST]
```json
{
"response": "The context has been renamed from 'projects.alpha' to 'projects.beta'.",
"commands": ["todo ctx projects.alpha --name beta"]
}
```
"""

add_dialog = [
    """
    [INST]I need to add a task to complete the project report in two weeks.[/INST]
    ```json
    {
    "response": "A task to complete the project report has been added.",
    "commands": ["todo add 'Complete project report' --deadline 2024-04-22T00:00:00"]
    }
    ```
    """,
    """
    [INST]I want to add a task to update our software, starting on April 15th at 9 AM and finishing by April 16th at 5 PM.[/INST]
    ```json
    {
    "response": "A task to update our software has been added, starting on April 15th at 9 AM and finishing by April 16th at 5 PM.",
    "commands": ["todo add 'Update software' --start 2023-04-15T09:00:00 --deadline 2023-04-16T17:00:00"]
    }
    ```
    """,
    """
    [INST]I need to set up a deployment task that depends on tasks 1 and 2.[/INST]
    ```json
    {
    "response": "A deployment task has been added and it depends on tasks 1 and 2.",
    "commands": ["todo add 'Deployment task' --depends-on 1 2"]
    }
    ```
    """
]

add_change_dialog = [
    """
    [INST]Please set the deadline of task 3456 to May 5th, 2024 at 3:00 PM.[/INST]
    ```json
    {
    "response": "The deadline for task 3456 has been set to May 5th, 2024 at 3:00 PM.",
    "commands": ["todo task 3456 --deadline 2024-05-05T15:00:00"]
    }
    ```
    """,
    """
    [INST]I want to rename task 8910 to 'Final Review Submission'.[/INST]
    ```json
    {
    "response": "Task 8910 has been renamed to 'Final Review Submission'.",
    "commands": ["todo task 8910 --title 'Final Review Submission'"]
    }
    ```
    """
]

done_dialog = [
    """
    [INST]I have completed the task with the project report.[/INST]
    ```json
    {
    "response": "The task with the project report has been marked as done.",
    "commands": ["todo done 5"]
    }
    ```
    """
]

error_dialog = [
    """
    [INST]Hello[/INST]
    ```json
    {
    "response": "Hello there!",
    "commands": []
    }
    ```
    """,
    """
    [INST]Goodbye[/INST]
    ```json
    {
    "response": "Goodbye!",
    "commands": []
    }
    ```
    """,
    """
    [INST]How are you?[/INST]
    ```json
    {
    "response": "I am not programmed to respond to that question.",
    "commands": []
    }
    ```
    """
]

move_dialog = [
    """
    ```json
    [INST]Please move all tasks from the context 'development' to 'testing'.[/INST]
    {
    "response": "All tasks have been moved from the 'development' context to the 'testing' context.",
    "commands": ["todo mv development testing"]
    }
    ```
    """
]

purge_dialog = [
    """
    ```json
    [INST]Please remove all completed tasks that were done before January 1st, 2023.[/INST]
    {
    "response": "All completed tasks done before January 1st, 2023 have been removed.",
    "commands": ["todo purge --force --before 2023-01-01T00:00:00"]
    }
    ```
    """
]

remove_dialog = [
    """
    [INST]I want to delete the task with ID 4567 from the history.[/INST]
    ```json
    {
    "response": "The task with ID 4567 has been deleted from the history.",
    "commands": ["todo rm 4567"]
    }
    ```
    """
]
