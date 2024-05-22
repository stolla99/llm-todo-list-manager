import queue
import threading

import logic_llm.chain_llm as chains
from logic_todo import todo_cmd


class ApiResponse:
    """
    This class represents an API response.
    """
    def __init__(self):
        self.done = False
        self.request_done = False
        self.char_length = 0


def start_thread(
        _api_response: ApiResponse,
        prompt: str,
        location_data: dict,
        enable_check: bool,
        api_response_queue: queue.Queue,
        todo_update_queue: queue.Queue
):
    """
    This function starts a new thread to stream the API response.

    Args:
        _api_response (ApiResponse): An instance of the ApiResponse class.
        prompt (str): The prompt to be processed.
        location_data (dict): A dictionary containing the location data.
        enable_check (bool): A flag indicating whether to enable the check.
        api_response_queue (queue.Queue): A queue for collecting the responses.
        todo_update_queue (queue.Queue): A queue for updating the to-do list.
    """
    print(" 😶‍🌫️ ", "Starting thread...")
    thread = threading.Thread(
        target=stream_api_response,
        daemon=True,
        args=(
            _api_response,
            prompt,
            location_data,
            enable_check,
            api_response_queue,
            todo_update_queue))
    thread.start()


def chunk_string_generator(s: str, chunk_size: int) -> str:
    """
    This function generates chunks of a given string.

    Args:
        s (str): The string to be chunked.
        chunk_size (int): The size of each chunk.

    Yields:
        str: The next chunk of the string.
    """
    for i in range(0, len(s), chunk_size):
        yield s[i:i + chunk_size]


def stream_api_response(
        _api_response: ApiResponse,
        prompt: str,
        location_data: dict,
        enable_check: bool,
        collected_queue: queue.Queue,
        todo_update_queue: queue.Queue
):

    """
    This function streams the API response by processing the prompt and location data, and updating the to-do list.

    Args:
        _api_response (ApiResponse): An instance of the ApiResponse class.
        prompt (str): The prompt to be processed.
        location_data (dict): A dictionary containing the location data.
        enable_check (bool): A flag indicating whether to enable the check.
        collected_queue (queue.Queue): A queue for collecting the responses.
        todo_update_queue (queue.Queue): A queue for updating the to-do list.
    """
    chars = 0
    must_check = False
    if enable_check:
        response, must_check = chains.zero_shot_bert(prompt)
        response = response + "\n\n"
        collected_queue.put(response)
        chars += len(response)
    if must_check:
        chains.lon = location_data["lon"]
        chains.lat = location_data["lat"]
        model_weather_recommendation = chains.weather_chain.invoke(prompt)
        recommendation_output = model_weather_recommendation + "\n\n"
        collected_queue.put(recommendation_output)
        chars += len(recommendation_output)
    else:
        recommendation_output = ""
    new_input = prompt + "\n\n" + recommendation_output
    model_output: dict = chains.todo_command_chain.invoke(new_input)
    print(" 🦙 ", model_output)
    to_user = model_output["response"] + "\n\n"
    collected_queue.put(to_user)
    chars += len(to_user)
    todo_cmd.exec_command_list(model_output["commands"])
    collected_queue.join()

    # finishing up
    _api_response.char_length = chars
    _api_response.request_done = True
    print(" 😶‍🌫️ ", "Request fulfilled...")
    todo_update_queue.put(True)
    todo_update_queue.join()
    print(" 😶‍🌫️ ", "Todo list updated...")
