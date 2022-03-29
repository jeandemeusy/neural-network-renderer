import sys
from pathlib import Path

from network_layer.architecture import Architecture
from network_layer.colors import Colors
from network_layer.layers import (
    Conv,
    ConvConvRelu,
    Dense,
    DottedLines,
    Input,
    Pool,
    Softmax,
    Spacer,
)


def main():
    Colors.Dense("lightgray")
    Colors.Softmax("lightgray")

    arch = Architecture(4 / 32)

    # input
    arch.add(Input("assets/input_def_crop.png", shape=[64, 64]))

    # first layer
    arch.add(ConvConvRelu(s_filter=64, n_filter=[32, 32], to="(5,0,0)"))
    arch.add(Pool([32, 32, 32]))
    arch.add(Spacer(width=20))

    # second layer
    arch.add(ConvConvRelu(s_filter=32, n_filter=[64, 64]))
    arch.add(Pool([16, 16, 64]))

    arch.add(Spacer())

    # third layer
    arch.add(ConvConvRelu(s_filter=16, n_filter=[64, 64]))
    arch.add(Pool([8, 8, 64], name="last_pool"))
    arch.add(Spacer())

    # GPA
    arch.add(Conv(s_filter=8, n_filter=1, name="gpa", caption="GPA"))

    # flatten
    arch.add(Dense(64, name="flatten", offset="(4,0,0)", caption="Hidden Layer"))
    arch.add(Softmax(5, 5, name="output", caption="Output", offset="(4,0,0)"))
    arch.add(DottedLines("gpa", "flatten"))
    arch.add(DottedLines("flatten", "output"))

    arch.generate(f"{Path(sys.argv[0]).stem}.tex")


if __name__ == "__main__":
    main()
