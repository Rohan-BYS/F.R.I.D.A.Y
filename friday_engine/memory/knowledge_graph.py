"""
F.R.I.D.A.Y. Knowledge Graph (Mem0 Standard).
Proactively extracts and stores facts and entities from user interactions.
"""

from typing import Dict, List
import json
import os
from friday_engine.logger import logger

class KnowledgeGraph:
    """
    Maintains a core persona and fact graph (e.g. "User likes Python", "User's name is John").
    This is extracted in the background asynchronously.
    """
    def __init__(self, storage_path: str = "data/knowledge_graph.json"):
        self.storage_path = storage_path
        self.facts: List[Dict[str, str]] = []
        self._load()

    def _load(self):
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    self.facts = json.load(f)
            except json.JSONDecodeError:
                self.facts = []

    def _save(self):
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(self.facts, f, indent=2)

    def extract_and_store(self, user_input: str, llm_engine: 'BaseLLMProvider'):
        """
        In a real implementation, this prompts a small fast LLM (like Flash) 
        to extract facts from the `user_input` and appends them.
        """
        # Placeholder for background fact extraction logic
        # e.g., "Extract facts from: 'I prefer using React over Vue'"
        # -> {"subject": "User", "predicate": "prefers", "object": "React over Vue"}
        logger.info(f"Knowledge Graph analyzed input: {user_input[:20]}...")
        pass

    def get_core_persona(self) -> str:
        """Returns a compiled string of core facts to inject into the System Prompt."""
        if not self.facts:
            return "No persistent facts learned about the user yet."
            
        persona = "Learned Facts about the User:\n"
        for fact in self.facts:
            persona += f"- {fact.get('subject', 'User')} {fact.get('predicate', 'is/does')} {fact.get('object', '')}\n"
        return persona
