from operator import le
import requests
from bs4 import BeautifulSoup


def get_prepods_text_list_page(url):

    prepod_list = []

    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    for select_div in soup.find_all("div", {"class": "mb-4"}):
        for select_lesson in select_div.find_all("p", {"class": "mb-2 fw-semi-bold text-dark"}):
            lesson = " ".join(select_lesson.find(text=True, recursive=False).split())
            
            for select_lesson_next in select_lesson.find_all("span", {"class": "text-nowrap"}):
                lesson_part = " ".join(select_lesson_next.find(text=True, recursive=False).split())
                full_lesson = lesson + " " + lesson_part
                
                for lesson_type in select_lesson_next.find_all("span", {"class": "badge bg-soft-secondary text-secondary ms-2 fw-medium text-smaller"}):
                    type = " ".join(lesson_type.find(text=True, recursive=False).split())    
                    
        for select_prepod in select_div.find_all("a", {"class": "text-body"}):
            if {"prepod": select_prepod.text, "lesson": lesson} not in prepod_list:
                prepod_list.append(
                    {"prepod": select_prepod.text, "lesson": full_lesson, "role": type})

    return(prepod_list)

