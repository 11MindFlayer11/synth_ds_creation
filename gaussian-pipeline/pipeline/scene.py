from pipeline.workspace import Workspace
from pipeline.extract_frames import FrameExtractor
from pipeline.config import FPS


class Scene:

    def __init__(self, scene_name):

        self.name = scene_name

        self.workspace = Workspace(scene_name)

    def prepare_workspace(self):

        self.workspace.prepare()

    def extract_frames(self):

        extractor = FrameExtractor(
            self.workspace.video,
            self.workspace.images,
            FPS
        )

        extractor.extract()