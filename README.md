# SceneSage

LLM-powered CLI tool to analyze subtitle files (`.srt`) and extract structured metadata for each scene.

## Features

- Scene segmentation based on pauses ≥ 4s
- Local LLM-based extraction of:
  - Summary
  - Characters
  - Mood
  - Cultural references

## Requirements

- Python 3.8+
- A compatible GPU (optional but recommended for faster inference)
- Hugging Face Transformers-compatible language model (e.g., `HuggingFaceH4/zephyr-7b-beta`)

## Setup

```bash
pip install -r requirements.txt
```

## Usage

```bash
python scenesage.py plan9.srt --model HuggingFaceH4/zephyr-7b-beta --output scenes.json
```

## Arguments

- plan9.srt: The subtitle file you want to analyze (must be in .srt format).

- --model: Name or path of a locally available Hugging Face model compatible with transformers.

- --output: (Optional) Output file path for the results. Defaults to scenes.json.

## Output:

- Segment the .srt file into scenes based on 4-second pauses.

- Use the LLM to extract structured metadata for each scene.

- Save the results in a JSON file like:
 
```
[
  {
    "start": "00:00:01,000",
    "end": "00:00:08,000",
    "transcript": "...",
    "summary": "...",
    "characters": [...],
    "mood": "...",
    "cultural_refs": [...]
  },
  ...
]
```

The file is saved to the path provided via --output, or scenes.json by default.
