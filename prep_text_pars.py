import requests
from bs4 import BeautifulSoup


def get_prepods_text_list_page(url):

    prepod_list = []

    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    for select_div in soup.find_all("div", {"class": "mb-4"}):
        for select_lesson in select_div.find_all("p", {"class": "mb-2 fw-semi-bold text-dark"}):
            lesson = (" ".join(select_lesson.text.split()))
        for select_prepod in select_div.find_all("a", {"class": "text-body"}):
            if {"prepod": select_prepod.text, "lesson": lesson} not in prepod_list:
                prepod_list.append(
                    {"prepod": select_prepod.text, "lesson": lesson})

    return(prepod_list)
