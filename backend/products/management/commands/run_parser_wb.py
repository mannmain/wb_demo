from products.management.commands.parser_wb.view.request_api import starter_parse
import asyncio
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Асинхронный парсинг товаров с Wildberries'

    def handle(self, *args, **options):
        asyncio.run(self.parse())

    async def parse(self):
        await starter_parse()

    async def save_product(self, item):
        from asgiref.sync import sync_to_async

        @sync_to_async
        def save():
            pass
        await save()
