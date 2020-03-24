"""download online oss text files."""

from concurrent.futures import ThreadPoolExecutor as tpe
import glob

import requests


def download_nd_save(url: str) -> (str, str):
    """download content and return name and content."""
    resp = requests.get(url)
    content = resp.content.decode("utf-8")
    fname = url.split("/")[-1]
    save(fname, content)


def combine_files(to_file: str = "big_file.txt"):
    """combine all txt files into one big file."""
    txt_files = glob.glob("texts/*.txt")
    with open(to_file, "a") as bh:
        for txt_file in txt_files:
            with open(txt_file, "r") as fh:
                bh.write(fh.read())


def save(fname, content):
    """save files to texts directory."""
    fname = f"texts/{fname}"
    try:
        with open(fname, "w") as fh:
            fh.write(content)
    except FileExistsError as e:
        print("error: ", e)


def runner():
    urls = [
        "https://www.gutenberg.org/cache/epub/376/pg376.txt",
        "https://www.gutenberg.org/files/84/84-0.txt",
        "https://www.gutenberg.org/cache/epub/844/pg844.txt",
    ]

    with tpe(max_workers=8) as exe:
        results = exe.map(download_nd_save, urls)
    combine_files()
