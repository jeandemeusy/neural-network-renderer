import os
from math import sqrt


class Layers:
    def __init__(self, name: str):
        self.hidden_name = name

    @property
    def name(self):
        return self.hidden_name

    def text(self, depth_factor: float = 1.0, idx: int = None):
        return


class Head(Layers):
    def __init__(self, projectpath: str):
        self.path = projectpath
        self.hidden_name = "head"

    def text(self, depth_factor: float = 1.0, idx: int = None):
        pathlayers = os.path.join(self.path, "layers/").replace("\\", "/")
        text = r"""
        \documentclass[border=8pt, multi, tikz]{standalone} 
        \usepackage{import}
        \usepackage{graphicx}
        \usepackage[export]{adjustbox}
        \subimport{LAYERS_PATH}{init}
        \usetikzlibrary{positioning}
        \usetikzlibrary{3d}
        \usepackage{etoolbox}% provides \preto
        """

        return text.replace("LAYERS_PATH", pathlayers)


class Colors(Layers):
    def __init__(self):
        self.hidden_name = "colors"

    def text(self, depth_factor: float = 1.0, idx: int = None):
        return r"""
        \def\ConvColor{rgb:yellow,5;red,2.5;white,5}
        \def\ConvReluColor{rgb:yellow,5;red,5;white,5}
        \def\PoolColor{rgb:red,1;black,0.3}
        \def\UnpoolColor{rgb:blue,2;green,1;black,0.3}
        \def\FcColor{rgb:blue,5;red,2.5;white,5}
        \def\FcReluColor{rgb:blue,5;red,5;white,4}
        \def\SoftmaxColor{rgb:white,2;black,4}   
        \def\DenseColor{rgb:white,2;black,4}   
        \def\SumColor{rgb:blue,5;green,15}
        """


class Begin(Layers):
    def __init__(self):
        self.hidden_name = "begin"

    def text(self, depth_factor: float = 1.0, idx: int = None):
        return r"""
        \newcommand{\copymidarrow}{\tikz \draw[-Stealth,line width=0.8mm,draw={rgb:blue,4;red,1;green,1;black,3}] (-0.3,0) -- ++(0.3,0);}

        \begin{document}
        \begin{tikzpicture}
        \tikzstyle{connection}=[ultra thick,every node/.style={sloped,allow upside down},draw=\edgecolor]
        \tikzstyle{copyconnection}=[ultra thick,every node/.style={sloped,allow upside down},draw={rgb:blue,4;red,1;green,1;black,3},opacity=0.7]
        """


class Input(Layers):
    def __init__(self, pathfile, shape: list[int], to="(0,0,0)", name="temp"):
        self.hidden_name = name
        self.pathfile = pathfile
        self.to = to
        self.width = shape[0]
        self.height = shape[1]

    def text(self, depth_factor: float = 1.0, idx: int = None):
        base_text = r"""
        \node[canvas is zy plane at x=0] (NAME) at TO 
        {\scalebox{-1}[1]{\includegraphics[width=WIDTHem, height=HEIGHTem, frame] {PATHFILE}}};
        """
        base_text = base_text.replace("NAME", self.name)
        base_text = base_text.replace("TO", self.to)
        base_text = base_text.replace("WIDTH", str(self.width / sqrt(3)))
        base_text = base_text.replace("HEIGHT", str(self.height / sqrt(3)))
        base_text = base_text.replace("PATHFILE", self.pathfile)

        return base_text


class Conv(Layers):
    def __init__(
        self,
        shape: list[int],
        s_filter=256,
        n_filter=64,
        name: str = None,
        offset="(0,0,0)",
        to=None,
        opacity=0.9,
        caption=" ",
    ):
        self.hidden_name = name
        self.s_filter = s_filter
        self.n_filter = n_filter
        self.offset = offset
        self.to = to
        self.width = shape[0]
        self.height = shape[1]
        self.depth = shape[2]
        self.opacity = opacity
        self.caption = caption

    def text(self, depth_factor: float = 1.0, idx: int = None):
        base_text = r"""
        \pic[shift={OFFSET}] at TO
        {
            Box={
                name=NAME, caption=CAPTION, xlabel={{N_FILTER, }}, zlabel=S_FILTER, opacity=OPACTIY, fill=\ConvColor, height=HEIGHT, width=WIDTH, depth=DEPTH
            }
        };
        """
        if not self.name:
            self.hidden_name = f"conv_{idx}"

        base_text = base_text.replace("NAME", self.name)
        base_text = base_text.replace("CAPTION", self.caption)
        base_text = base_text.replace("OPACTIY", str(self.opacity))
        base_text = base_text.replace("OFFSET", self.offset)
        base_text = base_text.replace("TO", self.to)
        base_text = base_text.replace("N_FILTER", str(self.n_filter))
        base_text = base_text.replace("S_FILTER", str(self.s_filter))
        base_text = base_text.replace("HEIGHT", str(self.height))
        base_text = base_text.replace("WIDTH", str(self.depth * depth_factor))
        base_text = base_text.replace("DEPTH", str(self.width))

        return base_text


