# coding: utf-8
import arrow
from django.conf import settings
from django.core.management.base import BaseCommand
from rich.console import Console
from yeoboseyo.models import Trigger


console = Console()


class Command(BaseCommand):
    help = 'Switch the status of the trigger'

    def add_arguments(self, parser):
        parser.add_argument('trigger', type=int)

    def handle(self, *args, **options):
        """

        :param options:  to pass the trigger to switch on/off
        :return:
        """
        console.print("여보세요 !")

        if 'trigger' in options:
            trigger = Trigger.objects.get(id=options.get('trigger'))
            date_triggered = arrow.utcnow().to(settings.TIME_ZONE.format('YYYY-MM-DD HH:mm:ssZZ'))
            trigger.mastodon = not trigger.mastodon
            trigger.date_triggered = date_triggered
            trigger.save()
            msg = f"Successfully enabled Mastodon Trigger '{trigger.description}'"
            if trigger.mastodon is False:
                msg = f"Successfully disabled Mastodon Trigger '{trigger.description}'"

            console.print(msg)
