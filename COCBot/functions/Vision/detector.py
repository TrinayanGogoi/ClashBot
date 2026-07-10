from pathlib import Path

class Detector:

    def __init__(self, vision, logger=None):
        self.vision = vision
        self.logger = logger

    def log(self, message):
        if self.logger:
            self.logger(message)

    def find_templates(self, screenshot, folder, threshold):

        matches = []

        templates = sorted(
            Path(folder).glob("*.png")
        )

        self.log(
            f"Searching {len(templates)} templates in {folder}..."
        )

        for template in templates:
            
            # --------------------------------------
            # result = self.vision.find_template(
            #     screenshot,
            #     str(template),
            #     threshold,
            # )

            # if result["found"]:

            #     result["template"] = template.name
            #     matches.append(result)
            #---------------------------------------
            results = self.vision.find_all_templates(
                screenshot,
                str(template),
                threshold,
            )

            for result in results:

                result["template"] = template.name

                matches.append(result)

        return matches