from products.management.commands.parser_wb.config.config import PAGE_SIZE

HEADERS = {
    'accept': '*/*',
    'accept-language': 'ru',
    'origin': 'https://www.wildberries.ru',
    'priority': 'u=1, i',
    'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
}


def split_list(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def split_list_to_n_parts(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))


def get_max_page(total, page_size=PAGE_SIZE):
    if total % page_size == 0:
        page_max = total // page_size
    else:
        page_max = total // page_size + 1
    return page_max


def get_nn(product_id: str) -> str:
    n = int(product_id) // 10 ** 5
    if 0 <= n <= 143:
        return "01"
    elif n <= 287:
        return "02"
    elif n <= 431:
        return "03"
    elif n <= 719:
        return "04"
    elif n <= 1007:
        return "05"
    elif n <= 1061:
        return "06"
    elif n <= 1115:
        return "07"
    elif n <= 1169:
        return "08"
    elif n <= 1313:
        return "09"
    elif n <= 1601:
        return "10"
    elif n <= 1655:
        return "11"
    elif n <= 1919:
        return "12"
    elif n <= 2045:
        return "13"
    elif n <= 2189:
        return "14"
    elif n <= 2405:
        return "15"
    elif n <= 2621:
        return "16"
    elif n <= 2837:
        return "17"
    elif n <= 3053:
        return "18"
    elif n <= 3269:
        return "19"
    elif n <= 3485:
        return "20"
    elif n <= 3701:
        return "21"
    elif n <= 3917:
        return "22"
    elif n <= 4133:
        return "23"
    elif n <= 4349:
        return "24"
    elif n <= 4565:
        return "25"
    elif n <= 4877:
        return "26"
    elif n <= 5189:
        return "27"
    elif n <= 5501:
        return "28"
    else:
        return "29"
