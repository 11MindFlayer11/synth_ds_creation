from pipeline.workspace import Workspace
from pipeline.extract_frames import FrameExtractor
from pipeline.config import FPS
from pipeline.colmap import COLMAP

class Scene:

    def __init__(self, scene_name):

        self.name = scene_name
        
        self.workspace = Workspace(scene_name)
        self.colmap = COLMAP(self.workspace)

    def prepare_workspace(self):

        self.workspace.prepare()

    def extract_frames(self):

        extractor = FrameExtractor(
            self.workspace.video,
            self.workspace.images,
            FPS
        )

        extractor.extract()

    def run_feature_extraction(self):

        self.colmap.feature_extraction()

    def run_feature_matching(self):

        self.colmap.feature_matching()

    def run_sparse_reconstruction(self):

        self.colmap.sparse_reconstruction()

    def run_image_undistortion(self):

        self.colmap.image_undistortion()