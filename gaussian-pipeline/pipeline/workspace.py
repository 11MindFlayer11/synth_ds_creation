from pathlib import Path
import shutil

from pipeline.config import DATASET_ROOT, WORKSPACE
from pipeline.logger import info, success


class Workspace:

    def __init__(self, scene_name):

        self.scene_name = scene_name

        self.dataset = DATASET_ROOT / scene_name

        self.workspace = WORKSPACE / scene_name

        self.video = self.workspace / "video.mp4"

        self.images = self.workspace / "images"

        self.sparse = self.workspace / "sparse"

        self.dense = self.workspace / "dense"

        self.output = self.workspace / "output"

        self.renders = self.workspace / "renders"

    def prepare(self):

        info(f"Preparing workspace for {self.scene_name}")

        self.workspace.mkdir(parents=True, exist_ok=True)

        for folder in [
            self.images,
            self.sparse,
            self.dense,
            self.output,
            self.renders
        ]:
            folder.mkdir(exist_ok=True)

        source_video = self.dataset / "video.mp4"

        if not source_video.exists():
            raise FileNotFoundError(source_video)

        shutil.copy2(source_video, self.video)

        success("Workspace ready.")