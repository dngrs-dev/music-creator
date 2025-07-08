# Music Creator
![Python Version](https://img.shields.io/badge/python-3.12+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Table of Contents

- [About](#about)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project_structure)
- [Requirements](#requirements)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## About

Python-based toolkit for procedural music generation, sound synthesis, and audio effects. It enables users to algorithmically compose, synthesize, and process music, supporting a variety of instruments and effects.

## Features

- Procedural music composition and automation
- Multiple instrument models (piano, guitar, drums, synths, etc.)
- Audio effects and mixing (reverb, spatial audio, etc.)
- Granular and physical modeling synthesis
- Command-line interface and web backend
- Output to WAV and JSON formats

## Installation

Clone the repository:

```sh
git clone https://github.com/dngrs-dev/music-creator.git
cd music-creator
```

Install dependencies:

```sh
pip install -r requirements.txt
```

## Usage

Generate music from the command line:

```sh
python cli.py [--config example/config_example.json] [--output music/output.wav] [--info music/output_info.json]
```

Run the web backend:

```sh
python web_backend.py
```

## Project Structure

- `cli.py` - Command-line interface
- `web_backend.py` – Web server for music generation
- `music_generator.py` – Core music generation logic
- `composition` – Composition and theory modules
- `effects` – Audio effects and mixing
- `instruments` – Instrument models
- `samples`, `sounds`, `music` – Audio assets and outputs
- `site` – Web frontend

## Requirements

- Python 3.12+
- See `requirements.txt` for Python dependencies.

## Contributing

Contributions are welcome! Please open issues or submit pull requests.

## License

[MIT License](LICENSE)

## Contact

For questions or feedback, open an issue.