class Spacer(Layers):
    def __init__(self, name: str = None, width: int = 15):
        self.hidden_name = name
        self.width = width
        self.to = None

    def text(self, depth_factor: float = 1.0, idx: int = None):
        base_text = r"""
        \pic at TO
        {
            Box={
                name=NAME,
                caption= ,
                xlabel={{" ","dummy"}},
                zlabel= ,
                fill=\SoftmaxColor,
                opacity=0.0,
                height=0.0,
                width=WIDTH,
                depth=0.0
            }
        };
        \draw [connection]  (NAME-west) -- node {\midarrow} (NAME-east);
        """

        if not self.name:
            self.hidden_name = f"spacer_{idx}"

        base_text = base_text.replace("NAME", self.name)
        base_text = base_text.replace("WIDTH", str(self.width))
        base_text = base_text.replace("TO", self.to)

        return base_text


class ConvConvRelu(Layers):
    def __init__(
        self,
        name,
        s_filer=256,
        n_filer=(64, 64),
        offset="(0,0,0)",
        to=None,
        width=(2, 2),
        height=40,
        depth=40,
        caption=" ",
    ):
        self.hidden_name = name
        self.s_filer = s_filer
        self.n_filer = n_filer
        self.offset = offset
        self.to = to
        self.width = width
        self.height = height
        self.depth = depth
        self.caption = caption

    def text(self, depth_factor: float = 1.0, idx: int = None):
        base_text = r"""
        \pic[shift={OFFSET}] at TO
        {
            RightBandedBox={
                name=NAME,
                caption=CAPTION,
                xlabel={{ N_FILER_0, N_FILER_1 }},
                zlabel=S_FILER,
                fill=\ConvColor,
                bandfill=\ConvReluColor,
                height=HEIGHT,
                width={ WIDTH_0 , WIDTH_1 },
                depth=DEPTH
            }
        };
        """

        if not self.hidden_name:
            self.hidden_name = f"convconv_relu_{idx}"

        base_text = base_text.replace("NAME", self.name)
        base_text = base_text.replace("OFFSET", self.offset)
        base_text = base_text.replace("N_FILER_0", str(self.n_filer[0]))
        base_text = base_text.replace("N_FILER_1", str(self.n_filer[1]))
        base_text = base_text.replace("S_FILER", str(self.s_filer))
        base_text = base_text.replace("TO", self.to)
        base_text = base_text.replace("WIDTH_0", str(self.width[0]))
        base_text = base_text.replace("WIDTH_1", str(self.width[1]))
        base_text = base_text.replace("HEIGHT", str(self.height))
        base_text = base_text.replace("DEPTH", str(self.depth))
        base_text = base_text.replace("CAPTION", str(self.caption))

        return base_text


class Pool(Layers):
    def __init__(
        self,
        shape: list[int],
        name: str = None,
        offset: str = "(0.5,0,0)",
        to=None,
        opacity=0.75,
        caption=" ",
    ):
        self.hidden_name = name
        self.offset = offset
        self.to = to
        self.width = shape[0]
        self.height = shape[1]
        self.depth = shape[2]
        self.caption = caption
        self.opacity = opacity

    def text(self, depth_factor: float = 1.0, idx: int = None):
        base_text = r"""
        \pic[shift={OFFSET}] at TO
        {
            Box={
                name=NAME,
                caption=CAPTION,
                fill=\PoolColor,
                opacity=OPACITY,
                height=HEIGHT,
                width=WIDTH,
                depth=DEPTH
            }
        };
        """

        if not self.name:
            self.hidden_name = f"pool_{idx}"

        base_text = base_text.replace("NAME", self.name)
        base_text = base_text.replace("OFFSET", self.offset)
        base_text = base_text.replace("TO", self.to)
        base_text = base_text.replace("WIDTH", str(self.depth * depth_factor))
        base_text = base_text.replace("HEIGHT", str(self.height))
        base_text = base_text.replace("DEPTH", str(self.width))
        base_text = base_text.replace("CAPTION", str(self.caption))
        base_text = base_text.replace("OPACITY", str(self.opacity))

        return base_text


