import re


def parse_srt(filename):
    with open(filename, "r", encoding="utf-8-sig") as f:
        content = f.read()

    pattern = re.compile(r"(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.*?)(?=\n\n|\Z)", re.DOTALL)
    subs = []
    for match in pattern.finditer(content):
        index, start, end, text = match.groups()
        lines = text.strip().replace('\n', ' ')
        subs.append({"start": start, "end": end, "text": lines})
    return subs


def segment_scenes(subs, max_pause=4):
    from datetime import datetime

    def parse_time(s):
        return datetime.strptime(s, "%H:%M:%S,%f")

    scenes = []
    current = [subs[0]]

    for prev, curr in zip(subs, subs[1:]):
        delta = (parse_time(curr["start"]) - parse_time(prev["end"])).total_seconds()
        if delta < max_pause:
            current.append(curr)
        else:
            scenes.append(current)
            current = [curr]

    scenes.append(current)
    return scenes
