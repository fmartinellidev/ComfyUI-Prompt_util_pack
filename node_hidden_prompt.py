# node_hidden_prompt.py
#Developed in 2025 by Luis Fernando Martinelli (http://www.fernandomartinelli.dev.br) from Brazil to FP8 AI Studio.
#Developed in JavaScript and converted to Python by Qwen Chat.
import re
from typing import Tuple

class PromptHiddenProcessor:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {
                    "multiline": True,
                    "default": "A portrait of [[smile;neutral;laugh]], soft lighting, studio background"
                }),
                "input_index_split": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 99,
                    "step": 1
                }),
                "delimiter_pair": (["[[ ]]", "## ##"], {
                    "default": "[[ ]]"
                })
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("input_prompt", "clean_prompt")
    FUNCTION = "process"
    CATEGORY = "prompt/util_pack"
    DISPLAY_NAME = "Prompt Hidden Processor"
    NODE_ID = "PromptHiddenProcessor"

    def process(
        self,
        prompt: str,
        input_index_split: int,
        delimiter_pair: str
    ) -> Tuple[str, str]:
        """
        Processa prompt com trechos ocultos:
        - [[option1;option2;option3]] → substitui por optionN (N = input_index_split)
        - clean_prompt remove todos os trechos ocultos
        Suporta delimitadores: [[ ]] ou ## ##
        """
        if not prompt.strip():
            return ("", "")

        # Define delimitadores com base na escolha
        if delimiter_pair == "[[ ]]":
            start_delim, end_delim = r"\[\[", r"\]\]"
            pattern = r"\[\[([^\]]*?)\]\]"
        else:  # "## ##"
            start_delim, end_delim = r"##", r"##"
            pattern = r"##([^#]*?)##"

        # Regex para encontrar todos os trechos ocultos
        hidden_pattern = re.compile(pattern, re.DOTALL)
        hidden_matches = hidden_pattern.findall(prompt)

        # ✅ clean_prompt: remove todos os trechos ocultos
        clean_prompt = hidden_pattern.sub("", prompt).strip()

        # ✅ input_prompt: substitui trechos ocultos pela variação escolhida
        input_prompt = prompt
        for match in hidden_pattern.finditer(prompt):
            full_match = match.group(0)      # ex: "[[smile;neutral;laugh]]"
            content = match.group(1).strip()  # ex: "smile;neutral;laugh"

            # Divide por ";" e limpa espaços
            options = [opt.strip() for opt in content.split(";") if opt.strip()]
            
            if not options:
                replacement = ""
            elif input_index_split < len(options):
                replacement = options[input_index_split]
            else:
                # Índice fora do range → usa o último
                replacement = options[-1]

            # Substitui no prompt
            input_prompt = input_prompt.replace(full_match, replacement, 1)

        return (input_prompt.strip(), clean_prompt)