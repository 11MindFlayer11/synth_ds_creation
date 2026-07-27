import subprocess

from pipeline.config import GRAPHDECO
from pipeline.logger import info, success


class Renderer:

    def __init__(self, workspace):
        self.workspace = workspace

    def render(self):

        info("Rendering scene...")

        model = self.workspace.workspace / "model"

        subprocess.run([
            "python",
            "render.py",
            "-m", str(model)
        ],
        cwd=GRAPHDECO,
        check=True)

        success("Rendering complete.")