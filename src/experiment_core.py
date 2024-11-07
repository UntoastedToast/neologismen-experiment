"""Core experiment logic for the Neologismen experiment."""

import os
import random
import logging
import pandas as pd
from datetime import datetime
from typing import Dict, Any, Optional, List
from psychopy import core, event, data

from .config import ExperimentConfig, ParticipantInfo
from .ui import WindowFactory, UIManager
from .input_handler import InputHandler

class NeologismenCore:
    """Core experiment implementation."""
    
    def __init__(self, config: Optional[ExperimentConfig] = None):
        """Initialize the experiment with optional configuration."""
        self.config = config or ExperimentConfig()
        self.current_date = datetime.now().strftime("%Y-%m-%d")
        self._setup_logging()
        self._setup_directories()
        
        # UI setup
        self.ui_manager = UIManager('de')  # Default language, will be updated
        exp_config = self._get_experiment_config()
        if not exp_config:
            core.quit()
            
        self.language = exp_config['language']
        self.ui_manager = UIManager(self.language)  # Reinit with selected language
        
        # Load texts and get participant info
        self.instructions = self.ui_manager.load_instructions(self.config.instruction_sections)
        participant_data = self._get_participant_info()
        if not participant_data:
            core.quit()
            
        self.participant_info = self._create_participant_info(participant_data, exp_config)
        
        # Setup window and stimuli
        self.window_factory = WindowFactory()
        self.win = self.window_factory.create_window(self.config)
        self.stims = self.ui_manager.create_stimuli(self.win)
        
        # Setup experiment data
        self.keylog_data: List[Dict[str, Any]] = []
        self.input_handler = InputHandler(self.keylog_data)
        self.trials = self._load_stimuli()

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
    
    def _get_experiment_config(self) -> Optional[Dict[str, str]]:
        """Get experiment configuration from UI."""
        return self.ui_manager.get_experiment_config()
    
    def _get_participant_info(self) -> Optional[Dict[str, str]]:
        """Get participant information from UI."""
        return self.ui_manager.get_participant_info()
    
    def _create_participant_info(self, info: Dict[str, str], 
                               config: Dict[str, str]) -> ParticipantInfo:
        """Create ParticipantInfo instance from collected data."""
        return ParticipantInfo(
            name=info[self.ui_manager.texts['name']],
            age=info[self.ui_manager.texts['age']],
            gender=info[self.ui_manager.texts['gender']],
            session_name=self.current_date,
            word_count=config['word_count'],
            language=config['language']
        )

    def _load_stimuli(self) -> data.TrialHandler:
        """Load and prepare word stimuli for the experiment."""
        stimuli = pd.read_csv(f'stimuli/{self.language}_words.csv')
        word_list = stimuli.to_dict('records')
        random.shuffle(word_list)
        
        if self.participant_info.word_count != 'all':
            try:
                word_list = word_list[:int(self.participant_info.word_count)]
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
            self.show_text(self.ui_manager.texts['thank_you'])
            logging.info("Experiment completed successfully")

        except Exception as e:
            logging.error(f"Error during experiment: {e}")
            self.save_data(aborted=True)
        
        finally:
            if hasattr(self, 'win'):
                self.win.close()
            core.quit()
