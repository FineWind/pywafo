import os
import re
from numpy.distutils.core import setup
from numpy.distutils.misc_util import Configuration

PACKAGE_NAME = 'wafo'
ROOT = os.path.abspath(os.path.dirname(__file__))

def read(file_path):
    """Returns contents of file as a string."""
    with open(file_path, 'r') as fp:
        return fp.read()

def find_version(file_path):
    """Returns version given in the __version__ variable of a module file"""
    version_file = read(file_path)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

def setup_package():
    extra_link_args = ["-static", "-static-libgfortran", "-static-libgcc"] if os.name == 'nt' else []
    config = Configuration(PACKAGE_NAME)

    # Add extensions
    config.add_extension('c_library', sources=['source/c_library/c_library.pyf', 'source/c_library/c_functions.c'])
    config.add_extension('mvn', sources=['source/mvn/mvn.pyf', 'source/mvn/mvndst.f'], extra_link_args=extra_link_args)
    
    # Add mvnprdmod library and extension
    lib_mvnprdmod_src = ['source/mvnprd/mvnprd.f', 'source/mvnprd/mvnprodcorrprb.f']
    config.add_library('_mvnprdmod', sources=lib_mvnprdmod_src)
    config.add_extension('mvnprdmod', sources=['source/mvnprd/mvnprd_interface.f'], libraries=['_mvnprdmod'],
                         depends=(lib_mvnprdmod_src), extra_link_args=extra_link_args)

    # Add other extensions similarly...

    setup(
        version=find_version(os.path.join(ROOT, 'src', PACKAGE_NAME, "__init__.py")),
        **config.todict()
    )

if __name__ == "__main__":
    setup_package()
