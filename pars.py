from bs4 import BeautifulSoup
import requests

headers = {"User-Agent": "Mozilla/5.0"}

url = 'https://mai.ru/education/studies/schedule/index.php?group=%D0%9C3%D0%9E-221%D0%91-20'

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

root = soup.html
    
for tag in soup.find_all("p", {"class": "mb-2 fw-semi-bold text-dark"}):
    print("{0}: {1}".format(tag.name, " ".join(tag.text.split())))
