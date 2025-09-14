import subprocess
import sys
from pathlib import Path

import tomllib

from .log import logger

DEVTOOLS_DIR = Path(__file__).parent
CONFIG_DIR = DEVTOOLS_DIR / "config"
BLACK_TOML = CONFIG_DIR / "black.toml"
RUFF_TOML = CONFIG_DIR / "ruff.toml"
MYPY_INI = CONFIG_DIR / "mypy.ini"

assert DEVTOOLS_DIR.is_dir()
assert CONFIG_DIR.is_dir()
assert BLACK_TOML.is_file()
assert RUFF_TOML.is_file()
assert MYPY_INI.is_file()


def run_command(cmd: list[str]):
    """Run a command with subprocess, and check for a non-zero exit code"""
    logger.info(f"Running command: {' '.join(cmd)}")
    result = subprocess.run(cmd, check=False)  # noqa: S603
    if result.returncode != 0:
        sys.exit(result.returncode)


def _find_file(name: str, root: Path = Path.cwd()) -> Path | None:
    file = root / name
    if file.is_file():
        return file
    return None


def get_ruff_toml(root: Path = Path.cwd()) -> Path:
    return _find_file(RUFF_TOML.name, root=root) or RUFF_TOML


def get_black_toml(root: Path = Path.cwd()) -> Path:
    return _find_file(BLACK_TOML.name, root=root) or BLACK_TOML


def get_mypy_ini(root: Path = Path.cwd()) -> Path:
    return _find_file(MYPY_INI.name, root=root) or MYPY_INI


def get_package_name_from_pyproject(
    pyproject_path: Path = Path("pyproject.toml"),
) -> str:
    """
    Reads the package name from the pyproject.toml in the current working directory.

    Args:
        pyproject_path: Path to pyproject.toml (default: "pyproject.toml").

    Returns:
        str: The package name defined in [project.name] or [tool.poetry.name].

    Raises:
        FileNotFoundError: If pyproject.toml does not exist.
        ValueError: If the name field cannot be found.
    """
    if not pyproject_path.is_file():
        msg = f"{pyproject_path} not found in {Path.cwd()}"
        raise FileNotFoundError(msg)

    with pyproject_path.open("rb") as f:
        data = tomllib.load(f)

    # PEP 621: standard location
    if "project" in data and "name" in data["project"]:
        return data["project"]["name"]

    # Poetry-specific fallback
    if "tool" in data and "poetry" in data["tool"] and "name" in data["tool"]["poetry"]:
        return data["tool"]["poetry"]["name"]

    msg = f"Package name not found in {pyproject_path}"
    raise ValueError(msg)
