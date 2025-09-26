# UnwrellaConnect Wine Extension for Blender

**UnwrellaConnect Wine for Blender** is a fork of [UnwrellaConnect for Blender](https://github.com/3d-io/unwrella-connect-for-blender) that adds functionality for Linux users to use the addon through Wine.

All functionality is directly available from within Blender's UV editor and all interaction between the programs happens transparently in the background. Unwrap anything without any manual exporting and re-importing of objects.

![UnwrellaConnect for Blender screenshot](https://docs.3d-plugin.com/images/unwrella-blender-bridge/unwrella-blender-UnwrellaConnect-title.png "UnwrellaConnect for Blender screenshot")

## Requirements
The extension requires Blender version 4.2 or later.

For Linux users, the extension requires Wine to be installed.

The extension does not work on its own but serves as a direct connection to Unwrella-IO or Packer-IO. One of these programs must be installed on the computer for the extension to work:

### Packer-IO
Packer-IO is freely available for Windows and Mac. It can be used with UnwrellaConnect to provide the full packing (but not the unwrapping) functionality of Unwrella completely free of charge.
UnwrellaConnect for Blender can interact with Packer-IO 1.2.0 or later.
For more information and free download of Packer-IO check out the [Packer-IO homepage](https://www.uv-packer.com)

### Unwrella-IO
Unwrella-IO is commercially available for Windows and can be used with UnwrellaConnect to provide full featured unwrapping and packing functionality.
UnwrellaConnect for Blender can interact with Unwrella-IO 1.1.0 or later.
For more information about Unwrella-IO check out the [Unwrella-IO homepage](https://www.unwrella.com)

**DISCLAIMER:** This fork has not been tested with Unwrella-IO, since the author doesn't own a copy of that software. It still tries to execute it, but support is not guaranteed.

## Installation on Linux
1. [Download and install Wine](https://gitlab.winehq.org/wine/wine/-/wikis/Download)
2. Download the installer for [Packer-IO](https://www.uv-packer.com/download/) or [Unwrella-IO](https://www.unwrella.com/download-order/)
3. Run the installer through Wine and proceed with the installation as normal
4. Download the addon as a .zip file from the [Releases page](https://github.com/Hokiper/unwrella-connect-wine-for-blender/releases/latest)
5. Drag and drop the downloaded .zip file into the Blender viewport

## Documentation
You can find the full documentation for UnwrellaConnect here:
https://docs.3d-plugin.com/unwrellaconnect-blender

## See it in Action
[![UnwrellaConnect video](https://img.youtube.com/vi/BiFyYPNrmDc/maxresdefault.jpg)](https://www.youtube.com/watch?v=BiFyYPNrmDc)
