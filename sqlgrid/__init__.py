from ._version import version_info, __version__  # noqa F401

from .grid import (
    enable,
    disable,
    set_defaults,
    on,
    off,
    set_grid_option,
    show_grid,
    sqlgridWidget,
    gridctl,
)


def _jupyter_nbextension_paths():
    return [
        {
            "section": "notebook",
            "src": "static",
            "dest": "sqlgrid",
            "require": "sqlgrid/extension",
        }
    ]


__all__ = [
    "enable",
    "disable",
    "set_defaults",
    "on",
    "off",
    "set_grid_option",
    "show_grid",
    "sqlgridWidget",
    "gridctl",
]