class UnPool(Layers):
    def __init__(
        self,
        name,
        offset="(0,0,0)",
        to=None,
        width=1,
        height=32,
        depth=32,
        opacity=0.5,
        caption=" ",
    ):
        self.hidden_name = name
        self.offset = offset
        self.to = to
        self.width = width
        self.height = height
        self.depth = depth
        self.caption = caption

    def text(self, depth_factor: float = 1.0, idx: int = None):
        base_text = r"""
        \pic[shift={OFFSET}] at TO
        {
            Box={
                name=NAME,
                caption=CAPTION,
                fill=\UnpoolColor,
                opacity=OPACTIY,
                height=HEIGHT,
                width=WIDTH,
                depth=DEPTH
            }
        };
        """

        if not self.name:
            self.hidden_name = f"unpool_{idx}"

        base_text = base_text.replace("NAME", self.name)
        base_text = base_text.replace("OFFSET", self.offset)
        base_text = base_text.replace("TO", self.to)
        base_text = base_text.replace("WIDTH", str(self.width))
        base_text = base_text.replace("HEIGHT", str(self.height))
        base_text = base_text.replace("DEPTH", str(self.depth))
        base_text = base_text.replace("CAPTION", str(self.caption))
        base_text = base_text.replace("OPACITY", str(self.opacity))

        return base_text


class ConvRes(Layers):
    def __init__(
        self,
        name,
        s_filer=256,
        n_filer=64,
        offset="(0,0,0)",
        to=None,
        width=6,
        height=40,
        depth=40,
        opacity=0.2,
        caption=" ",
    ):
        self.hidden_name = name
        self.s_filer = s_filer
        self.n_filer = n_filer
        self.offset = offset
        self.to = to
        self.width = width
        self.height = height
        self.depth = depth
        self.caption = caption
        self.opacity = opacity

    def text(self, depth_factor: float = 1.0, idx: int = None):
        base_text = r"""
        \pic[shift={OFFSET}] at TO 
        {
            RightBandedBox={
                name=NAME,
                caption=CAPTION,
                xlabel={{ N_FILER, }},
                zlabel=S_FILER,
                fill={rgb:white,1;black,3},
                bandfill={rgb:white,1;black,2},
                opacity=OPACITY,
                height=HEIGHT,
                width=WIDTH,
                depth=DEPTH
            }
        };
        """

        if not self.name:
            self.hidden_name = f"convres_{idx}"

        base_text = base_text.replace("NAME", self.name)
        base_text = base_text.replace("N_FILER", str(self.n_filer))
        base_text = base_text.replace("S_FILER", str(self.s_filer))
        base_text = base_text.replace("OFFSET", self.offset)
        base_text = base_text.replace("TO", self.to)
        base_text = base_text.replace("WIDTH", str(self.width))
        base_text = base_text.replace("HEIGHT", str(self.height))
        base_text = base_text.replace("DEPTH", str(self.depth))
        base_text = base_text.replace("CAPTION", str(self.caption))
        base_text = base_text.replace("OPACITY", str(self.opacity))

        return base_text

    # def conv_softmax(
    #     cls,
    #     name,
    #     s_filer=40,
    #     offset="(0,0,0)",
    #     to=None,
    #     width=1,
    #     height=40,
    #     depth=40,
    #     caption=" ",
    # ):

    #     base_text = r"""
    #     \pic[shift={OFFSET}] at TO
    #     {
    #         Box={
    #             name=NAME,
    #             caption=CAPTION,
    #             zlabel=S_FILER,
    #             fill=\SoftmaxColor,
    #             height=HEIGHT,
    #             width=WIDTH,
    #             depth=DEPTH
    #         }
    #     };
    #     """

    #     base_text = base_text.replace("NAME", name)
    #     base_text = base_text.replace("S_FILER", str(s_filer))
    #     base_text = base_text.replace("OFFSET", offset)
    #     base_text = base_text.replace("TO", to)
    #     base_text = base_text.replace("WIDTH", str(width))
    #     base_text = base_text.replace("HEIGHT", str(height))
    #     base_text = base_text.replace("DEPTH", str(depth))
    #     base_text = base_text.replace("CAPTION", str(caption))

    #     return base_text


