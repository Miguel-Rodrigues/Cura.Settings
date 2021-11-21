# Copyright (c) 2019 Thomas Karl Pietrowski

import os
import platform

from UM.Application import Application  # @UnresolvedImport
from UM.Logger import Logger  # @UnresolvedImport
from UM.i18n import i18nCatalog  # @UnresolvedImport
from UM.Version import Version  # @UnresolvedImport

from .CadIntegrationUtils.CommonCLIReader import CommonCLIReader  # @UnresolvedImport

# Since 3.4: Register Mimetypes:
if Version("3.4") <= Version(Application.getInstance().getVersion()):
    from UM.MimeTypeDatabase import MimeTypeDatabase, MimeType

i18n_catalog = i18nCatalog("CuraBlenderIntegrationPlugin")


class BlenderReader(CommonCLIReader):
    def __init__(self):
        super().__init__()

        if Version("3.4") <= Version(Application.getInstance().getVersion()):
            MimeTypeDatabase.addMimeType(MimeType(name="application/x-extension-blend",
                                                  comment="Blender files",
                                                  suffixes=["BLEND"]
                                                  )
                                         )

        self._supported_extensions = [".BLEND".lower(),
                                      ]

        self.findPathsForAllExtensions()

    def areReadersAvailable(self):
        return bool(self._readerForFileformat)

    def openForeignFile(self, options):
        options["fileFormats"].append("stl")

        return super().openForeignFile(options)

    def exportFileAs(self, options, quality_enum=None):
        cmd = 'blender'
        bpy_scripts = os.path.join(os.path.split(__file__)[0], "BpyScripts")

        Logger.log("d", "BpyScripts at: {}".format(bpy_scripts))
        Logger.log("d", "Using blender file at: {}".format(
            options["foreignFile"]))
        Logger.log("d", "Exporting to: {}".format(options["tempFile"]))

        cmd = [cmd,
               options["foreignFile"],
               "--background",
               "--python",
               os.path.join(bpy_scripts, "ExportAsStl.py"),
               "--",
               options["tempFile"],
               ]

        self.executeCommand(cmd, cwd=os.path.split(options["foreignFile"])[0])
