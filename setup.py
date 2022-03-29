import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="neural-network-renderer",
    version="0.1",
    scripts=["bin/neural-network-renderer"],
    author="Jean Demeusy",
    author_email="dev.jdu@gmail.com",
    description="A usefull CNN/DenseNet visualization tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jeandemeusy/neural-network-renderer",
    packages=["neural-network-renderer"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
