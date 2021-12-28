from __future__ import annotations

import logging
import typing as t

import aiohttp

__all__ = ["init_logger", "check_for_updates"]

_LOGGER = logging.getLogger(__name__)

FORMAT = "%(levelname)-1.1s %(asctime)s %(name)s: %(message)s"
COLORS = {
    logging.DEBUG: "\33[1m",  # bold default
    logging.INFO: "\33[1;32m",  # bold green
    logging.WARNING: "\33[1;33m]",  # bold yellow
    logging.ERROR: "\33[1;31m",  # bold red
    logging.CRITICAL: "\33[1;35m",  # bold magenta
}


class Formatter(logging.Formatter):
    def format(self, record):
        color = COLORS[record.levelno]
        log = color + FORMAT + "\33[0m"
        return logging.Formatter(log, style="%").format(record)


def init_logger(config: t.Union[str, int, dict[str, t.Any]]):
    if isinstance(config, dict):
        logging.config.dictConfig(config)

    else:
        handler = logging.StreamHandler()
        handler.setFormatter(Formatter())
        logging.basicConfig(level=config, handlers=[handler])


async def check_for_updates():
    from packaging import version

    from verox._about import __version__

    try:
        async with aiohttp.request("GET", "https://pypi.org/pypi/verox/json") as resp:
            data = await resp.json()

        newest_version = version.parse(data["info"]["version"])

        curr_version = version.parse(__version__)

        if newest_version > curr_version:
            answer = input(
                f"A new version of verox is available (currently on {__version__}). Do you want to upgrade to {newest_version}? [Y/n]"
            )
            if answer.lower() == "y" or answer == "":
                import os
                import subprocess
                import sys

                args = (
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    "-U",
                    f"verox=={newest_version}",
                )
                subprocess.run(args)
                os.execv(sys.executable, [sys.executable] + sys.argv)

    except Exception as e:
        _LOGGER.error("Could not determine whether verox needs an update.", exc_info=e)
