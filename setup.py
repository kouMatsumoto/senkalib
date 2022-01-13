from setuptools import setup, find_packages
from glob import glob
from os.path import splitext
from os.path import basename


setup(
    name='senkalib',
    version='0.0.1',
    license='mit',
    description='tools for senka',

    author='ca3-caaip',
    author_email='ywakimoto1s@gmail.com',
    url='https://github.com/ca3-caaip/senkalib',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')]
)