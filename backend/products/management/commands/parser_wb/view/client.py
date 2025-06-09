from products.management.commands.parser_wb.view.interfaces import Logger


class Client(Logger):
    def __init__(
            self, proxy_list: list = None,
    ):
        Logger.__init__(self)
        self.proxy_list = proxy_list
        self.proxy_idx = 0
        self.proxy_init = proxy_list[0] if proxy_list else None
        # if self.proxy_init:
        #     self.session = ClientSession(connector=ProxyConnector.from_url(f'http://{self.proxy_init}', ssl=ssl.create_default_context(), verify_ssl=True))
        # else:
        #     self.session = ClientSession()

