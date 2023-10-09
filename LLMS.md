# Supported LLMs
The default LLM to use can be set using `ADVENTURE_LLM` environment variable,
i.e. .env file.

## Currently supported models
* cohere: [Cohere command](https://cohere.com/models/command)
  * Reasonably capable, fast
* cohere-nightly: Cohere command, nightly/unstable version
  * Slow, should be usually avoided
* gpt-3.5: OpenAI's gpt-3.5-turbo-instruct
  * Quite capable, fast
* gpt-3.5-chat: OpenAI's gpt-3.5-turbo (chat model)
  * Probably equally capable to gpt-3.5-turbo-instruct
* gpt-4: OpenAI's GPT-4 (chat model)
  * **EXPENSIVE**, do not use!

When in doubt, use gpt-3.5 or cohere.

## Completion vs. chat models
TODO; for now, just use the non-chat versions if you encounter problems