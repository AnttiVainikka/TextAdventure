import os
from abc import ABC, abstractmethod
from typing import TypedDict

import cohere

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

class LlmConnector(ABC):
    _bias_cache: dict[LogitBias, dict[str, float]]

    def __init__(self):
        self._bias_cache = {}

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
            tokens = self.tokenize(tok_id)
            if len(tokens) != 1:
                raise ValueError(f'logit_bias does not support multi-token words such as {tok_id}')
            tokenized[str(tokens[0])] = value
        self._bias_cache[bias] = tokenized
        return tokenized


class CohereConnector(LlmConnector):
    _model: str
    _client: cohere.Client

    def __init__(self):
        super().__init__();
        self._model = 'command-nightly'
        self._client = cohere.Client(os.environ['COHERE_API_KEY'])

    def complete(self, prompt: str, options: LlmOptions) -> list[str]:
        options = _fill_options(options)
        result = self._client.generate(
            model=self._model,
            prompt=prompt,
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


_model_name = os.environ['ADVENTURE_LLM']
connector: LlmConnector

if _model_name == 'cohere':
    connector = CohereConnector()