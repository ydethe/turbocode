"""

.. include:: ../../README.md

# Testing

## Run the tests

To run tests, just run:

    uv run pytest

## Test reports

[See test report](../tests/report.html)

[See coverage](../coverage/index.html)

.. include:: ../../CHANGELOG.md

"""

import sys
import logging

# création de l'objet logger qui va nous servir à écrire dans les logs
logger = logging.getLogger("pyturbocode")

# Create stream handler for stdout
logHandler = logging.StreamHandler(sys.stdout)

# JSON formatter
formatter = logging.Formatter(
    '{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s", "name": "%(name)s"}'
)

logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
