import re
import string

test_str = "My N@me is Sk!b@@d, it's ni-ce to meet you"

PERMITTED_CHARS = string.digits + string.ascii_letters + "-' "


new_str = "".join(c for c in test_str if c in PERMITTED_CHARS)
print(new_str)

test2str = ["httpshammurabi", "camel", "joe", "https"]

for wrd in test2str:
    if "https" in wrd:
        test2str.remove(wrd)

print(test2str)


