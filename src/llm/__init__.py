import os
from dotenv import load_dotenv
load_dotenv()

from llm.connector import EMPTY_OPTIONS, connector

from llm.question import Question as Question

_BASE_PROMPT = 'You are a fantasy text adventure game generator.'

def complete(prompt: str, options=EMPTY_OPTIONS) -> str:
    """
    Completes the given prompt using LLM and returns the most likely response.
    """
    if options['generations'] != 1:
        raise ValueError('multiple generations not supported')
    return connector.complete(f'{_BASE_PROMPT}\n\n{prompt}', options)[0]

