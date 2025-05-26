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
