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

        # Common preprocessing
        self.images = self.workspace / "images"
        self.sparse = self.workspace / "sparse"
        self.dense = self.workspace / "dense"

        # Method-specific
        self.gs3d = self.workspace / "3dgs"
        self.gs2d = self.workspace / "2dgs"

    def prepare(self):

        info(f"Preparing workspace for {self.scene_name}")
        self.workspace.mkdir(parents=True, exist_ok=True)
        for folder in [
            self.images,
            self.sparse,
            self.dense,
            self.gs3d,
            self.gs2d,
        ]:
            folder.mkdir(parents=True, exist_ok=True)

        # Find video
        videos = list(self.dataset.glob("*.mp4"))

        if not videos:
            raise FileNotFoundError(
                f"No .mp4 video found in {self.dataset}"
            )

        if len(videos) > 1:
            raise RuntimeError(
                f"Multiple videos found in {self.dataset}: {videos}"
            )

        source_video = videos[0]

        info(f"Using video: {source_video.name}")

        shutil.copy2(source_video, self.video)

        success("Workspace ready.")