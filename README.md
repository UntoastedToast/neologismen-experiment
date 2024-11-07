# 🧪 Neologismen-Experiment

Ein PsychoPy-Experiment zur Untersuchung der Verarbeitung von Neologismen (neuartigen Wörtern) in verschiedenen Sprachen.

# 📚 Nutzer:innen-Dokumentation (ohne Programmierkenntnisse)

## ✨ Über das Experiment

Dieses PsychoPy-Experiment untersucht, wie Menschen neue Wörter (Neologismen) lernen und verarbeiten. Die Teilnehmenden sehen Neologismen mit ihren semantischen Definitionen und tippen diese mehrmals ab. Das Experiment erfasst detaillierte Daten auf Tastendruck-Ebene, um das Tippverhalten genau zu analysieren.

## 🛠️ Installation & Voraussetzungen

1. Laden Sie StandalonePsychoPy herunter:
   
   - Download: https://www.psychopy.org/download.html
   - Wählen Sie die Standalone-Version für Ihr Betriebssystem

2. Laden Sie das Experiment herunter und speichern sie alle Dateien in einem Ordner auf Ihrem Computer

3. Stellen Sie sicher, dass alle Dateien vorhanden sind:
   
   - `texts/de_instructions.md` (Deutsche Anleitungen)
   - `texts/eng_instructions.md` (Englische Anleitungen)
   - `texts/de_ui.md` (Deutsche UI-Texte)
   - `texts/eng_ui.md` (Englische UI-Texte)
   - `stimuli/de_words.csv` (Deutsche Wörter)
   - `stimuli/eng_words.csv` (Englische Wörter)

### 📝 Anpassen der Experiment-Texte

Die Texte des Experiments können Sie in den Markdown-Dateien im `texts/`-Ordner anpassen. Für jede unterstützte Sprache gibt es separate Dateien:

- `texts/{sprache}_instructions.md`: Enthält alle Experimentanweisungen und Erklärungen
- `texts/{sprache}_ui.md`: Enthält die UI-Textelemente wie Buttons und Beschriftungen

Zum Bearbeiten dieser Dateien benötigen Sie einen Markdown-Editor. Hier einige empfohlene Optionen:

