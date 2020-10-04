# coding: utf-8
from django.core.management.base import BaseCommand
from rich.console import Console
from rich.table import Table
from yeoboseyo.models import Trigger

console = Console()


class Command(BaseCommand):
    help = 'Display report of the trigger'

    def handle(self, *args, **options):

        triggers = Trigger.objects.all()
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID")
        table.add_column("Name")
        table.add_column("Md Folder")
        table.add_column("Joplin Folder")
        table.add_column("Mastodon")
        table.add_column("Mail")
        table.add_column("Reddit")
        table.add_column("Status")
        table.add_column("Triggered", style="dim")

        for trigger in triggers:
            status = "[green]Ok[/]" if trigger.status else "[yellow]Disabled[/]"
            masto = "[green]Ok[/]" if trigger.mastodon else "[yellow]Disabled[/]"
            mail = "[green]Ok[/]" if trigger.mail else "[yellow]Disabled[/]"
            date_triggered = trigger.date_triggered if trigger.date_triggered is not None else '***Not triggered yet**'
            joplin_folder = trigger.joplin_folder if trigger.joplin_folder is not None else '***Not used ***'
            reddit = trigger.reddit if trigger.reddit is not None else '***Not used ***'
            localstorage = trigger.localstorage if trigger.localstorage is not None else '***Not used ***'
            table.add_row(str(trigger.id),
                          trigger.description,
                          localstorage,
                          joplin_folder,
                          masto,
                          mail,
                          reddit,
                          status,
                          str(date_triggered))
        console.print(table)
