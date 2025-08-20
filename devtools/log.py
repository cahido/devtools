import logging


def init_log(level=logging.INFO):
    logging.basicConfig(
        format="%(asctime)s [%(name)-10s :: %(levelname)8s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=level,
    )


logger = logging.getLogger("devtools")
