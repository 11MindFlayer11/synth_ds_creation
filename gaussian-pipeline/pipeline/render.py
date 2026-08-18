import subprocess

from pipeline.config import GRAPHDECO, TWODGS
from pipeline.logger import info, success

class Renderer:

    def __init__(self, workspace, method):

        self.workspace = workspace
        self.method = method

        if method == "3dgs":
            self.repo = GRAPHDECO
            self.model = workspace.gs3d / "output"

        elif method == "2dgs":
            self.repo = TWODGS
            self.model = workspace.gs2d / "output"

        else:
            raise ValueError(f"Unknown method: {method}")

    def render(self):

        info(f"Rendering {self.method} scene...")

        subprocess.run([
            "python",
            "render.py",
            "-m", str(self.model)
        ],
        cwd=self.repo,
        check=True)

        success("Rendering complete.")