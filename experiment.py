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

from src.experiment_core import NeologismenCore

if __name__ == '__main__':
    NeologismenCore().run()
