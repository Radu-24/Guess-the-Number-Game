# Guess the Number Game

A cross-platform number guessing game built with Python and PyQt6.  
Choose your difficulty, get real-time feedback, and track your performance with built-in history and timing features.

---

## Features

- Difficulty selection: Easy (1–50), Medium (1–100), Hard (1–200)
- Stopwatch and real-time clock
- Submit guesses using Enter key or GUI button
- Color-coded feedback (Too low / Too high / Correct)
- Guess history tracking with timestamps and grouping
- Clean dark-themed GUI with responsive layout
- Native Windows `.exe` build with custom icon
- Ubuntu `.deb` package with desktop entry and icon

---

## Installation

### Windows

Download the latest `.exe` from the [Releases page](https://github.com/Radu-24/Guess-the-Number-Game/releases).

No installation required. Just double-click to play.

---

### Linux (.deb)

Download the `.deb` package from the [Releases page](https://github.com/Radu-24/Guess-the-Number-Game/releases), then install:

```bash
sudo dpkg -i guess-the-number-app.deb
```

Launch it from your app menu.

---

## Run from Source

### Requirements

- Python 3.9+
- PyQt6

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the game

```bash
python src/guess.py
```

---

## Build Instructions

### Windows `.exe` using PyInstaller

```bash
pyinstaller --onefile --windowed ^
  --icon=assets\guessthenumber.ico ^
  --name=GuessTheNumber ^
  src\guess.py
```

Output will be in the `dist/` folder.

---

## Project Structure

```
Guess-the-Number-Game/
├── assets/           # Icons (.ico for Windows, .png for Linux)
├── src/              # Source code
├── dist/             # PyInstaller output (.exe)
├── README.md
├── LICENSE
├── requirements.txt
└── .gitignore
```

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Credits

Developed by Radu using Python and Qt 6.
