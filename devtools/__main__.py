from dataclasses import dataclass
from pathlib import Path

import click

from .log import init_log, logger
from .utils import (
    get_black_toml,
    get_mypy_ini,
    get_package_name_from_pyproject,
    get_ruff_toml,
    run_command,
)


@click.group()
@click.option(
    "--log-level",
    default="INFO",
    type=click.Choice(
        ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], case_sensitive=False
    ),
    help="Set the logging level.",
)
def main(log_level: str) -> None:
    """Main CLI group."""
    init_log(log_level)
    logger.debug("Logging initialized.")


@dataclass(frozen=True, kw_only=True)
class LintConfig:
    ruff_toml: Path
    black_toml: Path


@main.group()
@click.option(
    "--ruff-toml",
    "ruff_toml",
    default=None,
    type=click.Path(exists=True, file_okay=True, dir_okay=False, path_type=Path),
    help="ruff.toml configuration file",
)
@click.option(
    "--black-toml",
    "black_toml",
    default=None,
    type=click.Path(exists=True, file_okay=True, dir_okay=False, path_type=Path),
    help="black.toml configuration file",
)
@click.pass_context
def lint(
    ctx: click.Context,
    ruff_toml: Path | None = None,
    black_toml: Path | None = None,
) -> None:
    ctx.obj = LintConfig(
        ruff_toml=ruff_toml or get_ruff_toml(),
        black_toml=black_toml or get_black_toml(),
    )
    logger.info(
        f"Running lint with ruff at {ctx.obj.ruff_toml} and black at {ctx.obj.black_toml}"
    )


lint: click.Group  # type: ignore


@lint.command()
@click.pass_obj
def check(cfg: LintConfig) -> None:
    """Run a lint check, WITHOUT fixing things, return with a non-zero exit code if any lint
    check fails."""
    run_command(["black", "--version"])
    run_command(["ruff", "--version"])
    run_command(["ruff", "check", ".", "--config", str(cfg.ruff_toml.absolute())])
    run_command(
        ["black", "--check", "--diff", ".", "--config", str(cfg.black_toml.absolute())]
    )


@lint.command()
@click.pass_obj
def fix(cfg: LintConfig) -> None:
    """Attempt to fix as many lint checks as possible"""
    run_command(["black", "--version"])
    run_command(["ruff", "--version"])
    run_command(
        ["ruff", "check", ".", "--fix", "--config", str(cfg.ruff_toml.absolute())]
    )
    run_command(["black", ".", "--config", str(cfg.black_toml.absolute())])


@main.command()
@click.option(
    "--mypy-ini",
    "mypy_ini",
    default=None,
    type=click.Path(exists=True, file_okay=True, dir_okay=False, path_type=Path),
    help="mypy.ini configuration file",
)
def typecheck(mypy_ini: Path | None = None) -> None:
    mypy_ini = mypy_ini or get_mypy_ini()
    run_command(["mypy", "--version"])
    run_command(
        [
            "mypy",
            "-p",
            get_package_name_from_pyproject(),
            "--config-file",
            str(mypy_ini.absolute()),
            "--no-namespace-packages",
        ]
    )


if __name__ == "__main__":
    main()
