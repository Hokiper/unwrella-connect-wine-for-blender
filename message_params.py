from enum import Enum

class QueueMessage(Enum):
  MESSAGE = 0
  PROGRESS = 1
  STATS = 2
  COMPLETE = 3

class QueueMsgSeverity(Enum):
  INFO = 0
  WARNING = 1
  ERROR = 2