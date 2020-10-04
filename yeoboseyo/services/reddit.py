# coding: utf-8
"""
   여보세요 Service Reddit
"""
# std lib
from __future__ import unicode_literals
from django.conf import settings
from logging import getLogger
# external lib
from praw import Reddit as RedditAPI
# yeoboseyo
from yeoboseyo.services import Service

# create logger
logger = getLogger(__name__)

__all__ = ['Reddit']


class Reddit(Service):
    """
        Service Mastodon
    """
    def __init__(self):
        super().__init__()
        self.reddit = RedditAPI(client_id=settings.REDDIT_CLIENT_ID,
                                client_secret=settings.REDDIT_CLIENT_SECRET,
                                password=settings.REDDIT_PASSWORD,
                                user_agent=settings.REDDIT_USERAGENT,
                                username=settings.REDDIT_USERNAME)

    def save_data(self, trigger, entry) -> bool:
        """
        Post a new toot to Mastodon
        :param trigger: current trigger
        :param entry: data from Feeds
        :return: boolean
        """
        status = False
        try:
            self.reddit.subreddit(trigger.reddit).submit(entry.title, url=entry.link)
            status = True
        except ValueError as e:
            logger.error(e)
            status = False
        return status
