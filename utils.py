# ----------------------
# advent infrastructure
# ----------------------

BOLD = "\033[1m"
CLEAR = "\033[0m"


def get_line_items(fname):
    with open(fname) as f:
        return (item.strip() for item in f.readlines())
