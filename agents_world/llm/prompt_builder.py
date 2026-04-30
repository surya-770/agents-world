import os
import re
from typing import Any

from agents_world.utils.logger import logger

class PromptBuilder:
    """Manages prompt templates and personality modifiers."""
    
    def __init__(self, prompts_dir: str = None):
        if prompts_dir is None:
            self.prompts_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "prompts")
        else:
            self.prompts_dir = prompts_dir
        self._cache: dict[str, str] = {}

    def _load_template(self, template_name: str) -> str:
        if template_name in self._cache:
            return self._cache[template_name]
        
        filepath = os.path.join(self.prompts_dir, f"{template_name}.txt")
        if not os.path.exists(filepath):
            # Create a basic stub if it doesn't exist for now to avoid crashes
            # In a real environment, these would be populated text files.
            logger.warning(f"Template {template_name} not found at {filepath}, creating default stub.")
            return f"Placeholder for {template_name}. Context: {{context}}"
            
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            self._cache[template_name] = content
            return content

    def render(self, template_name: str, **kwargs) -> str:
        """Renders a template with provided kwargs."""
        template = self._load_template(template_name)
        
        # Simple extraction of {key}
        placeholders = re.findall(r'\{([a-zA-Z0-9_]+)\}', template)
        
        for p in placeholders:
            if p not in kwargs:
                raise ValueError(f"Missing placeholder '{p}' for template '{template_name}'")
        
        return template.format(**kwargs)

    def apply_personality(self, base_prompt: str, personality: Any) -> str:
        """Appends personality modifiers to the prompt."""
        modifiers = []
        if personality.aggression > 0.7:
            modifiers.append("Be highly aggressive and accusatory.")
        if personality.passivity > 0.7:
            modifiers.append("Be passive, avoid direct conflict, and go with the flow.")
        if personality.honesty < 0.3:
            modifiers.append("Lie subtly. Introduce misdirection without being obvious.")
        if personality.deception > 0.7:
            modifiers.append("Construct plausible alibis and confidently deflect suspicion.")
        
        if modifiers:
            behavior = "\n\nBehaviour instructions:\n" + "\n".join(f"- {m}" for m in modifiers)
            return base_prompt + behavior
        return base_prompt
