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
        console.print("여보세요 !")
        if 'trigger' in options:
            """
    
            :param trigger_id:  the id of the trigger to switch on/off
            :return:
            """
            trigger = Trigger.objects.get(id=options.get('trigger'))
            date_triggered = arrow.utcnow().to(settings.TIME_ZONE.format('YYYY-MM-DD HH:mm:ssZZ'))
            trigger.status = not trigger.status
            trigger.date_triggered = date_triggered
            trigger.save()
            msg = f"Successfully enabled Trigger '{trigger.description}'"
            if trigger.status is False:
                msg = f"Successfully disabled Trigger '{trigger.description}'"

            console.print(msg)

