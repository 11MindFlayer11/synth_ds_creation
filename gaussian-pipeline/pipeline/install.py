import os
import subprocess
import torch

from pipeline.logger import info, success, warning, error
from pipeline.config import (
    GRAPHDECO,
    GRAPHDECO_REPO,
    GRAPHDECO_COMMIT,
    ROOT,
    TWODGS,
    TWODGS_REPO,
    TWODGS_COMMIT
)
from pipeline.checkpoint import Checkpoint


class Installer:

    def __init__(self):
        self.runtime = None
        self.gpu_name = None
        self.checkpoint = Checkpoint(ROOT)

    # ============================================================
    # ENVIRONMENT
    # ============================================================

    def detect_runtime(self):
        if os.path.exists("/kaggle"):
            self.runtime = "Kaggle"

        elif os.path.exists("/content"):
            self.runtime = "Colab"

        else:
            raise RuntimeError(
                "Unsupported runtime. Please use Kaggle or Colab."
            )

    def detect_gpu(self):
        if not torch.cuda.is_available():
            raise RuntimeError(
                "GPU not available. Please enable GPU in the runtime settings."
            )

        self.gpu_name = torch.cuda.get_device_name(0)

    def check_environment(self):
        info("Checking environment...")

        self.detect_runtime()
        self.detect_gpu()

        success(f"Runtime: {self.runtime}")
        success(f"GPU: {self.gpu_name}")

    # ============================================================
    # COMMON COLMAP PIPELINE
    # ============================================================

    def install_colmap_pipeline(self):
        """
        Install everything required for the common
        video -> frames -> COLMAP preprocessing pipeline.
        """

        info("========================================")
        info("Installing COLMAP pipeline")
        info("========================================")

        self.install_system_packages()
        self.verify_ffmpeg()
        self.verify_colmap()

        success("COLMAP pipeline ready.")

    def install_system_packages(self):
        info("Installing system packages...")

        self.run_command([
            "apt-get",
            "update"
        ])

        self.run_command([
            "apt-get",
            "install",
            "-y",
            "ffmpeg",
            "colmap"
        ])

        success("System packages installed.")

    def verify_ffmpeg(self):
        info("Checking FFmpeg...")

        output = self.verify_command([
            "ffmpeg",
            "-version"
        ])

        version = output.splitlines()[0]

        success(version)

    def verify_colmap(self):
        info("Checking COLMAP...")

        output = self.verify_command([
            "colmap",
            "-h"
        ])

        version = output.splitlines()[0]

        success(version)

    # ============================================================
    # 3D GAUSSIAN SPLATTING
    # ============================================================

    def install_3dgs(self):
        """
        Install the GraphDECO 3D Gaussian Splatting pipeline.
        """

        info("========================================")
        info("Installing 3DGS")
        info("========================================")

        self.clone_graphdeco()
        self.checkout_graphdeco()
        self.install_graphdeco_requirements()
        self.compile_3dgs_extensions()
        self.verify_graphdeco()

        success("3DGS installation complete.")

    def clone_graphdeco(self):
        info("Checking GraphDECO repository...")

        if not GRAPHDECO.exists():

            info("Cloning GraphDECO...")

            self.run_command([
                "git",
                "clone",
                GRAPHDECO_REPO,
                str(GRAPHDECO),
                "--recursive"
            ])

            success("GraphDECO cloned successfully.")

        else:
            success("GraphDECO repository already exists.")

    def checkout_graphdeco(self):
        info("Checking out GraphDECO commit...")

        self.run_command([
            "git",
            "fetch"
        ], cwd=GRAPHDECO)

        self.run_command([
            "git",
            "checkout",
            GRAPHDECO_COMMIT
        ], cwd=GRAPHDECO)

        success("GraphDECO commit checked out.")

    def install_graphdeco_requirements(self):

        info("Installing 3DGS Python dependencies...")

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

        success("3DGS Python dependencies installed.")

    def compile_3dgs_extensions(self):

        info("Compiling 3DGS CUDA extensions...")

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

        success("3DGS CUDA extensions compiled.")

    def verify_graphdeco(self):

        info("Verifying 3DGS...")

        self.run_command([
            "python",
            "train.py",
            "-h"
        ], cwd=GRAPHDECO)

        success("3DGS verified.")

    # ============================================================
    # 2D GAUSSIAN SPLATTING
    # ============================================================

    def install_2dgs(self):
        """
        Install the 2D Gaussian Splatting pipeline.
        """

        info("========================================")
        info("Installing 2DGS")
        info("========================================")

        self.clone_2dgs()
        self.checkout_2dgs()
        self.install_2dgs_requirements()
        self.compile_2dgs_extensions()
        self.verify_2dgs()

        success("2DGS installation complete.")

    def clone_2dgs(self):
        info("Checking 2DGS repository...")

        if not TWODGS.exists():

            info("Cloning GraphDECO...")

            self.run_command([
                "git",
                "clone",
                TWODGS_REPO,
                str(TWODGS),
                "--recursive"
            ])

            success("2DGS cloned successfully.")

        else:
            success("2DGS repository already exists.")

    def checkout_2dgs(self):
        info("Checking out 2DGS commit...")

        self.run_command([
            "git",
            "fetch"
        ], cwd=TWODGS)

        self.run_command([
            "git",
            "checkout",
            TWODGS_COMMIT
        ], cwd=TWODGS)

        success("2DGS commit checked out.")

    def install_2dgs_requirements(self):

  
        info("Installing 2DGS Python dependencies...")

        packages = [
            "open3d==0.19.0",
            "mediapy==1.1.2",
            "lpips==0.1.4",
            "scikit-image==0.22.0",
            "tqdm==4.66.2",
            "trimesh==4.3.2",
            "plyfile",
            "opencv-python",
        ]

        self.run_command([
            "pip",
            "install",
            *packages
        ])

        success("2DGS Python dependencies installed.")

    def compile_2dgs_extensions(self):

        info("Compiling 2DGS CUDA extensions...")

        os.environ["TORCH_CUDA_ARCH_LIST"] = "7.5"

        submodules = [
            "submodules/diff-surfel-rasterization",
            "submodules/simple-knn"
        ]

        for module in submodules:

            info(f"Installing {module}...")

            self.run_command([
                "pip",
                "install",
                "-v",
                "--no-build-isolation",
                module
            ], cwd=TWODGS)

        success("2DGS CUDA extensions compiled.")

    def verify_2dgs(self):

        info("Verifying 2DGS...")

        self.run_command([
            "python",
            "train.py",
            "-h"
        ], cwd=TWODGS)

        success("2DGS verified.")

    # ============================================================
    # PIPELINE INSTALLATION
    # ============================================================

    def install_pipeline(self, method):
        """
        Install the common COLMAP pipeline and
        the requested reconstruction method.
        """

        self.check_environment()

        # --------------------------------------------------------
        # Stage 1: Common preprocessing
        # --------------------------------------------------------

        self.install_colmap_pipeline()

        # --------------------------------------------------------
        # Stage 2: Reconstruction method
        # --------------------------------------------------------

        methods = {
            "3dgs": self.install_3dgs,
            "2dgs": self.install_2dgs,
        }

        if method not in methods:
            raise ValueError(
                f"Unknown reconstruction method: {method}. "
                f"Available methods: {', '.join(methods.keys())}"
            )

        methods[method]()

        # --------------------------------------------------------
        # Final summary
        # --------------------------------------------------------

        self.summary()

    # ============================================================
    # UTILITIES
    # ============================================================

    def run_command(self, command, cwd=None):

        info(f"Running: {' '.join(command)}")

        result = subprocess.run(
            command,
            cwd=cwd,
            check=True,
            capture_output=True,
            text=True
        )

        return result.stdout.strip()

    def verify_command(self, command):

        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"{command[0]} not found or not working."
            )

        return result.stdout

    def summary(self):

        info("----------------------------------------")
        info(f"Runtime: {self.runtime}")
        info(f"GPU: {self.gpu_name}")
        info("----------------------------------------")