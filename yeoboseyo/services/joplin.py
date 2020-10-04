# coding: utf-8
"""
   여보세요 Service Joplin
"""
# std lib
from __future__ import unicode_literals
from django.conf import settings
import httpx
from logging import getLogger
import typing
# yeoboseyo
from yeoboseyo.services import Service

# create logger
logger = getLogger(__name__)

__all__ = ['Joplin']


class Joplin(Service):

    joplin_port = 41184
    joplin_url = 'http://127.0.0.1'

    def __init__(self):
        """
        init parms
        """
        super().__init__()
        # overwritting config
        self.format_to = 'markdown_github'
        self.format_from = 'html'

        self.joplin_port = settings.JOPLIN_PORT
        self.joplin_url = settings.JOPLIN_URL

    def get_folders(self) -> typing.Any:
        """
        get the list of all the folders of the joplin profile
        :return:
        """
        url = f'{self.joplin_url}:{self.joplin_port}/folders'
        with httpx.Client() as client:
            try:
                res = client.get(url)
                return res.json()
            except (OSError, httpx._exceptions.NetworkError) as e:
                logger.error(f"Connection failed to {url}. Check if joplin is started")
                logger.error(e)
                logger.error('Yeoboseyo: Joplin access failed!')
                return False

    def save_data(self, trigger, entry) -> bool:
        """
        Post a new note to the JoplinWebclipperServer
        :param trigger: current trigger
        :param entry: data from Feeds
        :return: boolean
        """
        # build the json data
        folders = self.get_folders()
        if folders is not False:
            notebook_id = 0
            for folder in folders:
                if folder.get('title') == trigger.joplin_folder:
                    notebook_id = folder.get('id')
            if notebook_id == 0:
                for folder in folders:
                    if 'children' in folder:
                        for child in folder.get('children'):
                            if child.get('title') == trigger.joplin_folder:
                                notebook_id = child.get('id')
            # get the content of the Feeds
            content = self.create_body_content(trigger.description, entry)
            data = {'title': entry.title,
                    'body': content,
                    'parent_id': notebook_id,
                    'author': entry.author,
                    'source_url': entry.link}
            url = f'{self.joplin_url}:{self.joplin_port}/notes'
            logger.debug(url)
            logger.debug(data)
            with httpx.Client() as client:
                res = client.post(url, json=data)
            if res.status_code == 200:
                return True
        return False

    def check_service(self) -> bool:
        url = f'{self.joplin_url}:{self.joplin_port}/ping'
        with httpx.AsyncClient() as client:
            try:
                res = client.get(url)
                if res.text == 'JoplinClipperServer':
                    return True
            except (OSError, httpx._exceptions.NetworkError) as e:
                logger.error(f"Connection failed to {url}. Check if joplin is started")
                logger.error(e)
                logger.error('Yeoboseyo: Joplin access aborted!')
                return False
