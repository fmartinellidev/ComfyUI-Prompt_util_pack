# __init__.py — prompt_utils_pack
from .node_prompt_variables_substitutor import PromptVariableSubstitutor
from .node_prompt_variable_extractor import PromptVariableExtractor
from .node_prompt_snippet import PromptSnippetExtractor
from .node_hidden_prompt import PromptHiddenProcessor  # ← novo nó

NODE_CLASS_MAPPINGS = {
    "PromptVariableSubstitutor": PromptVariableSubstitutor,
    "PromptVariableExtractor": PromptVariableExtractor,
    "PromptSnippetExtractor": PromptSnippetExtractor,
    "PromptHiddenProcessor": PromptHiddenProcessor,  # ← adicionado
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PromptVariableSubstitutor": "Prompt Variable Substitutor",
    "PromptVariableExtractor": "Prompt Variable Extractor",
    "PromptSnippetExtractor": "Prompt Snippet Extractor",
    "PromptHiddenProcessor": "Prompt Hidden Processor",  # ← adicionado
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]