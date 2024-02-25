[![Tests](https://github.com/VideojogosLusofona/egrader/actions/workflows/tests.yml/badge.svg)](https://github.com/VideojogosLusofona/egrader/actions/workflows/tests.yml)
[![codecov](https://codecov.io/gh/VideojogosLusofona/egrader/graph/badge.svg?token=US7KSSBSX4)](https://codecov.io/gh/VideojogosLusofona/egrader)
[![PyPI](https://img.shields.io/pypi/v/egrader)](https://pypi.org/project/egrader/)
[![MIT](https://img.shields.io/badge/license-GPLv3-yellowgreen.svg)](https://www.tldrlegal.com/license/gnu-general-public-license-v3-gpl-3)

# EGrader

Auto-grade simple programming exercises.

## How to use

```text
egrader --help
egrader fetch --help
egrader assess --help
egrader report --help
```

## How to install

### From source/GitHub

Install from PyPI:

```text
pip install egrader
```

Or each step at a time:

```text
pip install git+https://github.com/VideojogosLusofona/egrader.git#egg=egrader.
```

### Installing for development and/or improving the package

```text
git clone https://github.com/VideojogosLusofona/egrader.git
cd egrader
python -m venv env
source env/bin/activate
pip install -e .[dev]
```

<!-- On Windows replace `source env/bin/activate` with `. env\Scripts\activate`.-->

## License

[GPL v3](LICENSE)