1. **[MarkText](https://www.marktext.cc/)**
   - Benutzerfreundliche Oberfläche
   - Live-Vorschau der Formatierung
   - Verfügbar für Windows, Mac und Linux
2. **[Notepad++]([Downloads | Notepad&#43;&#43;](https://notepad-plus-plus.org/downloads/))**
   - Mit Markdown-Plugin nutzbar
   - Leichtgewichtig und schnell
   - Gute Option für einfache Textbearbeitung
3. **Online-Editor**
   - StackEdit ([stackedit.io]([StackEdit](https://stackedit.io/app#)))
   - Keine Installation notwendig

**Wichtige Hinweise zur Textbearbeitung:**

- Behalten Sie die Markdown-Syntax bei
- Testen Sie die Änderungen vor dem eigentlichen Experiment
- Erstellen Sie Backups der originalen Dateien
- Die Änderungen werden beim nächsten Experimentstart automatisch übernommen

## 🚀 Experiment durchführen

1. Starten Sie StandalonePsychoPy
2. Klicken Sie auf "File" → "Open"
3. Wählen Sie die Datei `experiment.py`
4. Klicken Sie auf den grünen `Run`-Button (oder drücken Sie `Strg` + `R`)

## 📊 Experimentablauf

1. Sprache und Wortanzahl auswählen:
   - Sprache: Deutsch (de) oder Englisch (eng)
   - Anzahl der zu testenden Wörter

2. Teilnehmerinformationen eingeben:
   - Name/ID
   - Alter
   - Geschlecht (m/w/d)

3. Für jedes Wort:
   - Definition lesen (erscheint zufällig vor oder nach dem Wort)
   - Wort 5-mal exakt eintippen

## 📊 Daten & Ergebnisse

Die Ergebnisdateien finden Sie im `data/`-Ordner:

Format: `YYYY-MM-DD/YYYY-MM-DD_participant_name_typ_HHMM.csv`

### Erfasste Daten

#### Versuchsspezifische Daten:
- `attempt`: Nummer des Versuchs (1-5, da jedes Wort 5 Mal getippt wird)
- `word`: Das Zielwort, das abgetippt werden soll
- `definition_position`: Position der Definition ("before"/"after")

#### Eingabedaten:
- `input`: Die aktuelle Gesamteingabe des Benutzers
- `char`: Der einzelne eingegebene Buchstabe (oder "backspace" bei Löschung)
- `correct`: Ob der eingegebene Buchstabe an der richtigen Position korrekt ist
- `time`: Zeit (in Sekunden) für die Eingabe des Buchstabens

#### Wortklassifikation:
- `class`: Klasse des Wortes
  - "blending" (Wortmischungen)
  - "compound" (Zusammensetzungen)
  - "derivation" (Ableitungen)
- `newness`: "new" (neu) oder "old" (etabliert)

#### Teilnehmerdaten:
- `name`: Name des Teilnehmers
- `language`: Gewählte Sprache
- `age`: Alter des Teilnehmers

Diese Daten ermöglichen Analysen von:
- Tippgeschwindigkeit pro Buchstabe
- Fehlermustern auf Buchstabenebene
- Korrekturen während des Tippens
- Zeitlichen Mustern im Tippverhalten

---

# 👩‍💻 Entwickler:innen-Dokumentation

## 📁 Projektstruktur

```
neologismen-experiment/
├── experiment.py            # Haupt-Experiment-Skript (Einstiegspunkt)
├── src/                    # Quellcode-Module
│   ├── config.py          # Konfigurationsklassen
│   ├── input_handler.py   # Eingabebehandlung und Logging
│   ├── ui.py             # UI-Komponenten und Text-Handling
│   └── experiment_core.py # Hauptexperimentlogik
├── texts/                  # Experiment-Textinhalte
│   ├── de_instructions.md  # Deutsche Experimentanweisungen
│   ├── eng_instructions.md # Englische Experimentanweisungen
│   ├── de_ui.md           # Deutsche UI-Textelemente
│   └── eng_ui.md          # Englische UI-Textelemente
├── stimuli/                # Stimulus-Dateien
│   ├── de_words.csv       # Deutsche Stimulusliste
│   └── eng_words.csv      # Englische Stimulusliste
└── data/                   # Gespeicherte Experimentdaten
    └── YYYY-MM-DD/        # Datumsspezifische Ergebnisse
```

## ⚙️ Technische Voraussetzungen

- Python 3.8 oder 3.10
- Erforderliche Pakete:
  ```bash
  pip install psychopy pandas
  ```

## 🔧 Code-Organisation

Der Code ist in logische Module aufgeteilt:

- `experiment.py`: Schlanker Einstiegspunkt zum Starten des Experiments
- `src/config.py`: Konfigurationsklassen für Experiment- und Teilnehmereinstellungen
- `src/input_handler.py`: Verarbeitung und Logging von Tastatureingaben
- `src/ui.py`: UI-Komponenten, Fenster-Management und Text-Handling
- `src/experiment_core.py`: Hauptexperimentlogik und Ablaufsteuerung

Diese modulare Struktur macht den Code:
- Übersichtlicher und leichter zu warten
- Besser testbar durch klare Trennung der Verantwortlichkeiten
- Einfacher zu erweitern durch lose Kopplung der Komponenten

## 🛡️ Fehlerbehandlung

Implementierte Sicherheitsfunktionen:
- Automatische Verzeichniserstellung
- Kontrollierte Experimentbeendigung
- Datensicherung bei Abbruch

## 🤝 Lizenz & Mitwirken

Dieses Projekt steht unter der MIT-Lizenz - siehe [LICENSE](LICENSE) Datei für Details.

Das bedeutet, Sie dürfen:
- ✅ Den Code kommerziell und privat nutzen
- ✅ Den Code modifizieren und anpassen
- ✅ Den Code verteilen
- ✅ Den Code in eigene Projekte einbinden

Die einzige Bedingung ist, dass Sie die Urheberrechtshinweise und die Lizenzerklärung beibehalten.
