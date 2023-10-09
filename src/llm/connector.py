import os
from abc import ABC, abstractmethod
from typing import TypedDict

import cohere
import openai
import tiktoken

class LogitBias:
    bias: dict[str, float]

    def __init__(self, bias: dict[str, float]):
        self.bias = bias

class LlmOptions(TypedDict):
    # Temperature or 'randomness' of the LLM
    # Generally in range of 0-2, higher values will be less predictable
    temperature: float
    # Penalizes tokens that have been recently seen by the LLM
    # Usually in range on 0-1
    frequence_penalty: float
    # Penalizes tokens that have been seen by the LLM at all
    # Usually in range on 0-1
    presence_penalty: float
    # Biases for particular tokens
    # Token ids mapped to bias value (-10 to 10)
    logit_bias: LogitBias

    # Maximum tokens the model will generate
    # This TRUNCATES longer responses but does not otherwise affect length of generated text!
    max_tokens: int
    # Amount of generations to return
    # Note that some of these generations could be duplicates!
    generations: int
    # List of strings that stop generation immediately if they are encountered
    # Stop sequences are not included in generated text
    stop_sequences: list[str]

EMPTY_OPTIONS: LlmOptions = {}

_DEFAULT_OPTIONS: LlmOptions = {
    'temperature': 1,
    'frequence_penalty': 0,
    'presence_penalty': 0,
    'logit_bias': LogitBias({}),
    'max_tokens': 300,
    'generations': 1,
    'stop_sequences': []
}

def _fill_options(options: LlmOptions) -> LlmOptions:
    return _DEFAULT_OPTIONS | (options or {})

def _clear_chat_markers(prompt: str) -> tuple[str, str]:
    return prompt.replace('---', '')

class _ChatMessage(TypedDict):
    role: str
    content: str

def _to_chat_prompt(prompt: str) -> list[_ChatMessage]:
    parts = prompt.split('---')
    messages = [{'role': 'system', 'content': parts[0]}]
    user_role = True
    for part in parts[1:]:
        messages.append({'role': 'user' if user_role else 'assistant', 'content': part})
        user_role = not user_role
    return messages

class LlmConnector(ABC):
    _bias_cache: dict[LogitBias, dict[str, float]]
    chat_model: bool

    def __init__(self, chat_model: bool):
        self._bias_cache = {}
        self.chat_model = chat_model

    @abstractmethod
    def complete(self, prompt: str, options: LlmOptions) -> list[str]:
        """
        Completes the given text prompt using an LLM.
        """
        pass

    @abstractmethod
    def tokenize(self, text: str) -> list[int]:
        pass

    def parse_bias(self, bias: LogitBias) -> dict[str, float]:
        if len(bias.bias) == 0:
            return {}
        if bias in self._bias_cache:
            return self._bias_cache[bias]
        tokenized = {}
        for tok_id, value in bias.bias.items():
            for token in self.tokenize(tok_id):
                # Allow all tokens in word, even though it slightly increases hallucination risk
                # Otherwise all logit_bias usage would need to be tested with ALL models
                tokenized[str(token)] = value
        self._bias_cache[bias] = tokenized
        return tokenized


class CohereConnector(LlmConnector):
    _model: str
    _client: cohere.Client

    def __init__(self, model: str):
        super().__init__(chat_model=False);
        self._model = model
        self._client = cohere.Client(os.environ['COHERE_API_KEY'])

    def complete(self, prompt: str, options: LlmOptions) -> list[str]:
        options = _fill_options(options)
        result = self._client.generate(
            model=self._model,
            prompt=_clear_chat_markers(prompt),
            temperature=options['temperature'],
            frequency_penalty=options['frequence_penalty'],
            presence_penalty=options['presence_penalty'],
            logit_bias=self.parse_bias(options['logit_bias']),
            max_tokens=options['max_tokens'],
            num_generations=options['generations'],
            end_sequences=options['stop_sequences']
            )
        return [gen.text for gen in result.generations]
    
    def tokenize(self, text: str) -> list[int]:
        return self._client.tokenize(model=self._model, text=text).tokens

class OpenAIConnector(LlmConnector):
    _model: str
    _encoding: tiktoken.Encoding

    def __init__(self, model: str, chat_model: bool):
        super().__init__(chat_model=chat_model)
        self._model = model
        self._encoding = tiktoken.encoding_for_model(model)
    
    def complete(self, prompt: str, options: LlmOptions) -> list[str]:
        options = _fill_options(options)
        if self.chat_model:
            results = openai.ChatCompletion.create(
                model=self._model,
                messages=_to_chat_prompt(prompt),
                temperature=options['temperature'],
                frequency_penalty=options['frequence_penalty'],
                presence_penalty=options['presence_penalty'],
                logit_bias=self.parse_bias(options['logit_bias']),
                max_tokens=options['max_tokens'],
                n=options['generations'],
                stop=options['stop_sequences'] if len(options['stop_sequences']) > 0 else None
            )
            return [gen.message.content for gen in results.choices]
        else:
            results = openai.Completion.create(
                model=self._model,
                prompt=_clear_chat_markers(prompt),
                temperature=options['temperature'],
                frequency_penalty=options['frequence_penalty'],
                presence_penalty=options['presence_penalty'],
                logit_bias=self.parse_bias(options['logit_bias']),
                max_tokens=options['max_tokens'],
                n=options['generations'],
                stop=options['stop_sequences'] if len(options['stop_sequences']) > 0 else None
            )
            return [gen.text for gen in results.choices]

    def tokenize(self, text: str) -> list[int]:
        return self._encoding.encode(text)

_model_name = os.environ['ADVENTURE_LLM']
connector: LlmConnector

if _model_name == 'cohere':
    connector = CohereConnector('command')
elif _model_name == 'command-nightly':
    connector = CohereConnector('command-nightly')
elif _model_name == 'gpt-3.5':
    connector = OpenAIConnector('gpt-3.5-turbo-instruct', chat_model=False)
elif _model_name == 'gpt-3.5-chat':
    connector = OpenAIConnector('gpt-3.5-turbo', chat_model=True)
elif _model_name == 'gpt-4':
    # EXPENSIVE, DO NOT USE
    connector = OpenAIConnector('gpt-4', chat_model=True)