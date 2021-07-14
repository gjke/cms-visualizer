from setuptools import setup, find_packages

setup(
    name='cms_visualizer',
    version='0.1',
    description='Visualize crowd modelling simulations in Jupyter widget.',
    url='https://github.com/gjke/cms-visualizer',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=[
        'ipycanvas',
        'numpy'
    ],
    extras_require={
        'test': ['coverage'],
    },
)
