class InvalidBoardSizeExcp(Exception):
    # Raised when a board size is not applicable
    # Range 3 - 50
    pass

class LogicalExcp(Exception):
    # Can be used as a wildcard to be handled a specific way if not fatal
    pass