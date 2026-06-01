from setuptools import setup, find_packages

try:
    with open("SIMULATION_PROOF.md", encoding="utf-8") as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = (
        "A recreational math library that bootstraps all algebraic operations "
        "from a single primitive: eml(x, y) = e^x − ln(y)."
    )

setup(
    name="pythoneml",
    version="2.0.0",
    author="Esoteric Math Enthusiast",
    description=(
        "A recreational math library bootstrapping all algebraic operations "
        "from a single primitive: eml(x, y) = e^x − ln(y)"
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/pythoneml",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    python_requires=">=3.8",
)
