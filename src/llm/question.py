from llm.connector import LogitBias, connector

_BASE_PROMPT = 'You are a fantasy text adventure game generator.'

class Question:
    """
    A question for an LLM. Try to initialize questions once and then reuse
    them, computing the logit bias for choices may require a remote call.

    question: The question.
    choices: A list of accepted answers for the question. If empty,
    a brief free-form answer is returned instead.
    """
    question: str
    _choices: list[str]

    def __init__(self, question: str, choices=[]):
        self.question = question
        self._choices = choices
        self._bias = LogitBias({word: 9 for word in choices})

    def ask(self, context: str) -> str:
        """
        Asks the question with the given context and returns the answer.
        """
        prompt = f"""{_BASE_PROMPT}

Here is a description of an in-game situation:
{context}

Please answer the following question about it: {self.question}

Consider these one-word answers: {', '.join(self._choices)}
Pick one of them, and justify your choice.
"""
        answer = connector.complete(prompt, {
            'temperature': 0.5,
        })[0]

        if len(self._choices) > 0:
            prompt += f"""---
{answer}

Now, repeat the one-word answer:
"""
            return connector.complete(prompt, {
                'temperature': 0.2,
                'max_tokens': 10,
                'logit_bias': self._bias
            })[0]
        else:
            return answer