from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
import configparser
import os

# Read config file for user's TudatBundle path.
config = configparser.ConfigParser()
config.read("setup.ini")
TUDATBUNDLE_ABSOLUTE_PATH = config["PATHS"]["TudatBundle"]

sourcefiles = [
    "src/cython/lambert_exponential_sinusoid.pyx",
    "src/cpp/lambertExponentialSinusoid.cpp",
]

install_requires = [
    "numpy>=1.15.4",
    "astropy"  # Only required for examples
]

extensions = Extension(
    "lambert_exponential_sinusoid",
    sources=sourcefiles,
    language="c++",
    include_dirs=[
        "src/cython",
        "src/cpp",
        TUDATBUNDLE_ABSOLUTE_PATH,
        os.path.join(TUDATBUNDLE_ABSOLUTE_PATH, "eigen"),
        os.path.join(TUDATBUNDLE_ABSOLUTE_PATH, "tudat"),
    ],
)

setup(
    name="lambert_exponential_sinusoid",
    ext_modules=cythonize(extensions),
    install_requires=install_requires

)
