"""
Neologismen Experiment

A PsychoPy-based experiment for studying the processing and learning of neologisms
(newly created words) through repeated typing tasks.

Requirements:
    - Python 3.8 or 3.10 or StandalonePsychoPy (https://www.psychopy.org/download.html)
    - psychopy
    - pandas
    - External files:
        - texts/{lang}_instructions.md: Experiment instructions
        - texts/{lang}_ui.md: UI text elements
        - stimuli/{lang}_words.csv: Stimulus words and definitions
"""

from __future__ import annotations  # For Python 3.8 compatibility with type hints
from psychopy import visual, core, event, data, gui
import pandas as pd
import os
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Callable, Any, Union
import random
import logging
from abc import ABC, abstractmethod

@dataclass
class ExperimentConfig:
    """Configuration settings for the experiment."""
    window_size: Tuple[int, int] = (1024, 768)
    max_attempts: int = 5
    instruction_sections: List[str] = field(default_factory=lambda: [
        'Welcome', 'Task Introduction', 'Input Instructions',
        'Definition Info', 'Controls', 'Exit Info'
    ])
    definition_display_time: float = 3.0
    blink_interval: float = 0.5

@dataclass
class ParticipantInfo:
    """Data class to store participant information."""
    name: str
    age: str
    gender: str
    session_name: str
    word_count: str
    language: str

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

class WindowFactory:
    """Factory for creating PsychoPy windows with consistent settings."""
    
    @staticmethod
    def create_window(config: ExperimentConfig) -> visual.Window:
        """Create a new window with the specified configuration."""
        return visual.Window(
            size=config.window_size,
            fullscr=True,
            allowGUI=False,
            color='black',
            units='height'
        )

