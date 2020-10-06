# coding: utf-8
import arrow
import datetime
from django.conf import settings
from django.core.management.base import BaseCommand
from rich.console import Console
import time
from yeoboseyo.models import Trigger
from feedparser_data import Rss


console = Console()


def _update_date(id) -> None:
    """
    update the database table with the execution date
    :param trigger_id: id to update
    :return: nothing
    """
    now = arrow.utcnow().to(settings.TIME_ZONE.format('YYYY-MM-DD HH:mm:ssZZ'))
    Trigger.objects.filter(id=id).update(date_triggered=str(now))


def get_published(entry) -> datetime:
    """
    get the 'published' attribute
    :param entry:
    :return: datetime
    """
    published = None
    if hasattr(entry, 'published_parsed'):
        if entry.published_parsed is not None:
            published = datetime.datetime.utcfromtimestamp(time.mktime(entry.published_parsed))
    elif hasattr(entry, 'created_parsed'):
        if entry.created_parsed is not None:
            published = datetime.datetime.utcfromtimestamp(time.mktime(entry.created_parsed))
    elif hasattr(entry, 'updated_parsed'):
        if entry.updated_parsed is not None:
            published = datetime.datetime.utcfromtimestamp(time.mktime(entry.updated_parsed))
    return published


def service(the_service, trigger, entry) -> int:
    """
    dynamic loading of service and submitting data to this one
    :param the_service:
    :param trigger:
    :param entry:
    :return:
    """
    # load the module/class + create class instance of the service
    klass = getattr(__import__('yeoboseyo.services.' + the_service.lower(), fromlist=[the_service]), the_service)
    # save the data
    if klass().save_data(trigger, entry):
        return 1
    else:
        console.print(f'no {the_service} created')
        return 0


class Command(BaseCommand):
    help = 'Grab all the news'

    def handle(self, *args, **options):
        console.print("여보세요 !")
        triggers = Trigger.objects.all()
        for trigger in triggers:
            if trigger.status:
                # RSS PART
                rss = Rss()
                # retrieve the data
                feeds = rss.get_data(**{'url_to_parse': trigger.rss_url, 'bypass_bozo': settings.BYPASS_BOZO})
                now = arrow.utcnow().to(settings.TIME_ZONE.format('YYYY-MM-DDTHH:mm:ssZZ'))
                date_triggered = arrow.get(trigger.date_triggered).to(settings.TIME_ZONE.format('YYYY-MM-DDTHH:mm:ssZZ'))
                read_entries = 0
                created_entries = 0
                for entry in feeds.entries:
                    # entry.*_parsed may be None when the date in a RSS Feed is invalid
                    # so will have the "now" date as default
                    published = get_published(entry)
                    if published:
                        published = arrow.get(published).to(settings.TIME_ZONE.format('YYYY-MM-DDTHH:mm:ssZZ'))
                    # last triggered execution
                    if published is not None and now >= published >= date_triggered:
                        read_entries += 1

                        if trigger.joplin_folder:
                            created_entries += service('Joplin', trigger, entry)
                        if trigger.mail:
                            created_entries += service('Mail', trigger, entry)
                        if trigger.mastodon:
                            created_entries += service('Mastodon', trigger, entry)
                        if trigger.reddit:
                            created_entries += service('Reddit', trigger, entry)
                        if trigger.localstorage:
                            created_entries += service('LocalStorage', trigger, entry)

                        if created_entries > 0:
                            _update_date(trigger.id)
                            console.print(f'[magenta]Trigger {trigger.description}[/] : '
                                          f'[green]{entry.title}[/]')

                if read_entries:
                    console.print(f'[magenta]Trigger {trigger.description}[/] : '
                                  f'[green]Entries[/] [bold]created[/] {created_entries} / '
                                  f'[bold]Read[/] {read_entries}')
                else:
                    console.print(f'[magenta]Trigger {trigger.description}[/] : no feeds read')
