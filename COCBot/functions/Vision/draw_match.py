
import cv2
from pathlib import Path


class DrawMatches:

    def __init__(self, logger=None):
        self.logger = logger

    def run(self, image, results, output="captures/debug_matches.png"):

        debug = image.copy()

        for result in results:

            if not result["found"]:
                continue

            x = result["x"]
            y = result["y"]
            w = result["width"]
            h = result["height"]

            cx = result["center_x"]
            cy = result["center_y"]

            confidence = result["confidence"]

            # Green rectangle
            cv2.rectangle(
                debug,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2,
            )

            # Red Center Dot
            cv2.circle(
                debug,
                (cx, cy),
                5,
                (0, 0, 255),
                -1,
            )

            # Confidence Text
            cv2.putText(
                debug,
                f"{confidence:.2f}",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2,
            )

        Path(output).parent.mkdir(exist_ok=True)
        cv2.imwrite(output, debug)

        if self.logger:
            self.logger(f"Debug image saved: {output}")