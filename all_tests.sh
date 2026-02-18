#! /bin/bash

mkdir -p htmldoc/pyturbocode
uv run pytest
uv run pdoc --html --force --config latex_math=True -o htmldoc pyturbocode
uv run coverage html -d htmldoc/coverage --rcfile tests/coverage.conf
uv run coverage xml -o htmldoc/coverage/coverage.xml --rcfile tests/coverage.conf
uv run docstr-coverage src/pyturbocode -miP -sp -is -idel --skip-file-doc --badge=htmldoc/pyturbocode/doc_badge.svg
uv run genbadge coverage -l -i htmldoc/coverage/coverage.xml -o htmldoc/pyturbocode/cov_badge.svg
