import cv2


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
    