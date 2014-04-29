"""
:synopsis: Parent crawler module, which supervises all crawlers.

Contains functions for initializing all subsidiary, threaded crawlers.
"""

import os, Queue

from bitshift.crawler import crawler, indexer

__all__ = ["crawl"]

def crawl():
    """
    Initialize all crawlers (and indexers).

    Start the:
    1. GitHub crawler, :class:`crawler.GitHubCrawler`.
    2. Bitbucket crawler, :class:`crawler.BitbucketCrawler`.
    3. Git indexer, :class:`bitshift.crawler.indexer.GitIndexer`.
    """

    MAX_URL_QUEUE_SIZE = 5e3

    repo_clone_queue = Queue.Queue(maxsize=MAX_URL_QUEUE_SIZE)
    threads = [crawler.GitHubCrawler(repo_clone_queue),
            crawler.BitbucketCrawler(repo_clone_queue),
            indexer.GitIndexer(repo_clone_queue)]

    for thread in threads:
        thread.start()
