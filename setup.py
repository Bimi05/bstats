import re

from setuptools import setup

with open("bstats/__init__.py") as file:
    version = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", file.read(), re.MULTILINE).group(1)

with open("README.md") as file:
    readme = file.read()


if version.endswith(("a", "b", "rc")):
    try:
        import subprocess

        process = subprocess.Popen(["git", "rev-parse", "--short", "HEAD"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        _out, _err = process.communicate()
        if _out:
            version += "+" + _out.decode("UTF-8").strip()
    except Exception:
        pass

# set it up and install
setup(
    name="bstats",
    version=version,
    author="Bimi05",
    license="MIT",
    url="https://github.com/Bimi05/bstats",
    project_urls={
        "Issues": "https://github.com/Bimi05/bstats/issues"
    },
    description="A fundamental wrapper for the Brawl Stars API covering all endpoints and including many features!",
    long_description=readme,
    long_description_content_type="text/markdown",
    python_requires=">=3.8.0",
    install_requires=["aiohttp>=3.7.0,<3.9", "cachetools>=4.1.0", "requests"],
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Topic :: Games/Entertainment :: Real Time Strategy",
        "Natural Language :: English,"
    ]
)