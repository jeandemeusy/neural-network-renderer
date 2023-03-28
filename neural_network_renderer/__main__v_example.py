from .architecture import Architecture
from .colors import Colors
from .layers import (
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

    arch = Architecture(8 / 32)

    # input
    arch.add(Input("assets/input.png", shape=[32, 32]))
    # arch.add(Spacer("inputspace"))

    # first layer
    arch.add(Conv(width=32, depths=32, to="(3,0,0)"))
    arch.add(Pool([16, 16, 32]))
    arch.add(Spacer(name="first_layer"))

    # second layer
    arch.add(Conv(width=16, depths=16))
    arch.add(Pool([8, 8, 16]))
    arch.add(Spacer(name="second_layer"))


    # dropout
    arch.add(Conv(width=8, depths=16, caption="Encoded features"))
    arch.add(Spacer(name="dropout"))

    # pre-last layer
    arch.add(Conv(width=8, depths=16))
    arch.add(Pool([16, 16, 16]))
    arch.add(Spacer(name="pre_last_layer"))


    # pre-last layer
    arch.add(Conv(width=16, depths=32))
    arch.add(Pool([32, 32, 32]))



    # output
    arch.add(Input("assets/output.png", shape=[32, 32], to="(29,0,0)"))

    arch.to_pdf("output_file")


if __name__ == "__main__":
    main()
