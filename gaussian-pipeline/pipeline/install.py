import os
import subprocess
import torch

from pipeline.logger import info, success, warning, error
from pipeline.config import GRAPHDECO, GRAPHDECO_REPO, GRAPHDECO_COMMIT

class Installer:
    def __init__(self):
        self.runtime = None
        self.gpu_name = None

    def detect_runtime(self):

        if os.path.exists("/kaggle"):
            self.runtime = "Kaggle"
        elif os.path.exists("/content"):
            self.runtime = "Colab"
        else:
            raise RuntimeError("Unsupported runtime. Please use Kaggle or Colab.")

    def detect_gpu(self):
        if not torch.cuda.is_available():
            return ("GPU not available. Please enable GPU in the runtime settings.")
        self.gpu_name = torch.cuda.get_device_name(0)

    def summary(self):
        info("----------------------------------------")
        info(f"Runtime: {self.runtime}")
        info(f"GPU: {self.gpu_name}")
        info("----------------------------------------")

    def install_everything(self):
        info ("Checking Environment...")
        self.detect_runtime()
        self.detect_gpu()   
        self.clone_graphdeco()
        self.checkout_graphdeco()
        self.install_graphdeco_requirements()
        self.compile_submodules()
        self.verify_graphdeco()
        self.verify_ffmpeg()
        self.verify_colmap()
        self.summary()

    def run_command(self, command, cwd=None):

        result = subprocess.run(
            command, cwd=cwd, check=True
        )
        if result.returncode!=0:
            raise RuntimeError(result.stderr)

        return result.stdout.strip()

    def clone_graphdeco(self):
        info("Checking GraphDECO repository...")

        if not GRAPHDECO.exists():
            info("Cloning GraphDECO")
            self.run_command(["git", "clone", GRAPHDECO_REPO, str(GRAPHDECO), "--recursive"])
            success("GraphDECO cloned successfully.")

        else:
            success("Repo already exists")

    def checkout_graphdeco(self):
        info("Checking out GraphDECO commit...")
        self.run_command(["git", "fetch"], cwd=GRAPHDECO)
        self.run_command(["git", "checkout", GRAPHDECO_COMMIT], cwd=GRAPHDECO)
        success("GraphDECO commit checked out successfully.")

    def install_graphdeco_requirements(self):

        info("Installing GraphDECO Python dependencies...")

        packages = [
            "plyfile",
            "tqdm",
            "opencv-python",
            "joblib"
        ]

        self.run_command([
            "pip",
            "install",
            *packages
        ])

        success("Python dependencies installed.")

    def verify_command(self, command):

        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            raise RuntimeError(f"{command[0]} not found.")

        return result.stdout

    def verify_ffmpeg(self):

        info("Checking FFmpeg...")

        output = self.verify_command(["ffmpeg", "-version"])

        version = output.splitlines()[0]

        success(version)

    def verify_colmap(self):

        info("Checking COLMAP...")

        output = self.verify_command(["colmap", "-h"])

        version = output.splitlines()[0]

        success(version)

    def compile_submodules(self):

        info("Compiling GraphDECO CUDA extensions...")

        submodules = [
            "submodules/diff-gaussian-rasterization",
            "submodules/simple-knn",
            "submodules/fused-ssim"
        ]

        for module in submodules:

            info(f"Installing {module}...")

            self.run_command([
                "pip",
                "install",
                module
            ], cwd=GRAPHDECO)

        success("CUDA extensions compiled.")

    def verify_graphdeco(self):

        info("Verifying GraphDECO...")

        self.run_command([
            "python",
            "-c",
            "import gaussian_renderer; print('GraphDECO OK')"
        ], cwd=GRAPHDECO)

        success("GraphDECO verified.")