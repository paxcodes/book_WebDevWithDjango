import base64
import json
import pprint
import sys


def get_session_dictionary(session_key):
    binary_key, payload = base64.b64decode(session_key).split(b':', 1)
    return json.loads(payload.decode())


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        sys.exit("Please pass the session data.")

    session_key = sys.argv[1]
    session_dictionary = get_session_dictionary(session_key)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(session_dictionary)
