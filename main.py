#!/usr/bin/env python
"""entrypoint file, where everything is initated"""

from download import runner
from summarize import summarize

if __name__ == "__main__":
    runner()
    with open("./big_file.txt", "r") as bf:
        print(summarize(bf.read()))

