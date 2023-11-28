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

## Example imagery
Since the application can't be run wihtout an active OpenAI key, we'll provide some image examples of the application. \
The title screen:
![Title screen](https://github.com/AnttiVainikka/TextAdventure/assets/77774384/d621387a-528a-4316-a925-ca0a5248fd19)
A scenario description:
![Scenario description](https://github.com/AnttiVainikka/TextAdventure/assets/77774384/8b12bde8-2068-4a4f-a783-6299e40c9dc9)
Choosing a faction to interact with:
![Faction choices](https://github.com/AnttiVainikka/TextAdventure/assets/77774384/5721ec56-f39f-4f85-a189-47afe1ae3a0d)
Text generated while adventuring:
![Example exploring text](https://github.com/AnttiVainikka/TextAdventure/assets/77774384/e2e1612f-c3a5-4e87-9e47-90452dc8201c)
A combat encounter:
![Example combat encounter](https://github.com/AnttiVainikka/TextAdventure/assets/77774384/7785c870-aa85-4ad8-8e90-8d8bf595e07e)
An enemy:
![Example enemy](https://github.com/AnttiVainikka/TextAdventure/assets/77774384/7f87c1da-a0f6-4466-867d-b51ff08331da)
A protagonist:
![Example protag](https://github.com/AnttiVainikka/TextAdventure/assets/77774384/8b0e88b2-1a3e-42ee-a6a2-ae2426c9e85d)
Protagonist's inventory:
![Example inventory](https://github.com/AnttiVainikka/TextAdventure/assets/77774384/8cc83c94-b581-4fd7-8cfa-2aff42e0c6c1)
