# 🧪 Neologismen-Experiment

Ein PsychoPy-Experiment zur Untersuchung der Verarbeitung von Neologismen (neuartigen Wörtern).

# 📚 Nutzer:innen-Dokumentation (ohne Programmierkenntnisse)

## ✨ Über das Experiment

Dieses PsychoPy-Experiment untersucht, wie Menschen neue Wörter (Neologismen) lernen und verarbeiten. Die Teilnehmenden sehen Neologismen mit ihren semantischen Definitionen und tippen diese mehrmals ab. Dabei werden verschiedene Leistungsmerkmale automatisch erfasst, um den Lernprozess zu analysieren.

## 🛠️ Installation & Voraussetzungen

1. Laden Sie StandalonePsychoPy herunter:
   
   - Download: https://www.psychopy.org/download.html
   - Wählen Sie die Standalone-Version für Ihr Betriebssystem

2. Laden Sie das Experiment herunter und speichern sie alle Dateien in einem Ordner auf Ihrem Computer

3. Stellen Sie sicher, dass alle Dateien vorhanden sind:
   
   - `texts/instructions.md`
   - `texts/ui.md`
   - `stimuli/words.csv`

## 🚀 Experiment durchführen

1. Starten Sie StandalonePsychoPy
2. Klicken Sie auf "File" → "Open"
3. Wählen Sie die Datei `experiment.py`
4. Klicken Sie auf den grünen `Run`-Button (oder drücken Sie `Strg` + `R`)

## 📊 Experimentablauf

1. Experimenteinstellungen konfigurieren:
   
   - Anzahl der zu testenden Wörter
   - Farbfeedback-Präferenz (ja/nein)

2. Teilnehmerinformationen eingeben:
   
   - Name/ID
   - Alter
   - Geschlecht (m/w/d)

3. Für jedes Wort:
   
   - Definition lesen (erscheint zufällig vor oder nach dem Wort)
   - Wort 5-mal exakt eintippen
   - Feedback zur Genauigkeit erhalten

## 💡 Best Practices für Experimentdurchführung

1. 🧪 Führen Sie eine Testsitzung durch
   
   - Testen Sie den kompletten Ablauf
   - Machen Sie sich mit der Bedienung vertraut

2. 📋 Vor dem Experiment:
   
   - Überprüfen Sie die Stimulusliste (words.csv)
   - Testen Sie das Tastaturlayout
   - Stellen Sie eine störungsfreie Umgebung sicher

3. 💾 Während des Experiments:
   
   - Notieren Sie besondere Vorkommnisse
   - Prüfen Sie regelmäßig die Datenspeicherung

## 📊 Daten & Ergebnisse

Die Ergebnisdateien finden Sie im `data/`-Ordner:

- Format: `YYYY-MM-DD_teilnehmer_name_typ_HHMM.csv`
- Enthält alle Eingaben und Messwerte
- Automatische Sicherung nach jedem Durchgang

---

# 👩‍💻 Entwickler:innen-Dokumentation

## 📁 Projektstruktur

```
neologismen-experiment/
├── experiment.py        # Haupt-Experiment-Skript
├── texts/              # Experiment-Textinhalte
│   ├── instructions.md # Experimentanweisungen
│   └── ui.md          # UI-Textelemente
├── stimuli/
│   └── words.csv      # Stimulusliste
└── data/              # Gespeicherte Experimentdaten
```

## ⚙️ Technische Voraussetzungen

- Python 3.8 oder 3.10

- Erforderliche Pakete:
  
  ```bash
  pip install psychopy pandas
  ```

## 📊 Datenformat

Die CSV-Ausgabedateien enthalten:

- `trial_nummer`: Fortlaufende Nummer des Wortdurchgangs
- `versuch_nummer`: Nummer des Versuchs (1-5) pro Wort
- `zielwort`: Zu tippendes Wort
- `eingabe`: Tatsächliche Eingabe
- `tippgenauigkeit`: Prozentuale Genauigkeit
- `case_correct`: Korrektheit der Groß-/Kleinschreibung
- `reaktionszeit`: Zeit bis zur Bestätigung
- `wortklasse`: Grammatikalische Klasse
- `neuheitswert`: Eingeschätzter Neuheitswert
- `definition_position`: Position der Definition
- `teilnehmer_daten`: Demografische Informationen

## 🛡️ Fehlerbehandlung

Implementierte Sicherheitsfunktionen:

- Automatische Verzeichniserstellung
- Regelmäßige Datensicherung
- Kontrollierte Experimentbeendigung
- Backup-System bei Abstürzen

## 🎨 Visuelle Anpassungen

Anpassbare Parameter in `experiment.py`:

1. Fenstereinstellungen:
   
   ```python
   def _create_window(self):
       return visual.Window(
           size=(1024, 768),
           fullscr=True,
           color='black',
           units='height'
       )
   ```

2. Textstyling:
   
   ```python
   self.stims = {
       'word': visual.TextStim(self.win, height=0.1, color='white'),
       'instruction': visual.TextStim(self.win, height=0.05, wrapWidth=1.5)
   }
   ```

3. Zeitparameter:
   
   ```python
   core.wait(1)  # Feedback-Anzeigedauer
   self.show_text(trial['definition'], 3)  # Definitions-Anzeigedauer
   ```

## 📚 Code-Dokumentation

Der Code enthält:

- Ausführliche Docstrings
- Typ-Annotationen
- Klare Strukturierung
- Umfassende Fehlerbehandlung
- Konsistente Namenskonventionen

## 🤝 Lizenz & Mitwirken

Dieses Projekt steht unter der MIT-Lizenz - siehe [LICENSE](LICENSE) Datei für Details.

Das bedeutet, Sie dürfen:

- ✅ Den Code kommerziell und privat nutzen
- ✅ Den Code modifizieren und anpassen
- ✅ Den Code verteilen
- ✅ Den Code in eigene Projekte einbinden

Die einzige Bedingung ist, dass Sie die Urheberrechtshinweise und die Lizenzerklärung beibehalten.