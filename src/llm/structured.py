import json
from typing import Type, TypeVar
from pydantic import BaseModel, ValidationError
import regex

from llm import connector
from llm.error import GenerateFailure

def _schema_to_prompt(json_schema: dict[str, any]) -> str:
    data = {}
    for key, details in json_schema['properties'].items():
        data[key] = details['title']
    return json.dumps(data, indent=2)

def _examples_to_prompt(examples: list[BaseModel]) -> str:
    return '\n\n'.join([sample.model_dump_json(indent=2) for sample in examples])

T = TypeVar('T')

def create_prompt(short_prompt: str, cls: Type[T], examples: list[T]) -> str:
    prompt = f"""Format your reply in JSON like this:
{_schema_to_prompt(cls.model_json_schema())}
"""
    if len(examples) > 0:
        prompt += f"""Here are examples of what it could look like:
{_examples_to_prompt(examples)}
"""
    
    prompt += f"""
Generate JSON that includes the requested fields and nothing else!

{short_prompt}
"""

    return prompt

_MAX_TRIES = 2
_JSON_PATTERN = regex.compile(r'\{(?:[^{}]|(?R))*\}')

def gen_sample(prompt: str, to_type: type[T]) -> T:
    for _ in range(_MAX_TRIES):
        result = connector.complete(prompt, {'max_tokens': 500})[0]
        json_texts = _JSON_PATTERN.findall(result)
        if len(json_texts) == 0:
            # Just retry without editing the prompt
            continue
        json_text = json_texts[0]
        prompt += f'---\n{json_text}\n---\n'
        try:
            json_dict = json.loads(json_text)
        except json.JSONDecodeError as e:
            prompt += f'That is not valid JSON: {e.msg}. Reply with fixed JSON only:'
            continue
        try:
            model = to_type(**json_dict)
        except ValidationError as e:
            prompt += f'I got the following error validating that: {e.msg}. Reply with fixed JSON data only:'
            continue
        return prompt, model
    raise GenerateFailure(f'failed generate, exceeded {_MAX_TRIES} tries')