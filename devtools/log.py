import logging


def init_log(level: int | str = logging.INFO) -> None:
    logging.basicConfig(
        format="%(asctime)s [%(name)-10s :: %(levelname)8s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=level,
    )


logger = logging.getLogger("devtools")
