import asyncio
import json
from typing import Union

from aiohttp import ClientSession
from asgiref.sync import sync_to_async
from django.db import transaction

from products.models import Card, ColorVariant, ProductItem, Color, Brand, Kind
from products.management.commands.parser_wb.config.config import QUERY, MAX_PAGE_GLOBAL
from products.management.commands.parser_wb.config.helper import HEADERS, get_max_page, get_nn
from products.management.commands.parser_wb.view.client import Client
from products.management.commands.parser_wb.view.interfaces import *


class ParserItems(Logger):
    def __init__(self, client, query):
        super().__init__()
        self.client = client
        self.query = query
        self.base_url_search = 'https://search.wb.ru/exactmatch/ru/common/v13/search'
        self.base_url_card = 'https://card.wb.ru/cards/v2/detail'
        self.base_card_endpoint = '/info/ru/card.json'
        self.base_img_endpoint = '/images/big/{}.webp'

    def get_basket_url(self, product_id: str, endpoint: str) -> str:
        nn = get_nn(product_id)
        return f'https://basket-{nn}.wbbasket.ru/vol{product_id[:-5]}/part{product_id[:-3]}/{product_id}{endpoint}'  # NN, [:-5], [:-3], [:]

    async def make_request(self, name_func: str, method: str = 'GET', url: str = None, headers: dict = None,
                           params: dict = None, data: str = None, json_data: dict = None,
                           resp_type: str = 'text') -> Union[dict, str, None]:
        _headers = HEADERS.copy()
        while True:
            try:
                _headers['User-Agent'] = get_user_agent()
                async with ClientSession(headers=headers) as session:
                    async with session.request(method='GET', url=url, headers=_headers, params=params, timeout=10) as response:
                        # async with self.client.session.request(method='GET', url=url, headers=_headers, params=params) as response:
                        response_text = await response.text()
                        if (response_text.find('The operation requested is currently unavailable. Please, try again later.') != -1) or (response_text.find("You don't have permission to access") != -1):
                            self.logger_msg(msg=f'{name_func} | Ban ip', type_msg='error')
                            await asyncio.sleep(60)
                            continue
                        if resp_type == 'text':
                            return response_text
                        if resp_type == 'json':
                            try:
                                return json.loads(response_text)
                            except Exception as ex:
                                try:
                                    if ('File not found' in response_text) or ('This page could not be found' in response_text):
                                        return None
                                except:
                                    pass
                                self.logger_msg(msg=f'{name_func} | cant dump json | {response_text} | {ex} | {url=} {params=}',
                                                type_msg='error')
                                return None
            except Exception as ex:
                self.logger_msg(msg=f'{name_func} | Запрос не прошел | {ex} | {url=} {params=}', type_msg='error')
                await asyncio.sleep(10)

    async def get_data_on_search_page(self, page: int = 1) -> dict:
        name_func = self.get_data_on_search_page.__name__
        url = f'{self.base_url_search}'
        params = {
            'ab_testing': 'false',
            'appType': '1',
            'curr': 'rub',
            'dest': '-1257786',
            'hide_dtype': '13',
            'lang': 'ru',
            'page': f'{page}',
            'query': self.query,
            'resultset': 'catalog',
            'sort': 'popular',
            'spp': '30',
            'suppressSpellcheck': 'false',
        }
        response_json: dict = await self.make_request(name_func=name_func, method='GET', url=url, params=params, resp_type='json')
        if not response_json:
            return None
        if response_json.get('data', {}).get('products', {}):
            return response_json['data']

    async def get_variations_info_about_product(self, product_id: str):
        name_func = self.get_variations_info_about_product.__name__
        url = self.get_basket_url(product_id, self.base_card_endpoint)
        response_json: dict = await self.make_request(name_func=name_func, method='GET', url=url, resp_type='json')
        if not response_json:
            return None
        if str(response_json.get('nm_id', '')) == product_id:
            return response_json

    async def get_card_info_about_variations(self, product_color_id_list: list):
        name_func = self.get_card_info_about_variations.__name__
        url = self.base_url_card
        params = {
            'ab_testing': 'false',
            'appType': '1',
            'curr': 'rub',
            'dest': '-1257786',
            'hide_dtype': '13',
            'lang': 'ru',
            'spp': '30',
            'nm': ';'.join([str(i) for i in product_color_id_list])
        }
        response_json: dict = await self.make_request(name_func=name_func, method='GET', url=url, params=params, resp_type='json')
        if not response_json:
            return None
        if response_json.get('data', {}).get('products', {}):
            return response_json['data']['products']

    @staticmethod
    def get_size_quantity(stocks):
        quantity = 0
        for i in stocks:
            quantity += i['qty']
        return quantity

    @staticmethod
    def get_first_price_color(sizes_list):
        price = None
        for size in sizes_list:
            price = size.get('price', {}).get('product', None)
            if price:
                break
        return price

    async def get_data_item(self, product_info):
        variations_info = await self.get_variations_info_about_product(str(product_info['id']))
        vars_in_card_list = await self.get_card_info_about_variations(variations_info['colors'])
        data_item = {
            'id': product_info['root'],
            'brand_id': product_info['brandId'],
            'brand': product_info['brand'],
            'name': product_info['name'],
            'colors': []
        }
        colors_list = []
        for color_item in vars_in_card_list:
            if str(product_info['id']) == str(color_item['id']):
                var_details = variations_info
            else:
                var_details = await self.get_variations_info_about_product(str(color_item['id']))
            color_dict = {
                'color_list': color_item['colors'],
                'kind_list': var_details.get('kinds', []),
                'id': color_item['id'],
                'name': color_item['name'],
                'pics': color_item['pics'],
                'price': self.get_first_price_color(color_item['sizes']),
                'total_quantity': color_item['totalQuantity'],
                'in_stock': True if color_item['totalQuantity'] > 0 else False,
                'img_main': self.get_basket_url(str(color_item['id']), self.base_img_endpoint.format('1')),
                'desc': var_details.get('description', ''),
                'grouped_options': json.dumps(var_details.get('grouped_options', {})),
                'sizes': [],
            }
            sizes_list = []
            for size in color_item['sizes']:
                size_dict = {
                    'name': size['name'],
                    'optionId': size['optionId'],
                    'origName': size['origName'],
                    'price': size.get('price', {}).get('product', None),
                    'quantity': self.get_size_quantity(size['stocks']),
                    'in_stock': True if self.get_size_quantity(size['stocks']) > 0 else False,
                }
                sizes_list.append(size_dict)
            color_dict['sizes'] = sizes_list

            colors_list.append(color_dict)
        data_item['colors'] = colors_list


        # data_item = {
        #     'id': product_info['root'],
        #     'brand_id': product_info['brandId'],
        #     'brand': product_info['brand'],
        #     'name': product_info['name'],
        #     'colors': [{
        #         'color_list': color_item['colors'],
        #         'id': color_item['id'],
        #         'name': color_item['name'],
        #         'pics': color_item['pics'],
        #         'price': self.get_first_price_color(color_item['sizes']),
        #         'total_quantity': color_item['totalQuantity'],
        #         'in_stock': True if color_item['totalQuantity'] > 0 else False,
        #         'img_main': self.get_basket_url(str(color_item['id']), self.base_img_endpoint.format('1')),
        #         'sizes': [{
        #             'name': size['name'],
        #             'optionId': size['optionId'],
        #             'origName': size['origName'],
        #             'price': size.get('price', {}).get('product', None),
        #             'quantity': self.get_size_quantity(size['stocks']),
        #             'in_stock': True if self.get_size_quantity(size['stocks']) > 0 else False,
        #         } for size in color_item['sizes']]
        #     } for color_item in vars_in_card_list]
        # }
        return data_item

    async def save_card_data(self, data):
        from asgiref.sync import sync_to_async

        @sync_to_async
        def save(data):
            with transaction.atomic():
                for data_item in data:
                    card, _ = Card.objects.update_or_create(
                        id=int(data_item['id']),
                        defaults={
                            'brand': data_item['brand'],
                            'name': data_item['name'],
                        }
                    )
                    Brand.objects.update_or_create(
                        id=int(data_item['brand_id']),
                        defaults={
                            'brand': data_item['brand'],
                        }
                    )

                    for color_variant in data_item['colors']:
                        color_ids = []
                        for color in color_variant['color_list']:
                            color_obj, _ = Color.objects.update_or_create(
                                id=int(color['id']),
                                defaults={'name': color['name']}
                            )
                            color_ids.append(color_obj.id)
                        color_variant_obj, _ = ColorVariant.objects.update_or_create(
                            id=int(color_variant['id']),
                            defaults={
                                'card': card,
                                'name': color_variant['name'],
                                'desc': color_variant['desc'],
                                'grouped_options': color_variant['grouped_options'],
                                'pics': color_variant['pics'],
                                'price': color_variant['price'],
                                'total_quantity': color_variant['total_quantity'],
                                'in_stock': color_variant['in_stock'],
                                'img_main': color_variant['img_main']
                            }
                        )
                        kind_ids = []
                        for kind_name in color_variant['kind_list']:
                            kind_obj, _ = Kind.objects.get_or_create(name=kind_name)
                            kind_ids.append(kind_obj.id)
                        color_variant_obj.kinds.set(kind_ids)
                        color_variant_obj.colors.set(color_ids)

                        for size in color_variant['sizes']:
                            ProductItem.objects.update_or_create(
                                color_variant=color_variant_obj,
                                id=int(f"{color_variant['id']}{size['optionId']}"),
                                defaults={
                                    'size_name': size['name'],
                                    'orig_name': size['origName'],
                                    'optionId': size['optionId'],
                                    'price': size['price'],
                                    'quantity': size['quantity'],
                                    'in_stock': size['in_stock'],
                                }
                            )
        await save(data)

    async def start_parse_items(self):

        data = await self.get_data_on_search_page()
        total = data['total']
        search_products_list = data['products']
        step = len(search_products_list)
        finish_count = 0
        max_page = get_max_page(total)
        if MAX_PAGE_GLOBAL['status']:
            max_page = MAX_PAGE_GLOBAL['max_page']
        for page in range(max_page):
            data = await self.get_data_on_search_page(page)
            tasks = [self.get_data_item(i) for i in data['products']]
            if not tasks:
                break
            data = await asyncio.gather(*tasks)

            await self.save_card_data(data)
            self.logger_msg(msg=f'Пройдено Items {finish_count + step}/{total} товаров', type_msg='info')
            finish_count += step


async def starter_parse():
    client = Client()
    worker = ParserItems(client, QUERY)
    await worker.start_parse_items()
    client.logger_msg(msg=f'Items success parsed', type_msg='success')


if __name__ == '__main__':
    asyncio.run(starter_parse())
