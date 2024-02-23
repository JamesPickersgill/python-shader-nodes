from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='shader-nodes',
    version='0.1',
    packages=find_packages(),
    install_requires=requirements,
    author='James Pickersgill',
    author_email='james@jorvai.com',
    description='Convert python code to Blender shader node materials',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/JamesPickersgill/python-shader-nodes',
)
