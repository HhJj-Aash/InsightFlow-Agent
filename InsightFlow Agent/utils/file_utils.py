import os

def ensure_dir(path: str) -> str:
    os.makedirs(path, exist_ok=True)
    return path

def read_prompt(name: str) -> str:
    prompt_path = os.path.join("prompts", f"{name}.txt")
    if not os.path.exists(prompt_path):
        raise FileNotFoundError(f"Prompt file not found: {prompt_path}")
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read().strip()

def save_file(content: str, path: str) -> str:
    ensure_dir(os.path.dirname(path) or ".")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path