class Softmax(Layers):
    def __init__(
        self,
        shape: int,
        s_filer: int = 10,
        name: str = None,
        offset: str = "(0,0,0)",
        to: str = None,
        opacity: float = 1,
        caption: str = " ",
    ):
        self.hidden_name = name
        self.s_filer = s_filer
        self.offset = offset
        self.to = to
        self.width = 1
        self.height = 1
        self.depth = shape
        self.caption = caption
        self.opacity = opacity

    def text(self, depth_factor: float = 1.0, idx: int = None):
        base_text = r"""
        \pic[shift={OFFSET}] at TO
        {
            Box={
                name=NAME,
                caption=CAPTION,
                xlabel={{" ","dummy"}},
                zlabel=S_FILER,
                fill=\SoftmaxColor,
                opacity=OPACITY,
                height=HEIGHT,
                width=WIDTH,
                depth=DEPTH
            }
        };
        """
        if not self.name:
            self.hidden_name = f"softmax_{idx}"

        base_text = base_text.replace("NAME", self.name)
        base_text = base_text.replace("S_FILER", str(self.s_filer))
        base_text = base_text.replace("OFFSET", self.offset)
        base_text = base_text.replace("TO", self.to)
        base_text = base_text.replace("WIDTH", str(self.width))
        base_text = base_text.replace("HEIGHT", str(self.height))
        base_text = base_text.replace("DEPTH", str(self.depth))
        base_text = base_text.replace("OPACITY", str(self.opacity))
        base_text = base_text.replace("CAPTION", str(self.caption))

        return base_text


class Dense(Layers):
    def __init__(
        self,
        shape: int,
        s_filer: int = 10,
        name: str = None,
        offset: str = "(0,0,0)",
        to: str = None,
        opacity: float = 0.9,
        caption: str = " ",
    ):
        self.hidden_name = name
        self.s_filer = s_filer
        self.offset = offset
        self.to = to
        self.width = 1
        self.height = 1
        self.depth = shape
        self.caption = caption
        self.opacity = opacity

    def text(self, depth_factor: float = 1.0, idx: int = None):
        base_text = r"""
        \pic[shift={OFFSET}] at TO
        {
            Box={
                name=NAME,
                caption=CAPTION,
                xlabel={{" ","dummy"}},
                zlabel=S_FILER,
                fill=\DenseColor,
                opacity=OPACITY,
                height=HEIGHT,
                width=WIDTH,
                depth=DEPTH
            }
        };
        """

        if not self.name:
            self.hidden_name = f"dense_{idx}"

        base_text = base_text.replace("NAME", self.name)
        base_text = base_text.replace("S_FILER", str(self.s_filer))
        base_text = base_text.replace("OFFSET", self.offset)
        base_text = base_text.replace("TO", self.to)
        base_text = base_text.replace("WIDTH", str(self.width))
        base_text = base_text.replace("HEIGHT", str(self.height))
        base_text = base_text.replace("DEPTH", str(self.depth))
        base_text = base_text.replace("OPACITY", str(self.opacity))
        base_text = base_text.replace("CAPTION", str(self.caption))

        return base_text

    # @classmethod
    # def sum(
    #     cls,
    #     name: str,
    #     offset: str = "(0,0,0)",
    #     to: str = "(0,0,0)",
    #     radius: float = 2.5,
    #     opacity: float = 0.6,
    # ):
    #     base_text = r"""
    #     \pic[shift={OFFSET}] at TO
    #     {
    #         Ball={
    #             name=NAME,
    #             fill=\SumColor,
    #             opacity=OPACITY,
    #             radius=RADIUS,
    #             logo=$+$
    #         }
    #     };
    #     """

    #     base_text = base_text.replace("NAME", name)
    #     base_text = base_text.replace("OFFSET", offset)
    #     base_text = base_text.replace("TO", to)
    #     base_text = base_text.replace("RADIUS", str(radius))
    #     base_text = base_text.replace("OPACITY", str(opacity))

    #     return base_text

    # @classmethod
    # def skip(cls, of: str, to: str, pos: float = 1.25):
    #     base_text = r"""
    #     \path (OF-southeast) -- (OF-northeast) coordinate[pos=POS] (OF-top);
    #     \path (TO-south)  -- (TO-north) coordinate[pos=POS] (TO-top);
    #     \draw [copyconnection] (OF-northeast) -- node {\copymidarrow}(OF-top) -- node {\copymidarrow}(TO-top) -- node {\copymidarrow}(TO-north);
    #     """

    #     base_text = base_text.replace("OF", of)
    #     base_text = base_text.replace("TO", to)
    #     base_text = base_text.replace("POS", str(pos))

    #     return base_text