class NeologismenExperiment:
    """Main experiment class implementing the neologism typing task."""
    
    def __init__(self, config: Optional[ExperimentConfig] = None, 
                 window_factory: Optional[WindowFactory] = None) -> None:
        """Initialize the experiment with optional configuration and dependencies."""
        self.config = config or ExperimentConfig()
        self.current_date = datetime.now().strftime("%Y-%m-%d")
        self._setup_logging()
        self._setup_directories()
        
        self.language = self._select_language()
        self._load_texts()
        self.participant_info = self._get_participant_info()
        self.trials = self._load_stimuli()
        
        self.window_factory = window_factory or WindowFactory()
        self.win = self.window_factory.create_window(self.config)
        self.keylog_data: List[Dict[str, Any]] = []
        self.input_handler = InputHandler(self.keylog_data)
        
        self._setup_stimuli()

    def _setup_logging(self) -> None:
        """Configure the logging system."""
        os.makedirs('logs', exist_ok=True)
        logging.basicConfig(
            filename=f'logs/{self.current_date}.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    
    def _setup_directories(self) -> None:
        """Create necessary directories for data storage."""
        self.data_dir = 'data'
        os.makedirs(self.data_dir, exist_ok=True)
        self.session_dir = os.path.join(self.data_dir, self.current_date)
        os.makedirs(self.session_dir, exist_ok=True)
    
    def _setup_stimuli(self) -> None:
        """Initialize visual stimuli with consistent settings."""
        self.stims = {
            'word': visual.TextStim(self.win, height=0.1, color='white'),
            'typed': visual.TextStim(self.win, pos=(0, -0.2), height=0.1, color='white'),
            'instruction': visual.TextStim(self.win, height=0.05, wrapWidth=1.5, color='white'),
            'continue': visual.TextStim(
                self.win,
                text=self.ui_texts['Continue Button'],
                pos=(0, -0.4),
                height=0.03,
                color='lightgray'
            )
        }

    def _select_language(self) -> str:
        """Display language selection dialog and return selected language."""
        available_languages = []
        for file in os.listdir('texts'):
            if file.endswith('_instructions.md'):
                lang = file.split('_')[0]
                available_languages.append(lang)
        
        lang_info = {'language': available_languages}
        dlg = gui.DlgFromDict(dictionary=lang_info, title='Select Language')
        if not dlg.OK:
            core.quit()
        return lang_info['language']

    def _load_texts(self) -> None:
        """Load all text content from markdown files."""
        def read_md_section(filepath: str, section: str) -> str:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            sections = content.split('##')
            for s in sections:
                if section in s:
                    return s.split('\n', 1)[1].strip()
            return ""

        self.instructions = []
        for section in self.config.instruction_sections:
            text = read_md_section(f'texts/{self.language}_instructions.md', section)
            self.instructions.append(text)
        
        self.thank_you_text = read_md_section(f'texts/{self.language}_instructions.md', 'Thank You')

        self.ui_texts = {
            'Continue Button': read_md_section(f'texts/{self.language}_ui.md', 'Continue Button'),
            'Dialog Titles': {
                'config': read_md_section(f'texts/{self.language}_ui.md', 'Experiment Config'),
                'participant': read_md_section(f'texts/{self.language}_ui.md', 'Participant Info')
            },
            'Dialog Labels': {
                'word_count': read_md_section(f'texts/{self.language}_ui.md', 'Word Count'),
                'name': read_md_section(f'texts/{self.language}_ui.md', 'Name'),
                'age': read_md_section(f'texts/{self.language}_ui.md', 'Age'),
                'gender': read_md_section(f'texts/{self.language}_ui.md', 'Gender')
            }
        }

    def _get_participant_info(self) -> ParticipantInfo:
        """Display dialog boxes to collect participant information."""
        session_info = {
            self.ui_texts['Dialog Labels']['word_count']: 'all'
        }
        
        if not gui.DlgFromDict(dictionary=session_info, 
                             title=self.ui_texts['Dialog Titles']['config'],
                             order=[self.ui_texts['Dialog Labels']['word_count']]).OK:
            core.quit()

        participant_info = {
            self.ui_texts['Dialog Labels']['name']: '',
            self.ui_texts['Dialog Labels']['age']: '',
            self.ui_texts['Dialog Labels']['gender']: ['m', 'w', 'd']
        }
        
        if not gui.DlgFromDict(dictionary=participant_info,
                             title=self.ui_texts['Dialog Titles']['participant'],
                             order=[self.ui_texts['Dialog Labels']['name'], 
                                   self.ui_texts['Dialog Labels']['age'], 
                                   self.ui_texts['Dialog Labels']['gender']]).OK:
            core.quit()

        return ParticipantInfo(
            name=participant_info[self.ui_texts['Dialog Labels']['name']],
            age=participant_info[self.ui_texts['Dialog Labels']['age']],
            gender=participant_info[self.ui_texts['Dialog Labels']['gender']],
            session_name=self.current_date,
            word_count=session_info[self.ui_texts['Dialog Labels']['word_count']],
            language=self.language
        )

    def _load_stimuli(self) -> data.TrialHandler:
        """Load and prepare word stimuli for the experiment."""
        stimuli = pd.read_csv(f'stimuli/{self.language}_words.csv')
        word_list = stimuli.to_dict('records')
        random.shuffle(word_list)
        
        if self.participant_info.word_count != 'all':
            try:
                num_words = int(self.participant_info.word_count)
                word_list = word_list[:num_words] if 0 < num_words <= len(word_list) else word_list
            except ValueError:
                logging.warning(f"Invalid word count: {self.participant_info.word_count}")
        
        return data.TrialHandler(
            [{**word, 'def_position': random.choice(['before', 'after'])}
             for word in word_list],
            nReps=1,
            method='random'
        )

    def save_data(self, aborted: bool = False) -> None:
        """Save experiment data to CSV file."""
        try:
            timestamp = datetime.now().strftime("%H%M")
            save_type = "aborted" if aborted else "final"
            filename = f'{self.current_date}_participant_{self.participant_info.name}_{save_type}_{timestamp}.csv'
            
            pd.DataFrame(self.keylog_data).to_csv(
                os.path.join(self.session_dir, filename),
                index=False
            )
            logging.info(f"Data saved successfully to {filename}")
                            
        except Exception as e:
            logging.error(f"Error saving data: {e}")

    def show_text(self, text: str, duration: Optional[float] = None) -> bool:
        """Display text on screen with optional duration."""
        timer = core.CountdownTimer(duration) if duration else None
        continue_visible = True
        blink_timer = core.Clock()
        
        while True:
            if event.getKeys(['escape']):
                return False
                
            if blink_timer.getTime() >= self.config.blink_interval:
                continue_visible = not continue_visible
                blink_timer.reset()
                
            self.stims['instruction'].text = text
            self.stims['instruction'].draw()
            
            if not duration:
                self.stims['continue'].color = 'white' if continue_visible else 'lightgray'
                self.stims['continue'].draw()
                
            self.win.flip()
            
            if timer and timer.getTime() <= 0:
                return True
                
            if not duration and event.getKeys(['space']):
                return True

    def run_single_input(self, target_word: str, attempt: int, trial: Dict[str, Any]) -> bool:
        """Handle a single word input trial with keylogging."""
        typed_text = ''
        current_pos = 0
        input_clock = core.Clock()
        last_keypress_time = input_clock.getTime()
        
        while True:
            self.stims['word'].text = target_word
            self.stims['word'].draw()
            
            current_time = input_clock.getTime()
            self.stims['typed'].text = typed_text + ('_' if int(current_time * 2) % 2 else ' ')
            self.stims['typed'].draw()
            self.win.flip()

            if event.getKeys(['escape']):
                return False

            for key, rt in event.getKeys(timeStamped=input_clock):
                if key in ['return', 'num_enter']:
                    return True
                    
                context = {
                    'typed_text': typed_text,
                    'current_pos': current_pos,
                    'last_keypress_time': last_keypress_time,
                    'target_word': target_word,
                    'trial': trial,
                    'attempt': attempt,
                    'participant_info': self.participant_info
                }
                
                typed_text, current_pos, last_keypress_time = self.input_handler.process_key(
                    key, rt, context
                )

    def run_trial(self, trial: Dict[str, Any]) -> bool:
        """Run a complete trial including definition and input attempts."""
        if trial['def_position'] == 'before':
            self.show_text(trial['definition'], self.config.definition_display_time)

        for attempt in range(1, self.config.max_attempts + 1):
            if not self.run_single_input(trial['word'], attempt, trial):
                return False

        if trial['def_position'] == 'after':
            self.show_text(trial['definition'], self.config.definition_display_time)
            
        return True

    def run(self) -> None:
        """Run the complete experiment sequence."""
        try:
            logging.info(f"Starting experiment for participant: {self.participant_info.name}")
            
            for instruction in self.instructions:
                if not self.show_text(instruction):
                    logging.info("Experiment aborted during instructions")
                    self.save_data(aborted=True)
                    return

            for trial in self.trials:
                if not self.run_trial(trial):
                    logging.info("Experiment aborted during trials")
                    self.save_data(aborted=True)
                    return

            self.save_data()
            self.show_text(self.thank_you_text)
            logging.info("Experiment completed successfully")

        except Exception as e:
            logging.error(f"Error during experiment: {e}")
            self.save_data(aborted=True)
        
        finally:
            if hasattr(self, 'win'):
                self.win.close()
            core.quit()

if __name__ == '__main__':
    NeologismenExperiment().run()
