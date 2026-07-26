import json
from pathlib import Path

class Checkpoint:
    def __init__(self, scene_folder):
        self.file = Path(scene_folder)/"status.json"

        if not self.file.exists():
            self.status = {
                "workspace": False,
                "frames": False,
                "colmap": False,
                "training": False,
                "render": False,
            }
            self.save()

        else:
            with open(self.file) as f:
                self.status = json.load(f)

    def save(self):
        with open(self.file, "w") as f:
            json.dump(self.status, f, indent=4)

    def done(self, stage):
        self.status[stage] = True
        self.save()

    def completed(self, stage):
        return self.status[stage]