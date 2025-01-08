from typing import Dict, List
import re
import json
from pathlib import Path
from loguru import logger

class TextProcessor:
    def __init__(self, custom_dict_path: str = None):
        self.custom_dict_path = custom_dict_path or Path("config/custom_dictionary.json")
        self.custom_dict: Dict[str, str] = self._load_custom_dictionary()
        self.common_patterns = {
            r'\b(\w+)(\s+)\1\b': r'\1',  # Remove palavras duplicadas
            r'\s+': ' ',  # Remove espaços extras
        }

    def _load_custom_dictionary(self) -> Dict[str, str]:
        """Carrega o dicionário personalizado de correções"""
        try:
            if Path(self.custom_dict_path).exists():
                with open(self.custom_dict_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logger.error(f"Erro ao carregar dicionário personalizado: {e}")
            return {}

    def save_custom_dictionary(self) -> None:
        """Salva o dicionário personalizado em arquivo"""
        Path(self.custom_dict_path).parent.mkdir(parents=True, exist_ok=True)
        with open(self.custom_dict_path, 'w', encoding='utf-8') as f:
            json.dump(self.custom_dict, f, ensure_ascii=False, indent=2)

    def add_correction(self, wrong: str, correct: str) -> None:
        """Adiciona uma nova correção ao dicionário"""
        self.custom_dict[wrong.lower()] = correct
        self.save_custom_dictionary()
        logger.info(f"Adicionada correção: '{wrong}' -> '{correct}'")

    def remove_correction(self, wrong: str) -> None:
        """Remove uma correção do dicionário"""
        if wrong.lower() in self.custom_dict:
            del self.custom_dict[wrong.lower()]
            self.save_custom_dictionary()
            logger.info(f"Removida correção para: '{wrong}'")

    def apply_corrections(self, text: str) -> str:
        """Aplica todas as correções ao texto"""
        # Aplica correções do dicionário personalizado
        words = text.split()
        corrected_words = []
        
        for word in words:
            word_lower = word.lower()
            if word_lower in self.custom_dict:
                # Preserva capitalização original se possível
                if word.isupper():
                    corrected_words.append(self.custom_dict[word_lower].upper())
                elif word[0].isupper():
                    corrected_words.append(self.custom_dict[word_lower].capitalize())
                else:
                    corrected_words.append(self.custom_dict[word_lower])
            else:
                corrected_words.append(word)
        
        text = ' '.join(corrected_words)
        
        # Aplica padrões comuns de correção
        for pattern, replacement in self.common_patterns.items():
            text = re.sub(pattern, replacement, text)
        
        return text.strip()

    def get_statistics(self) -> Dict:
        """Retorna estatísticas sobre as correções aplicadas"""
        return {
            "total_corrections": len(self.custom_dict),
            "corrections": self.custom_dict
        }

    def suggest_corrections(self, text: str) -> List[Dict]:
        """Sugere possíveis correções baseadas em padrões comuns"""
        suggestions = []
        words = text.split()
        
        # Identifica palavras repetidas próximas
        for i in range(len(words) - 1):
            if words[i].lower() == words[i + 1].lower():
                suggestions.append({
                    "type": "repetition",
                    "original": f"{words[i]} {words[i+1]}",
                    "suggestion": words[i]
                })
        
        return suggestions
