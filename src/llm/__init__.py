import json
from typing import TypeVar
from dotenv import load_dotenv
from pydantic import ValidationError
import regex

load_dotenv()

from llm.connector import EMPTY_OPTIONS, connector
from llm.question import Question as Question
from llm.structured import create_prompt, gen_sample
from llm.error import GenerateFailure as GenerateFailure

_BASE_PROMPT = 'You are a fantasy text adventure game generator.'

def complete(prompt: str, options=EMPTY_OPTIONS) -> str:
    """
    Completes the given prompt using LLM and returns the most likely response.
    """
    if options.get('generations', 1) != 1:
        raise ValueError('multiple generations not supported')
    return connector.complete(f'{_BASE_PROMPT}\n\n{prompt}', options)[0]

def complete_choices(prompt: str, count: int) -> set[str]:
    """
    Completes the prompt to generate multiple choices.
    This might call LLM multiple times if there are duplicates.
    """
    # The LLM might generate duplicates, so call it until we get X unique choices
    results = set()
    while len(results) < count:
        remaining = count - len(results)
        completions = connector.complete(prompt, {'generations': remaining})
        for i in range(min(len(completions), remaining)):
            results.add(completions[i])
    return results


T = TypeVar('T')
def generate(prompt: str, to_desc: str, to_type: type[T], examples: list[T], count=1) -> list[T]:
    """
    Completes the prompt to generate a structured response.
    """
    prompt = f"""You are an AI text adventure game master.

Format your responses in JSON, as instructed by the user. Be creative in what you generate, but ALWAYS stick to the format described to you!
---
{prompt}

{create_prompt(to_desc, to_type, examples)}"""
    
    results = []
    for _ in range(count):
        prompt, result = gen_sample(prompt, to_type)
        prompt += 'Good. Now create an another reply like that:\n'
        results.append(result)
    
    return results
