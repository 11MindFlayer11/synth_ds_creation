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
        if self.method=="2dgs":
            command = [
            "python",
            "train.py",
            "--source_path",
            str(self.workspace.dense),
            "--model_path",
            str(self.model_path),
            "--iterations",
            "15000",
            "--checkpoint_iterations",
            "7000",
                    ]
        elif self.method=="3dgs":
            command = [
            "python",
            "train.py",
            "-s", str(self.workspace.dense),
            "-m", str(self.model_path),
            "--disable_viewer"
        ]
        subprocess.run(command,
        cwd=self.repo,
        check=True)

        success(f"{self.method} training complete.")