from setuptools import setup
from distutils.core import Extension


setup(
    ext_modules= [
        Extension(
            "subsets._subsets",
            sources=[
                "./subsets/subsets.i",
                "./subsets/BitSet.cpp",
                "./subsets/DenseSet.cpp",
                "./subsets/DenseBox.cpp",
                "./subsets/DenseTernary.cpp",
            ],
            swig_opts=[
                "-c++",
                "-DSWIGWORDSIZE64",  # https://github.com/swig/swig/issues/568
            ],
            include_dirs=[
                "./subsets/",
            ],
            depends=[
                "./subsets/common.hpp",
                "./subsets/hackycpp.hpp",

                "./subsets/Sweep.hpp",
                "./subsets/BitSet.hpp",
                "./subsets/DenseSet.hpp",
                "./subsets/DenseBox.hpp",

                "./subsets/ternary.hpp",
                "./subsets/Sweep3.hpp",
                "./subsets/DenseTernary.hpp",
            ],
            extra_compile_args=["-std=c++2a", "-O3"],
            extra_link_args=["-Wl,-soname,python_subsets.so"],
        ),
    ]
)
