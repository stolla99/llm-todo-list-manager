import json
import random
import re
from json import JSONDecodeError
from string import Template
from typing import Any

from json_repair import repair_json
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import Field
from langchain_core.runnables import RunnablePassthrough, RunnableLambda, RunnableSerializable, chain
from openai import BaseModel
from transformers import pipeline

import logic_llm.prompts_llm as prompts
import logic_todo.todo_cmd as todo_cmd
from custom_llm.llama_llm import CustomLLM
from logic_weather import weather_api
from logic_weather.weather_api import fetch_weather_forecast


class CommandResponse(BaseModel):
    """
    This class represents the response to a command.
    """
    response: str = Field(..., description="response to the user")
    commands: list[str] = Field(default_factory=list, description="list of commands to execute")


def compile_llm_output(response: str) -> str:
    """
    This function compiles the output of the LLM by removing the stop token and everything after it.

    Args:
        response (str): The raw output from the LLM.

    Returns:
        str: The compiled output, with the stop token and everything after it removed.
    """
    stop_token = "```"
    pattern = f"^(.*)({stop_token})"
    match = re.match(pattern, response, re.DOTALL)
    if match:
        return match.group(1)
    else:
        return prompts.default_json_without_response


def validate_and_repair_json(potentially_malformed_json: str) -> str:
    """
    This function validates and repairs a potentially malformed JSON string.

    Args:
        potentially_malformed_json (str): The potentially malformed JSON string.

    Returns:
        str: The repaired JSON string if the input was malformed, otherwise the original JSON string.
    """
    repaired_json = repair_json(potentially_malformed_json)
    try:
        _ = json.loads(repaired_json)
        return repaired_json
    except JSONDecodeError:
        print(" 🔗 ", "Malformed JSON...")
        return prompts.default_json_without_response


def get_system_content() -> str:
    """
    This function generates a string that represents the system content.

    Returns:
        str: A string that represents the system content.
    """
    system_content = Template(prompts.command_system)
    return system_content.substitute(
        datetime=todo_cmd.get_current_datetime(),
        formatted_todo_list=(
                todo_cmd.get_pretty_printed_todo_list() +
                todo_cmd.get_pretty_printed_todo_list(done=True)
        )
    )


def get_weather_system_content(longitude, latitude) -> str:
    """
    This function fetches the weather forecast for a given location and formats it into a string.

    Args:
        longitude (str): The longitude of the location.
        latitude (str): The latitude of the location.

    Returns:
        str: A string containing the weather forecast and the current to-do list.
    """
    if lon == "" or lat == "":
        _lon, _lat = weather_api.fetch_geocode("Kaiserslautern", "DE", 1)
        code, forecast_data = fetch_weather_forecast(_lon, _lat)
    else:
        code, forecast_data = fetch_weather_forecast(longitude, latitude)
    return Template(prompts.weather_system).substitute(
        datetime=todo_cmd.get_current_datetime(),
        weather_data=weather_api.get_weather_string(forecast_data),
        formatted_todo_list=(
                todo_cmd.get_pretty_printed_todo_list() +
                todo_cmd.get_pretty_printed_todo_list(done=True)
        )
    )


def get_todo_command_chain(llm: CustomLLM, prompt: ChatPromptTemplate) -> RunnableSerializable[Any, Any]:
    """
    This function creates a chain of operations for generating a response based on a to-do command.

    Args:
        llm (CustomLLM): An instance of the CustomLLM class which is used to generate language based on a given prompt.
        prompt (ChatPromptTemplate): A template for the chat prompt.

    Returns:
        RunnableSerializable[Any, Any]: A chain of operations for generating a response based on a to-do command.
    """
    parser = JsonOutputParser(pydantic_object=CommandResponse)
    command_chain = (
            {"topic": RunnablePassthrough()}
            | prompt
            | llm
            | RunnableLambda(compile_llm_output)
            | RunnableLambda(validate_and_repair_json)
            | parser)
    return command_chain


@chain
def todo_command_chain(text: str):
    """
    This function uses a chain of operations to generate a response based on a to-do command.

    Args:
        text (str): The input text which is used as a topic for the chain of operations.

    Returns:
        dict: The output of the model after the chain of operations.
    """
    llm_command = CustomLLM(
        dialog=build_dialog(),
        system_content=get_system_content(),
        hint="```json")
    command_chain = get_todo_command_chain(llm_command, ChatPromptTemplate.from_template("{topic}"))
    model_output: dict = command_chain.invoke({"topic": text})
    return model_output


def get_weather_command_chain(llm: CustomLLM, prompt: ChatPromptTemplate) -> RunnableSerializable[Any, Any]:
    """
    This function creates a chain of operations for generating a response based on the weather.

    Args:
        llm (CustomLLM): An instance of the CustomLLM class which is used to generate language based on a given prompt.
        prompt (ChatPromptTemplate): A template for the chat prompt.

    Returns:
        RunnableSerializable[Any, Any]: A chain of operations for generating a response based on the weather.
    """
    weather_rag_chain = (
            {"topic": RunnablePassthrough()}
            | prompt
            | llm)
    return weather_rag_chain


lon, lat = "", ""
classifier = pipeline("zero-shot-classification", model="MoritzLaurer/deberta-v3-large-zeroshot-v2.0")


@chain
def weather_chain(text: str):
    """
    This function uses a chain of operations to generate a response based on the weather.

    Args:
        text (str): The input text which is used as a topic for the chain of operations.

    Returns:
        dict: The output of the model after the chain of operations.
    """
    global lon
    global lat
    llm_weather_rag = CustomLLM(
        system_content=get_weather_system_content(longitude=lon, latitude=lat),
        hint="One recommendation sentence:")
    weather_rag_chain = get_weather_command_chain(llm_weather_rag, ChatPromptTemplate.from_template("{topic}"))
    model_output: dict = weather_rag_chain.invoke({"topic": text})
    return model_output


def zero_shot_bert(text: str) -> [str, bool]:
    """
    This function uses a zero-shot classifier to determine if the weather is important for a given task.

    Args:
        text (str): The text of the task.

    Returns:
        str: A message indicating whether the weather is important or not.
        bool: A boolean value indicating whether the weather is important or not.
    """
    global classifier
    labels = ["indoor", "outdoor"]
    results = classifier(text, labels, multi_label=False)
    if results["labels"][0] == labels[1] and results["scores"][0] > 0.60:
        print(" 🌤️ ", "Weather is important...")
        return "I will check the weather for you...\n\n", True
    else:
        return "I think weather is not important for this task...\n\n", False


def build_dialog() -> str:
    """
     This function builds a dialog string by shuffling and joining a list of dialog prompts.

     Returns:
         str: A string containing the shuffled and joined dialog prompts. Each prompt is enclosed in <s> tags.
    """
    s_s = lambda t: f"<s>{t}</s>"
    full_dialog = [
        s_s(inst.strip()) for inst in
        [
            *prompts.add_dialog,
            *prompts.add_change_dialog,
            *prompts.error_dialog
        ]
    ]
    random.shuffle(full_dialog)
    return "\n".join(full_dialog)
