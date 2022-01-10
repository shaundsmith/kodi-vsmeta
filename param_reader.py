import sys
import urllib.parse


# Returns the current input parameters as a Python dict.
#   returns: the parameters as a Python dict
def read():
    """
    Returns the input parameters as a dict.

    :return: the input parameters
    """
    param_string = sys.argv[2][1:]
    if param_string:
        return dict(urllib.parse.parse_qsl(param_string))
    return {}
