#Developed in 2025 by Luis Fernando Martinelli from Brazil to FP8 AI Studio.
#Developed in JavaScript and converted to Python by Qwen Chat. 
#node_prompt_snippet.py
import re
from typing import Tuple

class PromptSnippetExtractor:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt_list": ("STRING", {
                    "multiline": True,
                    "default": ""
                }),
                "snippet_index": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 999
                }),
                "split_char": ("STRING", {
                    "multiline": False,
                    "default": "---"
                }),
                "first_word_is_filename": ("BOOLEAN", {"default": True}),  # ← renomeado
                "ignore_start_number_label": ("BOOLEAN", {"default": True})
            }
        }

    # ✅ Saídas atualizadas:
    # - prompt: trecho completo (ex: "001_smile_front\nA gentle smile...")
    # - prompt_text: trecho sem primeira palavra (ex: "A gentle smile...")
    # - filename_to_label: versão limpa para UI (ex: "smile front")
    # - filename: primeira palavra original (ex: "001_smile_front")
    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("prompt", "prompt_text", "filename_to_label", "filename")
    FUNCTION = "extract"
    CATEGORY = "prompt/util_pack"
    DISPLAY_NAME = "Prompt Snippet Extractor"
    NODE_ID = "PromptSnippetExtractor"

    def _clean_for_label(self, word: str, ignore_number: bool) -> str:
        """Remove prefixo numérico + _ opcional e converte _ → espaço"""
        if ignore_number:
            # Remove ^\d+[_\-]? apenas no início
            word = re.sub(r"^\d+[_\-]?", "", word)
        return word.replace("_", " ")

    def extract(
        self,
        prompt_list: str,
        snippet_index: int,
        split_char: str,
        first_word_is_filename: bool,
        ignore_start_number_label: bool
    ) -> Tuple[str, str, str, str]:
        """
        Extrai snippet com:
        - filename: primeira palavra original (ex: "001_smile_front")
        - filename_to_label: versão limpa para exibição (ex: "smile front")
        - prompt_text: resto do texto (sem primeira palavra)
        - prompt: trecho completo
        """
        if snippet_index < 0:
            raise ValueError("snippet_index must be >= 0")

        if not prompt_list.strip():
            return ("", "", "", "")

        if not split_char:
            full_snippet = prompt_list.strip()
            prompt_text = full_snippet
            filename_to_label = ""
            filename = ""

            if first_word_is_filename:
                match = re.match(r"^([a-zA-Z0-9_\-]+)", full_snippet)
                if match:
                    first_word = match.group(1)
                    filename = first_word  # ✅ mantém a palavra original
                    filename_to_label = self._clean_for_label(first_word, ignore_start_number_label)
                    prompt_text = re.sub(r"^[a-zA-Z0-9_\-]+[\s\n\t\r]*", "", full_snippet)
            return (full_snippet, prompt_text, filename_to_label, filename)

        # Normalização com &begin&
        normalized = "&begin&" + prompt_list.replace(split_char, split_char + "&begin&")
        normalized = re.sub(r"(&begin&)[\s\n\r]*$", "", normalized)

        # Extração
        pattern = rf"(&begin&)((?:[^&]|&(?!begin&))*)(?={re.escape(split_char)}|$)"
        snippets = re.findall(pattern, normalized, re.DOTALL)

        if not snippets:
            return ("", "", "", "")

        if snippet_index >= len(snippets):
            raise ValueError(f"snippet_index {snippet_index} out of range (0–{len(snippets)-1})")

        full_snippet = snippets[snippet_index][1].strip()
        prompt_text = full_snippet
        filename_to_label = ""
        filename = ""

        if first_word_is_filename:
            match = re.match(r"^([a-zA-Z0-9_\-]+)", full_snippet)
            if match:
                first_word = match.group(1)
                filename = first_word  # ✅ mantém a palavra original (com número)
                filename_to_label = self._clean_for_label(first_word, ignore_start_number_label)
                prompt_text = re.sub(r"^[a-zA-Z0-9_\-]+[\s\n\t\r]*", "", full_snippet)

        return (full_snippet, prompt_text, filename_to_label, filename)