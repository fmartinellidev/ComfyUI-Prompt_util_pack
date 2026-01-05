# node_prompt_extractor.py
#Developed in 2025 by Luis Fernando Martinelli (http://www.fernandomartinelli.dev.br) from Brazil to FP8 AI Studio.
#Developed in JavaScript and converted to Python by Qwen Chat.
import re

class PromptVariableExtractor:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "field_name": ("STRING", {
                    "multiline": False,
                    "default": "",
                    "placeholder": "ex: seed, expression, pose"
                }),
                "variables": ("STRING", {
                    "multiline": True,
                    "default": ""
                }),
                "char_to_space": ("STRING", {
                    "multiline": False,
                    "default": "",
                    "placeholder": "ex: _ ou -"
                }),
                "lowercase": ("BOOLEAN", {"default": False})
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("value",)
    FUNCTION = "extract"
    CATEGORY = "prompt/util_pack"
    DISPLAY_NAME = "Prompt Variable Extractor"
    NODE_ID = "PromptVariableExtractor"

    def extract(
        self,
        field_name: str,
        variables: str,
        char_to_space: str,
        lowercase: bool
    ) -> tuple[str]:
        """
        Extrai valor de key='value', com pós-processamento:
        - remove aspas simples
        - substitui espaços por char_to_space (se fornecido)
        - converte para lowercase (se solicitado)
        Replica exatamente matchVariableValue() do JS.
        """
        if not field_name.strip() or not variables.strip():
            return ("",)

        # Regex idêntica ao JS: (field = 'value'), case-insensitive
        pattern = rf"({re.escape(field_name)}\s*=\s*'((?:[^'\\]|\\.)*?)')"
        match = re.search(pattern, variables, re.IGNORECASE)

        if not match:
            return ("",)

        # Grupo 2 = valor interno (com escapes, sem aspas externas)
        raw_value = match.group(2)
        # Remove todas as aspas simples (como no JS: .replace(/'/g, ""))
        value = raw_value.replace("'", "")

        # Aplica char_to_space: substitui \s (espaço, tab, quebra) pelo caractere
        if char_to_space:
            value = re.sub(r"\s+", char_to_space, value)

        # Converte para lowercase, se solicitado
        if lowercase:
            value = value.lower()

        return (value,)