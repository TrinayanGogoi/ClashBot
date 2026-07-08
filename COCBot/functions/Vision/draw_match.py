import cv2
from pathlib import Path


class DrawMatch:

    def __init__(self, logger=None):
        self.logger = logger

    def run(self, image, result, output="captures/debug_match.png"):

        if not result["found"]:
            return

        x = result["x"]
        y = result["y"]
        w = result["width"]
        h = result["height"]

        cx = result["center_x"]
        cy = result["center_y"]

        confidence = result["confidence"]

        # Green rectangle
        cv2.rectangle(
            image,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2,
        )

        # Red center dot
        cv2.circle(
            image,
            (cx, cy),
            5,
            (0, 0, 255),
            -1,
        )

        # Confidence text
        cv2.putText(
            image,
            f"{confidence:.3f}",
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2,
        )

        Path(output).parent.mkdir(exist_ok=True)

        cv2.imwrite(output, image)

        if self.logger:
            self.logger(f"Debug image saved: {output}")