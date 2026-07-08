import time


class ZoomOut:

    def __init__(self, uiautomator, logger=None):
        self.ui = uiautomator
        self.logger = logger

    def run(self):

        if self.logger:
            self.logger("Zooming out...")

        stage = self.ui.d(resourceId="com.supercell.clashofclans:id/stage")

        if not stage.exists():
            raise RuntimeError("Stage element not found.")

        for i in range(2):

            if self.logger:
                self.logger(f"Zoom out {i+1}/2")

            stage.pinch_in(percent=50, steps=30)

            time.sleep(0.15)

        if self.logger:
            self.logger("Zoom complete.")