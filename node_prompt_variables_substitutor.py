#Developed in 2025 by Luis Fernando Martinelli (http://www.fernandomartinelli.dev.br) from Brazil to FP8 AI Studio.
#Developed in JavaScript and converted to Python by Qwen Chat.
# node_prompt_substitutor.py
import re
from typing import Dict

class PromptVariableSubstitutor:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt_template": ("STRING", {
                    "multiline": True,
                    "default": ""
                }),
                "variables": ("STRING", {
                    "multiline": True,
                    "default": ""
                }),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("prompt", "json_variables")
    FUNCTION = "substitute"
    CATEGORY = "prompt/util_pack"
    DISPLAY_NAME = "Prompt Variables Substitutor"
    NODE_ID = "PromptVariablesSubstitutor"

    def substitute(self, prompt_template: str, variables: str) -> tuple[str, str]:
        """
        Replace @variable in the prompt_template with values in `variables`.
        Variables syntax: key='value', another_key='value with, comma'
        Accepts lines break and apostrophes to group character sequence (via \').
        """
        # Regex robusta: captura key='value', ignorando vírgulas dentro das aspas
        pattern = r"([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*'((?:[^'\\]|\\.)*?)'"
        matches = re.findall(pattern, variables)

        if not matches:
            return ("", "")

        substitutions: Dict[str, str] = {}
        for key, raw_value in matches:
            # Remove escapes: \' → '
            clean_value = raw_value.replace("\\'", "'")
            substitutions[key.lower()] = clean_value

        # Substitui @key (case-insensitive) no prompt
        result = prompt_template
        for key, value in substitutions.items():
            # Regex com @key, case-insensitive
            result = re.sub(rf"@{re.escape(key)}", value, result, flags=re.IGNORECASE)

        # Formata dict como JSON para saída (útil para logging/seeds)
        import json
        variables_json = json.dumps(substitutions, indent=2, ensure_ascii=False)

        return (result, variables_json)