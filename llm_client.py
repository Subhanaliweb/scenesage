import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import json

PROMPT_TEMPLATE = """You are an expert film analyst. Analyze the following scene from the 1959 science fiction film *Plan 9 from Outer Space*.

The transcript is:
Scene:
\"\"\"
{transcript}
\"\"\"

Please extract the following:
1. A concise factual **summary** of what happens in this scene.
2. The **names of characters** present or mentioned in this scene (use names only from the transcript).
3. The **mood or tone** of the scene (e.g., eerie, suspenseful, campy).
4. Any **cultural references** or relevant genre tropes present in the dialogue or narration.

⚠️ Do not add characters or events not in the transcript. Do not reference unrelated movies like *The Godfather*.

Output format:
{{
  "summary": "...",
  "characters": [...],
  "mood": "...",
  "cultural_refs": [...]
}}
"""

def scene_to_prompt(transcript):
    return PROMPT_TEMPLATE.format(transcript=transcript)

def extract_json(text):
    # Try to find the first complete JSON object using stack-based matching
    brace_stack = []
    start = None

    for i, c in enumerate(text):
        if c == '{':
            if not brace_stack:
                start = i
            brace_stack.append(c)
        elif c == '}':
            if brace_stack:
                brace_stack.pop()
                if not brace_stack and start is not None:
                    try:
                        return json.loads(text[start:i + 1])
                    except json.JSONDecodeError:
                        continue
    raise ValueError("Valid JSON object not found in model output.")

class LocalLLMClient:
    def __init__(self, model_name):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16, device_map="auto")

    def run(self, transcript):
        prompt = scene_to_prompt(transcript)
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)

        with torch.no_grad():
            output = self.model.generate(**inputs, max_new_tokens=512, do_sample=True, temperature=0.3)
        decoded = self.tokenizer.decode(output[0], skip_special_tokens=True)
        return extract_json(decoded)