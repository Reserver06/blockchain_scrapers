import pickle
from pathlib import Path


def stash_webpage(response):
    raw_html = response.text
    raw_url = response.url[:-1] if response.url[-1] == "/" else response.url
    url = raw_url.split("/")[-1]

    item = {
        "url": response.url,
        "raw_html": raw_html,
    }
    path = Path.cwd().joinpath("blockchain_scrapers").joinpath("pickles")
    with open(path.joinpath(f"{url}.pickle"), "wb+") as pf:
        pickle.dump(item, pf)
