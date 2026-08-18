import subprocess
from pathlib import Path
from xml.parsers.expat import model

from pipeline.logger import info, success
from pipeline.config import GRAPHDECO, TWODGS


class GaussianTrainer:

    def __init__(self, workspace, method):

        self.workspace = workspace
        self.method = method

        if method == "3dgs":
            self.repo = GRAPHDECO
            self.model_path = workspace.gs3d / "output"

        elif method == "2dgs":
            self.repo = TWODGS
            self.model_path = workspace.gs2d / "output"

        else:
            raise ValueError(f"Unknown method: {method}")


    def train(self):

        info(f"Starting {self.method} training...")

        self.model_path.mkdir(parents=True, exist_ok=True)

        subprocess.run([
            "python",
            "train.py",
            "-s", str(self.workspace.workspace),
            "-m", str(self.model_path),
            "--disable_viewer"
        ],
        cwd=self.repo,
        check=True)

        success(f"{self.method} training complete.")