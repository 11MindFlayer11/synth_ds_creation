from pipeline.workspace import Workspace
from pipeline.extract_frames import FrameExtractor
from pipeline.config import FPS
from pipeline.colmap import COLMAP
from pipeline.train import GaussianTrainer
from pipeline.render import Renderer

class Scene:

    def __init__(self, scene_name, method):

        self.name = scene_name
        self.method = method

        self.workspace = Workspace(scene_name)

        self.colmap = COLMAP(self.workspace)

        self.trainer = GaussianTrainer(
            self.workspace,
            self.method
        )

        self.renderer = Renderer(
            self.workspace,
            self.method
        )

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

    def train_gaussians(self):
        self.trainer.train()

    def render(self):
        self.renderer.render()