class End(Layers):
    def __init__(self):
        self.hidden_name = "end"

    def text(self, depth_factor: float = 1.0, idx: int = None):
        return r"""
        \end{tikzpicture}
        \end{document}
        """

    # @classmethod
    # def block_2ConvPool(
    #     cls,
    #     name,
    #     botton,
    #     top,
    #     s_filer=256,
    #     n_filer=64,
    #     offset="(1,0,0)",
    #     size=(32, 32, 3.5),
    #     opacity=0.5,
    # ):
    #     return [
    #         Layers.conv_conv_relu(
    #             name="ccr_{}".format(name),
    #             s_filer=str(s_filer),
    #             n_filer=(n_filer, n_filer),
    #             offset=offset,
    #             to="({}-east)".format(botton),
    #             width=(size[2], size[2]),
    #             height=size[0],
    #             depth=size[1],
    #         ),
    #         Layers.pool(
    #             name="{}".format(top),
    #             offset="(0,0,0)",
    #             to="(ccr_{}-east)".format(name),
    #             width=1,
    #             height=size[0] - int(size[0] / 4),
    #             depth=size[1] - int(size[0] / 4),
    #             opacity=opacity,
    #         ),
    #         Layers.connection("{}".format(botton), "ccr_{}".format(name)),
    #     ]

    # @classmethod
    # def block_Unconv(
    #     cls,
    #     name,
    #     botton,
    #     top,
    #     s_filer=256,
    #     n_filer=64,
    #     offset="(1,0,0)",
    #     size=(32, 32, 3.5),
    #     opacity=0.5,
    # ):
    #     return [
    #         Layers.unpool(
    #             name="unpool_{}".format(name),
    #             offset=offset,
    #             to="({}-east)".format(botton),
    #             width=1,
    #             height=size[0],
    #             depth=size[1],
    #             opacity=opacity,
    #         ),
    #         Layers.conv_res(
    #             name="ccr_res_{}".format(name),
    #             offset="(0,0,0)",
    #             to="(unpool_{}-east)".format(name),
    #             s_filer=str(s_filer),
    #             n_filer=str(n_filer),
    #             width=size[2],
    #             height=size[0],
    #             depth=size[1],
    #             opacity=opacity,
    #         ),
    #         Layers.conv(
    #             name="ccr_{}".format(name),
    #             offset="(0,0,0)",
    #             to="(ccr_res_{}-east)".format(name),
    #             s_filer=str(s_filer),
    #             n_filer=str(n_filer),
    #             width=size[2],
    #             height=size[0],
    #             depth=size[1],
    #         ),
    #         Layers.conv_res(
    #             name="ccr_res_c_{}".format(name),
    #             offset="(0,0,0)",
    #             to="(ccr_{}-east)".format(name),
    #             s_filer=str(s_filer),
    #             n_filer=str(n_filer),
    #             width=size[2],
    #             height=size[0],
    #             depth=size[1],
    #             opacity=opacity,
    #         ),
    #         Layers.conv(
    #             name="{}".format(top),
    #             offset="(0,0,0)",
    #             to="(ccr_res_c_{}-east)".format(name),
    #             s_filer=str(s_filer),
    #             n_filer=str(n_filer),
    #             width=size[2],
    #             height=size[0],
    #             depth=size[1],
    #         ),
    #         Layers.connection("{}".format(botton), "unpool_{}".format(name)),
    #     ]

    # @classmethod
    # def block_Res(
    #     cls,
    #     num,
    #     name,
    #     botton,
    #     top,
    #     s_filer=256,
    #     n_filer=64,
    #     offset="(0,0,0)",
    #     size=(32, 32, 3.5),
    #     opacity=0.5,
    # ):
    #     lys = []
    #     layers = [*["{}_{}".format(name, i) for i in range(num - 1)], top]
    #     for name in layers:
    #         ly = [
    #             Layers.conv(
    #                 name="{}".format(name),
    #                 offset=offset,
    #                 to="({}-east)".format(botton),
    #                 s_filer=str(s_filer),
    #                 n_filer=str(n_filer),
    #                 width=size[2],
    #                 height=size[0],
    #                 depth=size[1],
    #             ),
    #             Layers.connection("{}".format(botton), "{}".format(name)),
    #         ]
    #         botton = name
    #         lys += ly

    #     lys += [
    #         Layers.skip(of=layers[1], to=layers[-2], pos=1.25),
    #     ]
    #     return lys
