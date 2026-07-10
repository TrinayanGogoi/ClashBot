import cv2
from pathlib import Path
import numpy as np

class Vision:
    """
    Wrapper around OpenCV.

    Responsibilities:
        - Load images
        - Template matching
        - Future image processing
    """

    def __init__(self, logger=None):
        self.logger = logger

    def log(self, message):
        if self.logger:
            self.logger(message)

    def load_image(self, image_path):
        """
        Load an image from disk.
        """

        image = cv2.imread(image_path)

        if image is None:
            raise FileNotFoundError(f"Could not load image: {image_path}")

        self.log(f"Loaded image: {image_path}")

        return image
    
    # Only returns the first match found, if any. Use find_all_templates to get all matches.
    # def find_template(self, screenshot, template_path, threshold=0.8):
    #     """
    #     Find a template inside a screenshot.

    #     Returns:
    #         (x, y, confidence) if found
    #         None otherwise
    #     """

    #     # screenshot = self.load_image(screenshot)
    #     template = self.load_image(template_path)

    #     result = cv2.matchTemplate(
    #         screenshot,
    #         template,
    #         cv2.TM_CCOEFF_NORMED,
    #     )

    #     _, confidence, _, location = cv2.minMaxLoc(result)

    #     self.log(f"Match confidence: {confidence:.3f}")

    #     if confidence < threshold:
    #         return {
    #             "found": False
    #         }

    #     x, y = location

    #     height, width = template.shape[:2]

    #     return {
    #         "found": True,
    #         "x": x,
    #         "y": y,
    #         "center_x": x + width // 2,
    #         "center_y": y + height // 2,
    #         "confidence": confidence,
    #         "width": width,
    #         "height": height,
    #     }
    

    # returns all matches found, if any. Use find_template to get only the first match.
    def find_all_templates(
        self,
        screenshot,
        template_path,
        threshold=0.90,
        overlap_threshold=0.30,
    ):
        """
        Returns ALL matches after Non-Maximum Suppression.
        """

        template = self.load_image(template_path)

        h, w = template.shape[:2]

        result = cv2.matchTemplate(
            screenshot,
            template,
            cv2.TM_CCOEFF_NORMED,
        )

        ys, xs = np.where(result >= threshold)

        if len(xs) == 0:
            return []

        boxes = []
        scores = []

        for x, y in zip(xs, ys):

            boxes.append(
                [x, y, w, h]
            )

            scores.append(
                float(result[y, x])
            )

        # ---------------------------------------
        # Non-Maximum Suppression
        # ---------------------------------------

        indices = cv2.dnn.NMSBoxes(
            boxes,
            scores,
            score_threshold=threshold,
            nms_threshold=overlap_threshold,
        )

        matches = []

        if len(indices) == 0:
            return matches

        for i in indices.flatten():

            x, y, w, h = boxes[i]

            matches.append({

                "found": True,

                "x": x,
                "y": y,

                "center_x": x + w // 2,
                "center_y": y + h // 2,

                "width": w,
                "height": h,

                "confidence": scores[i],

            })

        self.log(f"Matches after NMS: {len(matches)}")

        return matches