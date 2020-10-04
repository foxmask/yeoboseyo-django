# coding: utf-8
"""
   여보세요 Service Mastodon
"""
# std lib
from __future__ import unicode_literals
from django.conf import settings
from logging import getLogger
# external lib
from mastodon import Mastodon as MastodonAPI
# yeoboseyo
from yeoboseyo.services import Service

# create logger
logger = getLogger(__name__)

__all__ = ['Mastodon']


class Mastodon(Service):
    """
        Service Mastodon
    """
    def save_data(self, trigger, entry) -> bool:
        """
        Post a new toot to Mastodon
        :param trigger: current trigger
        :param entry: data from Feeds
        :return: boolean
        """
        status = False
        # check if we have a 'good' title
        content = str("{title} {link}").format(title=entry.title, link=entry.link)
        # if not then use the content
        content = self.set_mastodon_content(content)
        status = False
        try:
            toot_api = MastodonAPI(access_token='yeoboseyo_clientcred.secret',
                                   api_base_url=settings.MASTODON_INSTANCE)
            status = True
        except ValueError as e:
            logger.error(e)
            status = False
        try:
            toot_api.toot(content)
            status = True
        except Exception:
            status = False
        return status

    def set_mastodon_content(self, content) -> str:
        """
        cleaning content by removing any existing html tag
        :param content:
        :return:
        """
        limit = 560
        return content[:limit] if len(content) > limit else content
