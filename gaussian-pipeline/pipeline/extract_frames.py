import cv2

from pipeline.logger import info, success


class FrameExtractor:

    def __init__(self, video_path, output_dir, fps):

        self.video_path = str(video_path)
        self.output_dir = output_dir
        self.target_fps = fps

    def extract(self):

        info("Extracting frames...")

        cap = cv2.VideoCapture(self.video_path)

        if not cap.isOpened():
            raise RuntimeError(f"Cannot open {self.video_path}")

        video_fps = cap.get(cv2.CAP_PROP_FPS)

        frame_interval = max(1, round(video_fps / self.target_fps))

        frame_idx = 0
        saved = 0

        while True:

            ret, frame = cap.read()

            if not ret:
                break

            if frame_idx % frame_interval == 0:

                filename = self.output_dir / f"{saved:06d}.png"

                cv2.imwrite(str(filename), frame)

                saved += 1

            frame_idx += 1

        cap.release()

        success(f"Extracted {saved} frames.")