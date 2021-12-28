import os
import re
import types

from setuptools import find_namespace_packages
from setuptools import setup

name = "verox"


def parse_meta():
    with open(os.path.join(name, "_about.py")) as fp:
        code = fp.read()

    token_pattern = re.compile(r"^__(?P<key>\w+)?__\s*=\s*(?P<quote>(?:'{3}|\"{3}|'|\"))(?P<value>.*?)(?P=quote)", re.M)

    groups = {}

    for match in token_pattern.finditer(code):
        group = match.groupdict()
        groups[group["key"]] = group["value"]

    return types.SimpleNamespace(**groups)


def long_description():
    with open("README.md") as fp:
        return fp.read()


def parse_requirements_file(path):
    with open(path) as fp:
        dependencies = (d.strip() for d in fp.read().split("\n") if d.strip())
        return [d for d in dependencies if not d.startswith("#")]


meta = parse_meta()

setup(
    name="verox",
    version=meta.version,
    description="An implementation of IPC using websockets.",
    long_description=long_description(),
    long_description_content_type="text/markdown",
    author=meta.author,
    author_email=meta.email,
    url=meta.url,
    packages=find_namespace_packages(include=[name + "*"]),
    license=meta.license,
    include_package_data=True,
    zip_safe=False,
    install_requires=parse_requirements_file("requirements.txt"),
    python_requires=">=3.8.0,<3.11",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: AsyncIO",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)