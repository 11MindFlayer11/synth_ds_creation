import subprocess

from pipeline.logger import info, success


class COLMAP:

    def __init__(self, workspace):

        self.workspace = workspace

    def run(self, command):

        subprocess.run(command, check=True)

    def feature_extraction(self):

        info("Running COLMAP feature extraction...")

        database = self.workspace.workspace / "database.db"

        images = self.workspace.images

        self.run([
            "colmap",
            "feature_extractor",
            "--database_path", str(database),
            "--image_path", str(images),
            "--ImageReader.single_camera", "1"
        ])

        success("Feature extraction complete.")