# Recall

A reinforcement learning framework.


## Update Test PyPI
```
python3 -m build
python3 -m twine upload --repository testpypi dist/* --skip-existing
```

## Build and Install Locally
```
python3 setup.py install
```
May need to run this inside a virtual environment. 

## Run tests
```
make test
```

## Install dependencies
```
make
```

## Package Structure
```
https://docs.python-guide.org/writing/structure/
https://github.com/navdeep-G/samplemod
```

## Use
```
import recall as rl
```
