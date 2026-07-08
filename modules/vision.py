import cv2
from pathlib import Path


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
    
    def find_template(self, screenshot, template_path, threshold=0.8):
        """
        Find a template inside a screenshot.

        Returns:
            (x, y, confidence) if found
            None otherwise
        """

        # screenshot = self.load_image(screenshot)
        template = self.load_image(template_path)

        result = cv2.matchTemplate(
            screenshot,
            template,
            cv2.TM_CCOEFF_NORMED,
        )

        _, confidence, _, location = cv2.minMaxLoc(result)

        self.log(f"Match confidence: {confidence:.3f}")

        if confidence < threshold:
            return {
                "found": False
            }

        x, y = location

        height, width = template.shape[:2]

        return {
            "found": True,
            "x": x,
            "y": y,
            "center_x": x + width // 2,
            "center_y": y + height // 2,
            "confidence": confidence,
            "width": width,
            "height": height,
        }
    
    # def find_orb(
    #     self,
    #     screenshot,
    #     reference_path,
    #     min_matches=20,
    # ):
    #     """
    #     Detect an object using ORB feature matching.
    #     """

    #     reference = self.load_image(reference_path)

    #     orb = cv2.ORB_create(1000)

    #     kp1, des1 = orb.detectAndCompute(reference, None)
    #     kp2, des2 = orb.detectAndCompute(screenshot, None)

    #     self.log(f"Reference keypoints: {len(kp1) if kp1 else 0}")
    #     self.log(f"Screenshot keypoints: {len(kp2) if kp2 else 0}")
    #     if des1 is None or des2 is None:
    #         return {"found": False}

    #     bf = cv2.BFMatcher(cv2.NORM_HAMMING)

        # matches = bf.knnMatch(des1, des2, k=2)

        # good = []

        # for m, n in matches:
        #     if m.distance < 0.75 * n.distance:
        #         good.append(m)

        # self.log(f"ORB matches: {len(good)}")

        # if len(good) < min_matches:
        #     return {"found": False}

        # pts = [kp2[m.trainIdx].pt for m in good]

        # xs = [p[0] for p in pts]
        # ys = [p[1] for p in pts]

        # x1 = int(min(xs))
        # y1 = int(min(ys))
        # x2 = int(max(xs))
        # y2 = int(max(ys))

        # return {
        #     "found": True,
        #     "x": x1,
        #     "y": y1,
        #     "width": x2 - x1,
        #     "height": y2 - y1,
        #     "center_x": (x1 + x2) // 2,
        #     "center_y": (y1 + y2) // 2,
        #     "matches": len(good),
        # }
    