from enum import Enum

class AppAccess(Enum):
  NONE = 0
  PACKER_IO = 1
  UNWRELLA_IO = 2

unwrellaParams = {
  "appPath": "",
  "appAccess": AppAccess.NONE,
  "icons": {}
}