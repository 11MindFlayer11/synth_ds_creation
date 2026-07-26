import json
import shutil
from pathlib import Path


def ensure(path):
    Path(path).mkdir(parents=True, exist_ok=True)


def exists(path):
    return Path(path).exists()

def copy(src, dst):
    src = Path(src)
    dst = Path(dst)
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)

def save_json(data, file):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

def load_json(file):
    with open(file) as f:
        return json.load(f)