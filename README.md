# neural-network-renderer

This repository contains everything necessary to generated neural network visualisation.

The code generating the image is writen in Python. This code generates `.tex`file that is directly compiled and deleted once the results are available.

## Example

Here is an example of the code to generate a simple convolutionnal-network representation:

```Python
from pathlib import Path
import sys

from network_layer.architecture import Architecture
from network_layer.layers import Input, Pool, Conv, Softmax, Dense, Spacer


def main():
    arch = Architecture(2 / 32)

    # input
    arch.add(Input("assets/input_def_crop.png", shape=[64, 64]))

    # first layer
    arch.add(Conv([64, 64, 32], s_filter=64, n_filter=32, to="(4,0,0)"))
    arch.add(Conv([62, 62, 32], s_filter=62, n_filter=32))
    arch.add(Pool([31, 31, 32]))

    arch.add(Spacer())

    # second layer
    arch.add(Conv([31, 31, 64], s_filter=31, n_filter=64))
    arch.add(Conv([29, 29, 64], s_filter=29, n_filter=64))
    arch.add(Pool([14, 14, 64]))

    arch.add(Spacer())

    # third layer
    arch.add(Conv([13, 13, 64], s_filter=14, n_filter=64))
    arch.add(Conv([12, 12, 64], s_filter=12, n_filter=64))
    arch.add(Pool([6, 6, 64]))

    arch.add(Spacer())

    # flatten
    arch.add(Dense(64, 64))

    # output
    arch.add(Spacer())
    arch.add(Softmax(5, 5))

    arch.generate(f"{Path(sys.argv[0]).stem}.tex")


if __name__ == "__main__":
    main()
```

The rendering is started with this command: 

```sh
bash to_pdf.sh main
```
where `main` is the name of the python file.

**Result:**

![results](./assets/results.png)