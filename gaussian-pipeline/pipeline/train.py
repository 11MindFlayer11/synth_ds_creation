import subprocess
from pathlib import Path

from pipeline.logger import info, success
from pipeline.config import GRAPHDECO


class GaussianTrainer:

    def __init__(self, workspace):

        self.workspace = workspace

    def train(self):

        info("Starting Gaussian Splatting training...")

        model_path = self.workspace.workspace / "model"

        model_path.mkdir(exist_ok=True)

        subprocess.run([
            "python",
            "train.py",
            "-s", str(self.workspace.output),
            "-m", str(model_path),
            "--disable_viewer"
        ],
        cwd=GRAPHDECO,
        check=True)

        success("Training complete.")