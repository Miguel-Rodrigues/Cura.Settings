# Copyright (c) 2019 Thomas Karl Pietrowski

__plugin_name__ = "Blender plugin"
__plugin_id__ = "CuraBlenderPlugin"

# Uranium
from UM.Logger import Logger
from UM.i18n import i18nCatalog

# This plugin
from . import BlenderReader

i18n_catalog = i18nCatalog(__plugin_id__)


def getMetaData():
    return {
        "mesh_reader": [
            {
                "extension": "BLEND",
                "description": i18n_catalog.i18nc("@item:inlistbox",
                                                  "Blender file"
                                                  )
            },
        ]
    }


def register(app):
    plugin_data = {}
    try:
        reader = BlenderReader.BlenderReader()
        plugin_data["mesh_reader"] = reader
    except Exception:
        Logger.logException("e", "An error occured, when loading the reader!")
        return {}

    return plugin_data
