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

        success(f"Runtime:{self.runtime}")

    def detect_gpu(self):
        if not torch.cuda.is_available():
            raise RuntimeError("GPU not available. Please enable GPU in the runtime settings.")
        self.gpu_name = torch.cuda.get_device_name(0)
        success(f"GPU:{self.gpu_name}")

    def summary(self):
        info("----------------------------------------")
        info(f"Runtime: {self.runtime}")
        info(f"GPU: {self.gpu_name}")
        info("----------------------------------------")

    def install_everything(self):
        info ("Checking Environment...")
        self.detect_runtime()
        self.detect_gpu()   
        self.summary()