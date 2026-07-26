from pipeline.workspace import Workspace


class Scene:

    def __init__(self, scene_name):

        self.name = scene_name

        self.workspace = Workspace(scene_name)

    def prepare_workspace(self):

        self.workspace.prepare()