from setuptools import setup, find_packages

with open("README.md") as f:
    readme = f.read()

with open("LICENSE") as f:
    license = f.read()

setup(
    name="recall-ccooper",
    version="0.0.4",
    description="A reinforcement learning framework.",
    long_description=readme,
    author="Chris Cooper",
    author_email="chris@cooper.info",
    url="https://github.com/C-J-Cooper/recall",
    license=license,
    packages=find_packages(exclude=("tests", "examples"))
)

