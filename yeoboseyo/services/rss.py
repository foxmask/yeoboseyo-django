# coding: utf-8
"""
   여보세요 Service Rss
"""
# std lib
from __future__ import unicode_literals
from logging import getLogger
import typing
# external lib
import feedparser
import httpx

# create logger
logger = getLogger(__name__)

__all__ = ['Rss']


class Rss:

    USER_AGENT = 'Yeoboseyo/1.0 +https://github.com/foxmask/yeoboseyo'

    def get_data(self, **kwargs) -> typing.Any:
        """
        read the data from a given URL or path to a local file
        :param kwargs:
        :return: Feeds if Feeds well formed
        """
        if 'url_to_parse' not in kwargs:
            raise ValueError('you have to provide "url_to_parse" value')
        url_to_parse = kwargs.get('url_to_parse', '')
        if url_to_parse is False:
            raise ValueError('you have to provide "url_to_parse" value')
        bypass_bozo = kwargs.get('bypass_bozo', "False")
        with httpx.Client(timeout=30) as client:
            data = client.get(url_to_parse)
            logger.debug(url_to_parse)
            data = feedparser.parse(data.text, agent=self.USER_AGENT)
            # if the feeds is not well formed, return no data at all
            if bypass_bozo is False and data.bozo == 1:
                data.entries = ''
                log = f"{url_to_parse}: is not valid. You can tick the checkbox "
                "'Bypass Feeds error ?' to force the process"
                logger.info(log)

        return data
