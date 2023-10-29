from Generation.generator import llm_create
from Generation.Descriptions.summarize_context.model import MAX_LENGTH

def summarize_context(context: str) -> str:
    if len(context) <= MAX_LENGTH: return context
    return llm_create('summarize_context', context=context, number_of_characters=MAX_LENGTH)[0].summarized_context
