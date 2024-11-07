"""Input handling and logging for the Neologismen experiment."""

from typing import List, Dict, Tuple, Any

class InputHandler:
    """Handles keyboard input processing and logging."""
    
    def __init__(self, keylog_data: List[Dict[str, Any]]):
        self.keylog_data = keylog_data
    
    def process_key(self, key: str, rt: float, context: Dict[str, Any]) -> Tuple[str, int, float]:
        """Process a single keypress and update logging data."""
        typed_text = context['typed_text']
        current_pos = context['current_pos']
        last_keypress_time = context['last_keypress_time']
        time_since_last = rt - last_keypress_time
        
        if key == 'backspace' and typed_text and current_pos > 0:
            self._log_keypress(key, True, time_since_last, typed_text, context)
            return typed_text[:-1], current_pos - 1, rt
            
        elif len(key) == 1:
            expected_char = context['target_word'][current_pos].lower() if current_pos < len(context['target_word']) else ''
            is_correct = key.lower() == expected_char.lower()
            self._log_keypress(key, is_correct, time_since_last, typed_text, context)
            return typed_text + key, current_pos + 1, rt
            
        return typed_text, current_pos, last_keypress_time
    
    def _log_keypress(self, key: str, is_correct: bool, time_since_last: float, 
                     typed_text: str, context: Dict[str, Any]) -> None:
        """Log a keypress with its context."""
        self.keylog_data.append({
            'attempt': context['attempt'],
            'word': context['target_word'],
            'definition_position': context['trial']['def_position'],
            'input': typed_text,
            'char': key,
            'correct': is_correct,
            'time': time_since_last,
            'class': context['trial']['class'],
            'newness': context['trial']['newness'],
            'name': context['participant_info'].name,
            'language': context['participant_info'].language,
            'age': context['participant_info'].age
        })
