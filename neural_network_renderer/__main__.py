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
    Colors.Softmax("rgb:yellow,5;red,5;white,5")

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
    arch.add(Conv(width=8, depths=16, caption="Encoded features", name="encoded"))


    # pre-last layer
    arch.add(Dense(s_filter=32, offset="(3,0,0)", name="flatten"))

    # hidden layer  
    arch.add(Dense(s_filter=32, offset="(3,0,0)", name="hidden"))

    # last layer
    arch.add(Softmax(shape=10, s_filter=5, offset="(3,0,0)", name="output", caption="Output"))


    # lines
    arch.add(DottedLines("encoded", "flatten"))
    arch.add(DottedLines("flatten", "hidden"))
    arch.add(DottedLines("hidden", "output"))

    # output
    arch.to_pdf("output_file")


if __name__ == "__main__":
    main()
