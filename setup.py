from setuptools import setup

setup(
    name='compgraph',
    version='0.0.1',
    description='Computational graph builder and parser. Translates to tensorflow.',
    author='CONABIO',
    license='MIT',
    packages=['compgraph', 'tests'],
    install_requires=['lark-parser'],
    zip_safe=False
)
