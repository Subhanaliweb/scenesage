import argparse
import json
from tqdm import tqdm
from utils import parse_srt, segment_scenes
from llm_client import LocalLLMClient


def analyze_scene(client, scene):
    transcript = ' '.join([line['text'] for line in scene])
    start_time = scene[0]['start']
    end_time = scene[-1]['end']

    try:
        result = client.run(transcript)
        return {
            "start": start_time,
            "end": end_time,
            "transcript": transcript,
            "summary": result.get("summary", ""),
            "characters": result.get("characters", []),
            "mood": result.get("mood", ""),
            "cultural_refs": result.get("cultural_refs", [])
        }
    except Exception as e:
        print(f"Error processing scene {start_time}–{end_time}: {e}")
        return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("srt_file", help="Subtitle file in .srt format")
    parser.add_argument("--model", required=True, help="Model name (e.g. HuggingFaceH4/zephyr-7b-beta)")
    parser.add_argument("--output", default="scenes.json", help="Output JSON file")
    args = parser.parse_args()

    subs = parse_srt(args.srt_file)
    scenes = segment_scenes(subs)

    client = LocalLLMClient(args.model)

    results = []
    for scene in tqdm(scenes, desc="Analyzing scenes"):
        annotated = analyze_scene(client, scene)
        if annotated:
            results.append(annotated)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"Saved output to {args.output}")


if __name__ == "__main__":
    main()
