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

## Running
Run the scripts from root directory of this repository. Although Python imports
don't care about your working directory, other files are also accessed using
relative paths.

```sh
$ pwd
/home/you/TextAdventure
$ python src/main.py
```