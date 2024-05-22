import json
from string import Template
from typing import Any, Dict, Iterator, List, Optional

import requests
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.language_models.llms import LLM
from langchain_core.outputs import GenerationChunk


class CustomLLM(LLM):
    """A custom chat model that echoes the first `n` characters of the input.

    When contributing an implementation to LangChain, carefully document
    the model including the initialization parameters, include
    an example of how to initialize the model and include any relevant
    links to the underlying models documentation or API.

    Example:
        .. code-block:: python

            model = CustomChatModel(n=2)
            result = model.invoke([HumanMessage(content="hello")])
            result = model.batch([[HumanMessage(content="hello")],
                                 [HumanMessage(content="world")]])
    """

    llama_api_token = "<place llm aws token here>"
    """The API token to use for the LLM."""

    url = 'https://6xtdhvodk2.execute-api.us-west-2.amazonaws.com/dsa_llm/generate'
    """The URL to use for the LLM."""

    system_content: str
    """The system content to use for the LLM."""

    hint = ""
    """The hint to use for the LLM."""

    dialog = ""
    """The dialog to use for the LLM."""

    n = 512
    """The number of characters from the last message of the prompt to be echoed."""

    def _call(
            self,
            prompt: str,
            stop: Optional[List[str]] = None,
            run_manager: Optional[CallbackManagerForLLMRun] = None,
            **kwargs: Any,
    ) -> str:
        """Run the LLM on the given input.

        Override this method to implement the LLM logic.

        Args:
            prompt: The prompt to generate from.
            stop: Stop words to use when generating. Model output is cut off at the
                first occurrence of any of the stop substrings.
                If stop tokens are not supported consider raising NotImplementedError.
            run_manager: Callback manager for the run.
            **kwargs: Arbitrary additional keyword arguments. These are usually passed
                to the model provider API call.

        Returns:
            The model output as a string. Actual completions SHOULD NOT include the prompt.
        """
        if stop is not None:
            raise NotImplementedError("Stop tokens are not supported.")
        llama_template = Template(
            self.dialog +
            "<s>" +
            "[INST] <<SYS>>\n$system_content\n<</SYS>>\n\n"
            "$prompt" +
            "[/INST]\n" +
            self.hint + "\n"
        )
        body = {
            "prompt": llama_template.substitute(
                prompt=prompt,
                system_content=self.system_content
            ),
            "max_gen_len": self.n,
            "temperature": kwargs.get("temperature", 0.5),
            "top_p": 1,
            "length_penalty": 1,
            "presence_penalty": 0,
            "api_token": self.llama_api_token,
        }
        res = requests.post(self.url, json=body)
        print(res.text)
        return json.loads(res.text)["body"]["generation"]

    def _stream(
            self,
            prompt: str,
            stop: Optional[List[str]] = None,
            run_manager: Optional[CallbackManagerForLLMRun] = None,
            **kwargs: Any,
    ) -> Iterator[GenerationChunk]:
        """Stream the LLM on the given prompt.

        This method should be overridden by subclasses that support streaming.

        If not implemented, the default behavior of calls to stream will be to
        fallback to the non-streaming version of the model and return
        the output as a single chunk.

        Args:
            prompt: The prompt to generate from.
            stop: Stop words to use when generating. Model output is cut off at the
                first occurrence of any of these substrings.
            run_manager: Callback manager for the run.
            **kwargs: Arbitrary additional keyword arguments. These are usually passed
                to the model provider API call.

        Returns:
            An iterator of GenerationChunks.
        """
        raise NotImplemented("Streaming is not supported.")

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        """Return a dictionary of identifying parameters."""
        return {
            "model_name": "Llama2-70B",
        }

    @property
    def _llm_type(self) -> str:
        """Get the type of language model used by this chat model. Used for logging purposes only."""
        return "Meta"
