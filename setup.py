from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ProjectCodebaseToJsonl',
    version='2025.5.181247',
    author='Eugene Evstafev',
    author_email='chigwel@gmail.com',
    description='A package to convert project codebases into JSONL format for GPT model training.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/chigwell/ProjectCodebaseToJsonl',
    packages=find_packages(),
    install_requires=[
        'pathspec',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
