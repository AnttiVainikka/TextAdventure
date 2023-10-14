import json
import regex
from llm.connector import connector
import importlib

DESCRIPTION_DIRECTORY = "Generation/Descriptions"
FORM_FILE_NAME = "form.py"
QUERY_FILE_NAME = "query_text"
EXAMPLES_FILE_NAME = "examples.json"
PREDEFINED_FILE_NAME = "predefined.json"
FORM_FILE = DESCRIPTION_DIRECTORY + "/" + "{type_name}/" + FORM_FILE_NAME
QUERY_FILE = DESCRIPTION_DIRECTORY + "/" + "{type_name}/" + QUERY_FILE_NAME
EXAMPLES_FILE = DESCRIPTION_DIRECTORY + "/" + "{type_name}/" + EXAMPLES_FILE_NAME
PREDEFINED_FILE = DESCRIPTION_DIRECTORY + "/" + "{type_name}/" + PREDEFINED_FILE_NAME
FORM_MODUL_NAME = "form"
FORM_CLASS_NAME = "form"
EXAMPLES_KEY = "Examples"
NUMBER_OF_TRIES_TO_GENERATE = 2

class Generator:
    __json_pattern = regex.compile(r'\{(?:[^{}]|(?R))*\}')

    def __init__(self, type_name: str):
        self._type_name = type_name
        loader = importlib.machinery.SourceFileLoader(FORM_MODUL_NAME, FORM_FILE.format(type_name=type_name))
        module = loader.load_module()
        self._form = getattr(module, FORM_CLASS_NAME)
        self._template_query_text = open(QUERY_FILE.format(type_name=type_name), 'r').read()
        examples = json.load(open(EXAMPLES_FILE.format(type_name=type_name), 'r'))
        self._examples = []
        for example in examples[EXAMPLES_KEY]:
            self._examples.append(json.dumps(example, indent=4))

    def generate(self, **kwargs) -> (bool, dict):
        query_text = self._template_query_text.replace("{{form}}", json.dumps(self._form().model_dump(), ensure_ascii=False, indent=4))
        for (key, value) in kwargs.items():
            query_text = query_text.replace(f"{{{{{key}}}}}", value)
        
        if (len(self._examples) > 0):
            query_text += "\nFor example:\n"
            for example in self._examples:
                query_text += "\n" + example

        for _ in range(NUMBER_OF_TRIES_TO_GENERATE):
            data = self.__generate(query_text)
            if data != None: return (True, data)
        
        # Use predefined
        return (False, json.load(open(PREDEFINED_FILE.format(type_name=self._type_name))))

    def __generate(self, text: str):
        generated_text = connector.complete(text, None)[0]
        json_texts = Generator.__json_pattern.findall(generated_text)
        # Hopefully it only contains one json substring
        for json_text in json_texts:
            json_object = json.loads(json_text)
            try:
                form = self._form(**json_object)
                return form.model_dump()
            except:
                pass
        return None
