# pyturbocode

**pyturbocode** is a Python reference implementation of turbo codes (error-correction codes used in cellular communications and deep space). The implementation prioritizes clarity over performance and provides a simple rate 1/3 code without puncturing.

The main API is the `TurboCodec` class, which provides a clean `bytes -> bytes` interface wrapping CommPy's turbo encoding/decoding functions.

## Architecture

### Core Component: TurboCodec

The `TurboCodec` class (`src/pyturbocode/TurboCodec.py`) is the central API with two methods:

- **`encode(data: bytes) -> bytes`**: Converts input bytes to bits, passes them through a turbo encoder (rate 1/3), and returns encoded bytes with a 32-bit header storing the original bit length
- **`decode(encoded_data: bytes) -> bytes`**: Extracts metadata from the header, performs iterative turbo decoding (default 8 iterations), and returns decoded bytes

The class uses:
- Two RSC (Recursive Systematic Convolutional) trellis instances with configurable constraint length (default K=3)
- CommPy's `turbo_encode` and `turbo_decode` functions
- A random interleaver (seeded with 1346 for reproducibility)
- Bit-to-bytes conversion utilities for interfacing with CommPy

### Encoding Format

The encoded packet structure:
```
[Original bit length: 4 bytes][Systematic stream][Non-systematic stream 1][Non-systematic stream 2]
```

The systematic and non-systematic streams are each equal in length to the original message bits, making the output 3x the original size (rate 1/3).

## Common Commands

**Package manager**: Uses `uv` (not pip/pip-tools). Install with `uv sync --all-groups`.

### Testing

```bash
uv run pytest                                      # Run all tests
uv run pytest tests/test_codec.py::test_codec    # Run specific test
uv run pytest -v                                  # Verbose output
uv run pytest -k keyword                          # Run tests matching keyword
./all_tests.sh                                    # Full test + docs + coverage suite
```

### Code Quality

```bash
uv run black src/ tests/                          # Format code (100 char line length)
uv run ruff check src/ tests/                     # Lint with ruff
uv run pylint src/pyturbocode/                    # Lint with pylint
```

### Documentation & Coverage

```bash
uv run pdoc --html --force --config latex_math=True -o htmldoc pyturbocode
uv run coverage html -d htmldoc/coverage --rcfile tests/coverage.conf
uv run docstr-coverage src/pyturbocode
```

## Code Style & Configuration

- **Line length**: 100 characters (configured in pyproject.toml for black, ruff, and pylint)
- **Formatter**: Black
- **Linters**: Ruff, Pylint
- **Testing framework**: Pytest with plugins (html, cov, instafail, sugar, xdist, picked, mock)
- **Pre-commit hooks**: Enabled (see .pre-commit-config.yaml) - runs black, ruff, and basic checks

## Key Files

- `src/pyturbocode/TurboCodec.py` - Main API (core encode/decode logic)
- `src/pyturbocode/__init__.py` - Package initialization and logging setup
- `tests/test_codec.py` - Single integration test for encode/decode roundtrip
- `pyproject.toml` - Project configuration with build system, dependencies, tool configs, and dependency groups (dev, test, doc)
- `all_tests.sh` - Automation script for full test suite and documentation generation
- `.pre-commit-config.yaml` - Pre-commit hooks for code quality checks

## Dependencies

**Core runtime**:
- `numpy>=2.4.2` - Numerical operations
- `scikit-commpy>=0.8.0` - CommPy library providing Trellis, turbo_encode/turbo_decode, interleavers

**Python**: 3.12+

**Dependency groups** (managed by uv):
- `dev`: pre-commit, black, ipython, coverage-badge
- `test`: pytest and plugins
- `doc`: pdoc3, genbadge, docstr-coverage

## Recent Changes

The project underwent refactoring that consolidated separate modules into the `TurboCodec.py` API. The following modules were deprecated and removed:
- `rsc.py`, `trellis.py`, `siso_decoder.py`, `turbo_decoder.py`, `turbo_encoder.py`, `awgn.py`

These functions are now accessed directly through CommPy as external dependencies.

## Development Notes

- All functionality is currently in a single `TurboCodec` class - no need to navigate multiple modules
- The implementation uses CommPy's high-level API; low-level encoding/decoding details are abstracted away
- Tests are minimal (single roundtrip test) - focus is on correctness of the wrapper interface
- The interleaver seed is fixed (1346) for reproducibility across encode/decode cycles
