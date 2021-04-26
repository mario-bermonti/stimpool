
# stimpool


[![PyPI - Version](https://img.shields.io/pypi/v/stimpool.svg)](https://pypi.python.org/pypi/stimpool)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/stimpool.svg)](https://pypi.python.org/pypi/stimpool)
![GitHub](https://img.shields.io/github/license/mario-bermonti/stimpool)
[![Tests](https://github.com/mario-bermonti/stimpool/workflows/tests/badge.svg)](https://github.com/mario-bermonti/stimpool/actions?workflow=tests)
[![codecov](https://codecov.io/gh/mario-bermonti/stimpool/branch/master/graph/badge.svg?token=GGADPVQ5G2)](https://codecov.io/gh/mario-bermonti/stimpool)
[![Read the Docs](https://readthedocs.org/projects/stimpool/badge/)](https://stimpool.readthedocs.io/en/latest/)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)


Easily create stimuli pools for cognitive, learning, and psycholinguistics research


* GitHub repo: <https://github.com/mario-bermonti/stimpool.git>
* Documentation: <https://stimpool.readthedocs.io/en/latest/>
* Free software: BSD-3 Clause


## Features

* Easily create Spanish word pools for research
* Specify the characteristics that meet your needs
* Provide your own word pool or use the default one
* Get the cleaned pool or save it to a file

## Getting Started
### Installation
`pip install stimpool`

### Usage
```python
from stimpool.words import WordPool
words = ["gato", "canción", "oso", "otorrinolaringólogo"]
word_pool = WordPool(words)
word_pool.select_words_without_accented_characters()
print(word_pool.words)
```

Check [the documentation][project_docs] for more details.

## Contributing to this project
  All contributions are welcome!

  Will find a detailed description of all the ways you can contribute to stimpool in
  [the contributing guide][contributing_guide].

  This is a beginner-friendly project so don't hesitate to ask any questions or get in touch
  with the project's maintainers.

  Please review the [project's code of conduct][code_conduct] before making
  any contributions.

## Author
  This project was developed by Mario E. Bermonti-Pérez as part of
  his academic research. Feel free to contact me at
  [mbermonti@psm.edu](mailto:mbermonti@psm.edu)  or
  [mbermonti1132@gmail.com](mailto:mbermonti1132@gmail.com)

## Credits
This package was created with [Cookiecutter][cookiecutter] and the [fedejaure/cookiecutter-modern-pypackage][cookiecutter-modern-pypackage] project template.

[cookiecutter]: https://github.com/cookiecutter/cookiecutter
[cookiecutter-modern-pypackage]: https://github.com/fedejaure/cookiecutter-modern-pypackage
[project_docs]: https://stimpool.readthedocs.io/en/latest/
[code_conduct]: ./CODE_OF_CONDUCT.md
[contributing_guide]: ./docs/contributing.md
