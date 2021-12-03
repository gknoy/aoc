# ----------------------
# advent infrastructure
# ----------------------


def get_line_items(fname):
    with open(fname) as f:
        return (item.strip() for item in f.readlines())
