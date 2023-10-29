import json
import random
import importlib

import llm

_DESCRIPTION_PATH = 'src/Generation/Descriptions/{type_name}'
_MODEL_FILE = _DESCRIPTION_PATH + '/model.py'
_QUERY_FILE = _DESCRIPTION_PATH + '/query_text'
_EXAMPLES_FILE = _DESCRIPTION_PATH + '/examples.json'
_PREDEFINED_FILE = _DESCRIPTION_PATH + '/predefined.json'
_MODEL_MODULE_NAME = "model"
_MODEL_CLASS_NAME = "Model"

_generator_cache: dict[str, 'Generator'] = {}

def llm_create(type_name: str, count=1, **kwargs) -> list[dict]:
    if type_name in _generator_cache:
        generator = _generator_cache[type_name]
    else:
        generator = Generator(type_name)
        _generator_cache[type_name] = generator
    return generator.generate(count, **kwargs)[1]

class Generator:
    def __init__(self, type_name: str):
        self._type_name = type_name
        loader = importlib.machinery.SourceFileLoader(_MODEL_MODULE_NAME, _MODEL_FILE.format(type_name=type_name))
        module = loader.load_module()
        self._model = getattr(module, _MODEL_CLASS_NAME)
        with open(_QUERY_FILE.format(type_name=type_name), 'r') as f:
            self._template_query_text = f.read()

        try:
            with open(_EXAMPLES_FILE.format(type_name=type_name), 'r') as f:
                self._examples = list([self._model(**sample) for sample in json.load(f)])
        except FileNotFoundError:
            self._examples = []

        try:
            with open(_PREDEFINED_FILE.format(type_name=self._type_name), 'r') as f:
                self._fallbacks = list([self._model(**fallback) for fallback in json.load(f)])
        except FileNotFoundError:
            self._fallbacks = []

    def generate(self, count: int, **kwargs) -> (bool, dict):
        query_text = self._template_query_text
        for key, value in kwargs.items():
            query_text = query_text.replace(f"{{{{{key}}}}}", str(value))
        
        query_parts = query_text.split('---', maxsplit=1)

        try:
            # Try to get LLM generate us what we want
            reply = llm.generate(query_parts[0], query_parts[1] if len(query_parts) > 1 else 'Answer:', self._model, self._examples, count)
            return (True, reply)
        except llm.GenerateFailure as e:
            if len(self._fallbacks) > 0:
                # Use predefined fallback
                return (False, self._fallbacks[random.randint(0, len(self._fallbacks) - 1)].model_dump())
            else:
                # No predefined options available, need to crash
                raise e
