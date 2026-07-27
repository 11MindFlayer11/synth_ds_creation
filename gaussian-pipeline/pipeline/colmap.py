import subprocess
import os
from pipeline.logger import info, success
from pipeline.config import COLMAP_USE_GPU
import shutil


class COLMAP:

    def __init__(self, workspace):

        self.workspace = workspace

    def run(self, command):

        env = os.environ.copy()

        env["QT_QPA_PLATFORM"] = "offscreen"

        subprocess.run(command, check=True, env=env)

    def feature_extraction(self):

        info("Running COLMAP feature extraction...")

        database = self.workspace.workspace / "database.db"

        images = self.workspace.images

        self.run([
            "colmap",
            "feature_extractor",
            "--database_path", str(database),
            "--image_path", str(images),
            "--ImageReader.single_camera", "1",
            "--SiftExtraction.use_gpu", str(int(COLMAP_USE_GPU))
        ])

        success("Feature extraction complete.")

    def feature_matching(self):

        info("Running COLMAP feature matching...")

        database = self.workspace.workspace / "database.db"

        self.run([
            "colmap",
            "exhaustive_matcher",
            "--database_path", str(database),
            "--SiftMatching.use_gpu", str(int(COLMAP_USE_GPU))
        ])

        success("Feature matching complete.")

    def sparse_reconstruction(self):

        info("Running COLMAP mapper...")

        database = self.workspace.workspace / "database.db"

        images = self.workspace.images

        sparse = self.workspace.sparse

        sparse.mkdir(parents=True, exist_ok=True)

        self.run([
            "colmap",
            "mapper",
            "--database_path", str(database),
            "--image_path", str(images),
            "--output_path", str(sparse)
        ])

        success("Sparse reconstruction complete.")

    def image_undistortion(self):

        info("Running COLMAP image undistortion...")

        self.run([
            "colmap",
            "image_undistorter",
            "--image_path", str(self.workspace.images),
            "--input_path", str(self.workspace.sparse / "0"),
            "--output_path", str(self.workspace.output),
            "--output_type", "COLMAP"
        ])

        sparse = self.workspace.output / "sparse"
        model0 = sparse / "0"

        model0.mkdir(exist_ok=True)

        for file in [
            "cameras.bin",
            "images.bin",
            "points3D.bin"
        ]:
                src = sparse / file
                dst = model0 / file

                if src.exists():
                    shutil.move(src, dst)

        success("Image undistortion complete.")