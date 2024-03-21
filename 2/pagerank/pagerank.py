import os
import random
import re
import sys
from collections import Counter


DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    #corpus = {'1': {'2'}, '2': {'3', '1'}, '3': {'4', '2', '5'}, '4': {'2', '1'}, '5': set()}
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    all_pages = tuple(corpus.keys())

    source_pages = corpus.get(page)
    source_pages_len = len(source_pages)
    sourced = {p: damping_factor / source_pages_len for p in corpus.get(page)}

    if sourced:
        damped = {p: (1.0 - damping_factor) / len(all_pages) for p in all_pages}
        return {p: damped.get(p, 0) + sourced.get(p, 0) for p in (tuple(damped.keys()) + tuple(sourced.keys()))}
    else:
        return {p: 1.0 / len(all_pages) for p in all_pages}


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    all_pages = tuple(corpus.keys())
    tm = {page: transition_model(corpus, page, damping_factor) for page in all_pages}
    sample_page = random.choice(all_pages)
    data = [sample_page]
    tm_ = tm.get(sample_page)

    for n_ in range(n-1):
        sample_page = random.choices(tuple(tm_.keys()), weights=tuple(tm_.values()))[0]
        data.append(sample_page)
        tm_ = transition_model(corpus, sample_page, damping_factor)

    return {k: (1.0 * v)/n for k, v in Counter(data).items()}


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pages = tuple(corpus.keys())
    pages_len = len(pages)
    pagerank = {p: 1.0/pages_len for p in pages}

    threshold = 0.0001

    # {'3.html': {'4.html', '2.html'}, '4.html': {'2.html'}, '1.html': {'2.html'}, '2.html': {'3.html', '1.html'}}
    reverse_corpus = {p: {p2 for p2, i2 in corpus.items() if p in i2 or not i2} for p in corpus}
    # {'3.html': {'2.html'}, '4.html': {'3.html'}, '1.html': {'2.html'}, '2.html': {'4.html', '3.html', '1.html'}}


    pages_to_rank = set(pages)
    while pages_to_rank:
        for page in pages_to_rank.copy():
            pr = ( (1.0 - damping_factor) / pages_len ) + (damping_factor * sum(
                pagerank[i]/(
                    len(corpus[i]) if len(corpus[i]) > 0 else pages_len
                ) for i in reverse_corpus[page]
            ))
            #print(f'{page} {pagerank[page]} {pr}')
            if abs(pagerank[page] - pr) < threshold:
                pages_to_rank.remove(page)
            pagerank[page] = pr

    return pagerank


if __name__ == "__main__":
    main()
