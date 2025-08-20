import subprocess
import sys
from pathlib import Path

from .log import logger

DEVTOOLS_DIR = Path(__file__).parent
CONFIG_DIR = DEVTOOLS_DIR / "config"
BLACK_TOML = CONFIG_DIR / "black.toml"
RUFF_TOML = CONFIG_DIR / "ruff.toml"

assert DEVTOOLS_DIR.is_dir()
assert CONFIG_DIR.is_dir()
assert BLACK_TOML.is_file()
assert RUFF_TOML.is_file()


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
