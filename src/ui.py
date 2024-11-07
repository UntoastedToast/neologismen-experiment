"""UI components and text handling for the Neologismen experiment."""

import os
from typing import Dict, List
from psychopy import visual, gui
from .config import ExperimentConfig, ParticipantInfo

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

class UIManager:
    """Manages UI components and text loading."""
    
    def __init__(self, language: str):
        self.language = language
        self.texts = self._load_texts()
    
    def _load_texts(self) -> Dict[str, str]:
        """Load all text content from markdown files."""
        def read_md_section(filepath: str, section: str) -> str:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            sections = content.split('##')
            for s in sections:
                if section in s:
                    return s.split('\n', 1)[1].strip()
            return ""

        return {
            'continue': read_md_section(f'texts/{self.language}_ui.md', 'Continue Button'),
            'config_title': read_md_section(f'texts/{self.language}_ui.md', 'Experiment Config'),
            'participant_title': read_md_section(f'texts/{self.language}_ui.md', 'Participant Info'),
            'name': read_md_section(f'texts/{self.language}_ui.md', 'Name'),
            'age': read_md_section(f'texts/{self.language}_ui.md', 'Age'),
            'gender': read_md_section(f'texts/{self.language}_ui.md', 'Gender'),
            'word_count': read_md_section(f'texts/{self.language}_ui.md', 'Word Count'),
            'thank_you': read_md_section(f'texts/{self.language}_instructions.md', 'Thank You')
        }
    
    def load_instructions(self, sections: List[str]) -> List[str]:
        """Load instruction sections."""
        return [
            self._read_instruction_section(section)
            for section in sections
        ]
    
    def _read_instruction_section(self, section: str) -> str:
        """Read a specific instruction section."""
        with open(f'texts/{self.language}_instructions.md', 'r', encoding='utf-8') as f:
            content = f.read()
        sections = content.split('##')
        for s in sections:
            if section in s:
                return s.split('\n', 1)[1].strip()
        return ""
    
    def get_available_languages(self) -> List[str]:
        """Get list of available languages from instruction files."""
        return [file.split('_')[0] for file in os.listdir('texts') 
                if file.endswith('_instructions.md')]
    
    def get_experiment_config(self) -> Dict[str, str]:
        """Display combined language and word count selection dialog."""
        config_info = {
            'language': self.get_available_languages(),
            'word_count': 'all'
        }
        dlg = gui.DlgFromDict(dictionary=config_info, title=self.texts['config_title'])
        if not dlg.OK:
            return None
        return config_info
    
    def get_participant_info(self) -> Dict[str, str]:
        """Display dialog to collect participant information."""
        participant_info = {
            self.texts['name']: '',
            self.texts['age']: '',
            self.texts['gender']: ['m', 'w', 'd']
        }
        
        dlg = gui.DlgFromDict(dictionary=participant_info,
                             title=self.texts['participant_title'],
                             order=[self.texts['name'], 
                                   self.texts['age'], 
                                   self.texts['gender']])
        if not dlg.OK:
            return None
        return participant_info
    
    def create_stimuli(self, window: visual.Window) -> Dict[str, visual.TextStim]:
        """Create visual stimuli with consistent settings."""
        return {
            'word': visual.TextStim(window, height=0.1, color='white'),
            'typed': visual.TextStim(window, pos=(0, -0.2), height=0.1, color='white'),
            'instruction': visual.TextStim(window, height=0.05, wrapWidth=1.5, color='white'),
            'continue': visual.TextStim(
                window,
                text=self.texts['continue'],
                pos=(0, -0.4),
                height=0.03,
                color='lightgray'
            )
        }
