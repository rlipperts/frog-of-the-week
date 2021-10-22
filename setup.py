import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

test_deps = [
    'pytest',
    'flake8',
    'pylint',
    'mypy',
]
extras = {
    'test': test_deps
}

setuptools.setup(
    name="frog-of-the-week",
    version="0.0.0",
    author="Ruben Lipperts",
    author_email="",
    description="Discord bot that chooses a frog every week and posts about it",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rlipperts/frog-of-the-week",
    package_dir={'': 'src'},
    packages=['frog_of_the_week'],
    package_data={'frog_of_the_week': ['py.typed']},
    tests_require=test_deps,
    extras_require=extras,
    install_requires=[
    ],
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: https://pypi.org/classifiers/",
    ],
    python_requires='~=3.9',
)
