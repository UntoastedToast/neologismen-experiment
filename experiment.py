"""
Neologismen Experiment

A PsychoPy-based experiment for studying the processing and learning of neologisms
(newly created words) through repeated typing tasks.

Requirements:
    - Python 3.8 or 3.10 or StandalonePsychoPy (https://www.psychopy.org/download.html)
    - psychopy
    - pandas
    - External files:
        - texts/instructions.md: Experiment instructions
        - texts/ui.md: UI text elements
        - stimuli/words.csv: Stimulus words and definitions

Project Structure:
    - data/: Experiment results (created automatically)
    - texts/: Text content in markdown format
    - stimuli/: Stimulus materials
"""

from psychopy import visual, core, event, data, gui
import pandas as pd
import os
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
import random

@dataclass
class ParticipantInfo:
    """
    Data class to store participant information.
    
    Attributes:
        name (str): Participant's name/identifier
        age (str): Participant's age
        gender (str): Participant's gender (m/w/d)
        session_name (str): Session identifier (automatically set to current date)
        word_count (str): Number of words to test ('all' or specific number)
    """
    name: str
    age: str
    gender: str
    session_name: str
    word_count: str

class NeologismenExperiment:
    """
    Main experiment class for studying the processing of neologisms.
    
    This experiment presents participants with novel words (neologisms) and their definitions.
    Participants must type each word exactly as shown, with the definition appearing either
    before or after the word. Each word is presented 5 times to measure learning effects.
    
    The experiment uses external markdown files for all text content:
    - texts/instructions.md: Contains all instruction texts
    - texts/ui.md: Contains UI-related texts (buttons, labels, etc.)
    """
    
    def __init__(self):
        """
        Initialize the experiment by:
        1. Setting up the current date for session management
        2. Loading text content from markdown files
        3. Getting participant information
        4. Loading stimuli
        5. Creating the experiment window
        6. Setting up visual stimuli
        """
        self.current_date = datetime.now().strftime("%Y-%m-%d")
        self._load_texts()
        self.participant_info = self._get_participant_info()
        self.trials = self._load_stimuli()
        self.win = self._create_window()
        self.all_responses = []
        
        # Create all visual stimuli with consistent styling
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
            ),
            'feedback': visual.TextStim(self.win, pos=(0, -0.2), height=0.1, color='white')
        }

    def _load_texts(self):
        """
        Load all text content from markdown files.
        
        This method reads structured markdown files and extracts specific sections
        for use in the experiment. This allows non-technical users to modify
        experiment texts without touching the code.
        """
        def read_md_section(filepath: str, section: str) -> str:
            """Helper function to extract a specific section from a markdown file."""
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            sections = content.split('##')
            for s in sections:
                if section in s:
                    return s.split('\n', 1)[1].strip()
            return ""

        # Load instruction texts in sequence
        self.instructions = []
        instruction_sections = ['Welcome', 'Task Introduction', 'Input Instructions', 
                              'Definition Info', 'Controls', 'Exit Info']
        for section in instruction_sections:
            text = read_md_section('texts/instructions.md', section)
            self.instructions.append(text)
        
        self.thank_you_text = read_md_section('texts/instructions.md', 'Thank You')

        # Load UI texts with hierarchical structure
        self.ui_texts = {
            'Continue Button': read_md_section('texts/ui.md', 'Continue Button'),
            'Dialog Titles': {
                'config': read_md_section('texts/ui.md', 'Experiment Config'),
                'participant': read_md_section('texts/ui.md', 'Participant Info')
            },
            'Dialog Labels': {
                'word_count': read_md_section('texts/ui.md', 'Word Count'),
                'color_feedback': read_md_section('texts/ui.md', 'Color Feedback'),
                'name': read_md_section('texts/ui.md', 'Name'),
                'age': read_md_section('texts/ui.md', 'Age'),
                'gender': read_md_section('texts/ui.md', 'Gender')
            }
        }

    def _get_participant_info(self) -> ParticipantInfo:
        """
        Display dialog boxes to collect participant information.
        
        Shows two sequential dialogs:
        1. Experiment configuration (word count, feedback settings)
        2. Participant demographics (name, age, gender)
        
        Returns:
            ParticipantInfo: Collected participant information
        """
        session_info = {
            self.ui_texts['Dialog Labels']['word_count']: 'all',
            self.ui_texts['Dialog Labels']['color_feedback']: ['Yes', 'No']
        }
        
        if not gui.DlgFromDict(dictionary=session_info, 
                             title=self.ui_texts['Dialog Titles']['config'],
                             order=[self.ui_texts['Dialog Labels']['word_count'], 
                                   self.ui_texts['Dialog Labels']['color_feedback']]).OK:
            core.quit()
            
        self.show_color_feedback = session_info[self.ui_texts['Dialog Labels']['color_feedback']] == 'Yes'

        # Create session directory using current date
        session_dir = os.path.join('data', self.current_date)
        os.makedirs(session_dir, exist_ok=True)
        self.session_dir = session_dir

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
            word_count=session_info[self.ui_texts['Dialog Labels']['word_count']]
        )

    def _load_stimuli(self) -> data.TrialHandler:
        """
        Load and prepare word stimuli for the experiment.
        
        Reads words from CSV, randomizes their order, and optionally limits
        the number of words based on participant settings.
        
        Returns:
            data.TrialHandler: Prepared trial sequence
        """
        stimuli = pd.read_csv('stimuli/words.csv')
        word_list = stimuli.to_dict('records')
        random.shuffle(word_list)
        
        if self.participant_info.word_count != 'all':
            try:
                num_words = int(self.participant_info.word_count)
                word_list = word_list[:num_words] if 0 < num_words <= len(word_list) else word_list
            except ValueError:
                pass  # Use all words if invalid input
        
        return data.TrialHandler(
            [{**word, 'def_position': random.choice(['before', 'after'])}
             for word in word_list],
            nReps=1,
            method='random'
        )

    def _create_window(self) -> visual.Window:
        """
        Create the experiment window with consistent settings.
        
        Returns:
            visual.Window: Configured PsychoPy window
        """
        return visual.Window(
            size=(1024, 768),
            fullscr=True,
            allowGUI=False,
            color='black',
            units='height'
        )

    def save_data(self, aborted: bool = False, intermediate: bool = False):
        """
        Save experiment data to CSV file.
        
        Args:
            aborted (bool): Whether the experiment was aborted
            intermediate (bool): Whether this is an intermediate save
        """
        try:
            timestamp = datetime.now().strftime("%H%M")
            
            save_type = "intermediate" if intermediate else ("aborted" if aborted else "final")
            filename = f'{self.current_date}_participant_{self.participant_info.name}_{save_type}_{timestamp}.csv'
            
            pd.DataFrame(self.all_responses).to_csv(
                os.path.join(self.session_dir, filename), 
                index=False
            )
            
            # Clean up intermediate files on final save
            if not aborted and not intermediate:
                search_pattern = f'{self.current_date}_participant_{self.participant_info.name}_intermediate'
                for file in os.listdir(self.session_dir):
                    if file.startswith(search_pattern):
                        try:
                            os.remove(os.path.join(self.session_dir, file))
                        except Exception:
                            pass
                            
        except Exception as e:
            print(f"Fehler beim Speichern der Daten: {e}")

    def show_text(self, text: str, duration: Optional[float] = None) -> bool:
        """
        Display text on screen with optional duration.
        
        Args:
            text (str): Text to display
            duration (float, optional): Display duration in seconds
        
        Returns:
            bool: False if escaped, True otherwise
        """
        timer = core.CountdownTimer(duration) if duration else None
        continue_visible = True
        blink_timer = core.Clock()
        
        while True:
            if event.getKeys(['escape']):
                return False
                
            if blink_timer.getTime() >= 0.5:
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

    def calculate_typing_accuracy(self, target_word: str, typed_text: str) -> tuple[float, bool]:
        """
        Calculate typing accuracy and case correctness.
        
        Args:
            target_word (str): The word to be typed
            typed_text (str): The participant's input
        
        Returns:
            tuple[float, bool]: (accuracy percentage, case correctness)
        """
        if not target_word or not typed_text:
            return 0.0, False
        if target_word == typed_text:
            return 100.0, True
            
        correct = sum(a == b for a, b in zip(target_word, typed_text))
        accuracy = (correct * 100.0) / max(len(target_word), len(typed_text))
        return round(accuracy, 1), False

    def run_single_input(self, target_word: str) -> tuple[str, dict]:
        """
        Handle a single word input trial.
        
        Displays the target word and handles keyboard input until Enter is pressed.
        
        Args:
            target_word (str): The word to be typed
        
        Returns:
            tuple[str, dict]: (typed text, trial results)
        """
        typed_text = ''
        shift_pressed = False
        input_clock = core.Clock()
        
        while True:
            self.stims['word'].text = target_word
            self.stims['word'].draw()
            
            current_time = input_clock.getTime()
            self.stims['typed'].text = typed_text + ('_' if int(current_time * 2) % 2 else ' ')
            self.stims['typed'].draw()
            self.win.flip()

            if event.getKeys(['escape']):
                return typed_text, {}

            for key, rt in event.getKeys(timeStamped=input_clock):
                if key in ['lshift', 'rshift']:
                    shift_pressed = True
                elif key in ['return', 'num_enter']:
                    accuracy, case_correct = self.calculate_typing_accuracy(target_word, typed_text)
                    
                    self.stims['feedback'].text = typed_text
                    if self.show_color_feedback:
                        self.stims['feedback'].color = (
                            'green' if accuracy >= 90 and case_correct
                            else 'yellow' if accuracy >= 70
                            else 'red'
                        )
                    else:
                        self.stims['feedback'].color = 'white'
                    self.stims['feedback'].draw()
                    self.win.flip()
                    
                    core.wait(1)  # Show feedback
                    
                    return typed_text, {
                        'typed_text': typed_text,
                        'tippgenauigkeit': accuracy,
                        'case_correct': case_correct,
                        'rt': rt
                    }
                elif key == 'backspace':
                    typed_text = typed_text[:-1]
                elif len(key) == 1:
                    typed_text += key.upper() if shift_pressed else key
                    shift_pressed = False

    def run_trial(self, trial: Dict) -> None:
        """
        Run a complete trial including definition and 5 input attempts.
        
        Args:
            trial (Dict): Trial information including word and definition
        
        Returns:
            bool: False if escaped, True otherwise
        """
        if trial['def_position'] == 'before':
            self.show_text(trial['definition'], 3)

        trial_number = len(self.all_responses) // 5 + 1
        
        for attempt in range(1, 6):
            typed_text, result = self.run_single_input(trial['word'])
            if not result:  # Escape was pressed
                return False
                
            self.all_responses.append({
                'trial_nummer': trial_number,
                'versuch_nummer': attempt,
                'zielwort': trial['word'],
                'eingabe': typed_text,
                'tippgenauigkeit': result['tippgenauigkeit'],
                'case_correct': result['case_correct'],
                'reaktionszeit': result['rt'],
                'wortklasse': trial['class'],
                'neuheitswert': trial['newness'],
                'definition_position': trial['def_position'],
                'teilnehmer_alter': self.participant_info.age,
                'teilnehmer_geschlecht': self.participant_info.gender,
                'name': self.participant_info.name
            })

        if trial['def_position'] == 'after':
            self.show_text(trial['definition'], 3)
            
        self.save_data(intermediate=True)
        return True

    def run(self):
        """
        Run the complete experiment sequence.
        
        This is the main method that:
        1. Shows instructions
        2. Runs all trials
        3. Saves data
        4. Shows thank you message
        5. Cleans up resources
        """
        try:
            # Show instructions
            for instruction in self.instructions:
                if not self.show_text(instruction):
                    self.save_data(aborted=True)
                    return

            # Run trials
            for trial in self.trials:
                if not self.run_trial(trial):
                    self.save_data(aborted=True)
                    return

            self.save_data()
            
            # Show thank you message
            self.show_text(self.thank_you_text)

        except Exception as e:
            print(f"Fehler während des Experiments: {e}")
            self.save_data(aborted=True)
        
        finally:
            if hasattr(self, 'win'):
                self.win.close()
            core.quit()

if __name__ == '__main__':
    NeologismenExperiment().run()
