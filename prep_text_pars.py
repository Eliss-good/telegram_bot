import requests
from bs4 import BeautifulSoup

def get_prepods_text_list_page(url):
    prepod_list = []
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    for all_info in soup.find_all("ul", {"class": "list-inline list-separator text-body small"}):
        for prepod_info in all_info.find_all("a", {"class": "text-body"}):
            if prepod_info.text not in prepod_list:
                prepod_list.append(prepod_info.text)

    return prepod_list
