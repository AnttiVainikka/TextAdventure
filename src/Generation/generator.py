import json
import regex
from llm.connector import connector

DESCRIPTION_DIRECTORY = "Generation/Descriptions"
FORM_FILE_NAME = "form.json"
QUERY_FILE_NAME = "query_text"
EXAMPLES_FILE_NAME = "examples.json"
PREDEFINED_FILE_NAME = "predefined.json"
FORM_FILE = DESCRIPTION_DIRECTORY + "/" + "{type_name}/" + FORM_FILE_NAME
QUERY_FILE = DESCRIPTION_DIRECTORY + "/" + "{type_name}/" + QUERY_FILE_NAME
EXAMPLES_FILE = DESCRIPTION_DIRECTORY + "/" + "{type_name}/" + EXAMPLES_FILE_NAME
PREDEFINED_FILE = DESCRIPTION_DIRECTORY + "/" + "{type_name}/" + PREDEFINED_FILE_NAME
EXAMPLES_KEY = "Examples"

class Form:
    def __init__(self, form_text: str):
        self._form = form_text
        self._keys = list(json.loads(self._form).keys())

    # TODO: Maybe we should apply a more detailed check just to be sure
    def FormatCheck(self, data_to_check: dict) -> bool:
        for key in self._keys:
            if key not in data_to_check:
                return False
        return True

    def __str__(self):
        return self._form

class Generator:
    __json_pattern = regex.compile(r'\{(?:[^{}]|(?R))*\}')

    def __init__(self, type_name: str):
        self._type_name = type_name
        self._form = Form(open(FORM_FILE.format(type_name=type_name), 'r').read())
        self._template_query_text = open(QUERY_FILE.format(type_name=type_name), 'r').read()
        examples = json.load(open(EXAMPLES_FILE.format(type_name=type_name), 'r'))
        self._examples = []
        for example in examples[EXAMPLES_KEY]:
            self._examples.append(json.dumps(example, indent=4))

    def generate(self, **kwargs) -> (bool, dict):
        query_text = self._template_query_text.replace("{{form}}", str(self._form))
        for (key, value) in kwargs.items():
            query_text = query_text.replace(f"{{{{{key}}}}}", value)
        
        # 0 - Generate without influence
        # 1 - Generate with a single example
        # 2 - Generate with multiple examples
        for i in range(3):
            query_text = self.__update_query_text(query_text, i)
            data = self.__generate(query_text)
            if data != None: return (True, data)

        # 3 - Use predefined
        return (False, json.load(open(PREDEFINED_FILE.format(type_name=self._type_name))))

    def __generate(self, text: str):
        generated_text = connector.complete(text, None)[0]
        json_texts = Generator.__json_pattern.findall(generated_text)
        # Hopefully it only contains one json substring
        for json_text in json_texts:
            json_object = json.loads(json_text)
            if self._form.FormatCheck(json_object):
                return json_object
        return None
    
    def __update_query_text(self, query_text: str, level: int) -> str:
        updated = query_text
        match level:
            case 0:
                pass

            case 1:
                updated += f"\nFor example:\n{self._examples[0]}"
            
            case 2:
                for i in range(1, len(self._examples)):
                    updated += "\n" + self._examples[i]

        return updated