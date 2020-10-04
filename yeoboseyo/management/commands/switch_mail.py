# coding: utf-8
import arrow
from django.conf import settings
from django.core.management.base import BaseCommand
from rich.console import Console
from yeoboseyo.models import Trigger


console = Console()


class Command(BaseCommand):
    help = 'Switch the Mail of the trigger'

    def add_arguments(self, parser):
        parser.add_argument('trigger', type=int)

    def handle(self, *args, **options):
        if 'trigger' in options:
            """
    
            :param trigger_id:  the id of the trigger to switch on/off mail
            :return:
            """
            trigger = Trigger.objects.get(id=options.get('trigger'))
            date_triggered = arrow.utcnow().to(settings.TIME_ZONE.format('YYYY-MM-DD HH:mm:ssZZ'))
            trigger.mail = not trigger.mail
            trigger.date_triggered = date_triggered
            trigger.save()
            msg = f"Successfully enabled Mail Trigger '{trigger.description}'"
            if trigger.mail is False:
                msg = f"Successfully disabled Mail Trigger '{trigger.description}'"

            console.print(msg)

