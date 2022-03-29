from pathlib import Path
from re import T

from .colors import Colors
from .layers import Begin, End, Head, Layer
from .styles import Ball, Box, RightBandedBox, PDFExport
import subprocess


class Architecture:
    def __init__(self, depth_factor: float):
        self.layers_list: list[Layer] = []
        self.depth_factor = depth_factor

    def add(self, layer: Layer):
        self.layers_list.append(layer)

    @property
    def lastname(self):
        return self.layers_list[-1].name

    def generate(self, pathname="file.tex"):
        path = Path(pathname)
        path.parents[0].mkdir(parents=True, exist_ok=True)

        with open(pathname, "w") as f:
            f.write(Head(".").text())
            f.write(Colors().text())
            f.write(Begin().text())

            last_to = "(0,0,0)"
            for idx, c in enumerate(self.layers_list):
                if hasattr(c, "to") and not c.to:
                    c.to = last_to

                f.write(c.text(self.depth_factor, idx))

                last_to = f"({c.name}-east)"

            f.write(End().text())

        Ball().generate()
        RightBandedBox().generate()
        Box().generate()

        PDFExport("to_pdf.sh").export(path)

        process = subprocess.Popen("bash to_pdf.sh main", shell=True)
        process.wait()
        Path("to_pdf.sh").unlink()
