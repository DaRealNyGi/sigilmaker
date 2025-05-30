# SigilMaker

Generate custom sacred-geometry sigils from mantras—via CLI, GUI, or as an importable Python module.

## Features

- Convert any mantra (consonants & digits) into a star-polygon sigil
- 14+ built-in geometry patterns (Seed-of-Life, Golden Spiral, Koch Snowflake, …)
- Composite and randomized overlays
- Radial or upright text placement
- CLI (`sigilmaker-cli`) and GUI (`sigilmaker-gui`) entry points
- Batch processing from text files
- Export to PNG/SVG with embedded mantra metadata
- Custom color palettes via JSON
- Plugin-friendly: drop additional `*.py` in `shapes/`

## Installation

```bash
git clone https://github.com/you/sigilmaker.git
cd sigilmaker
pip install -e .
