# TextAdventure
LLM-based text adventure game / tech demo.

## Installation
You'll need Python 3.11 and [Poetry](https://python-poetry.org/) for development.

To install dependencies, run:
```sh
poetry install
poetry config virtualenvs.in-project true # For editor support
```

Then, create `.env` file from `.env.sample` that is committed to Git.
Fill your API keys to the .env file. **NEVER** commit the API keys to Git!

Then, to use the created venv from shell, run:
```sh
poetry shell
```