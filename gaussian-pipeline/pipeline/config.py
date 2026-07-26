from pathlib import Path

# ==========================================================
# ROOTS
# ==========================================================

ROOT = Path("/kaggle/working")

PROJECT_ROOT = ROOT / "synth_ds_creation"

GRAPHDECO = ROOT / "gaussian-splatting"

WORKSPACE = ROOT / "workspace"

# ==========================================================
# DATA
# ==========================================================

DATASET_ROOT = Path("/kaggle/input/datasets/shivanshanand11/scene-001")

OUTPUT_ROOT = Path("/kaggle/working/output")

CHECKPOINT_ROOT = OUTPUT_ROOT / "checkpoints"

# ==========================================================
# PARAMETERS
# ==========================================================

FPS = 2

IMAGE_EXTENSION = ".png"

IMAGE_SIZE = 1600 #specify width height of img

RANDOM_SEED = 42 #initial value given to a random number generator

for folder in [

    WORKSPACE,

    OUTPUT_ROOT,

    CHECKPOINT_ROOT

]:

    folder.mkdir(parents=True, exist_ok=True)




# ==========================================================
# EXTERNAL REPOSITORIES
# ==========================================================

GRAPHDECO_REPO = "https://github.com/graphdeco-inria/gaussian-splatting.git"

# Temporary until we pin a tested commit
GRAPHDECO_COMMIT = "main"