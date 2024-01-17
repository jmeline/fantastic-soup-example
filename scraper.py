from bs4 import BeautifulSoup
from urllib.parse import urljoin

import requests
import concurrent.futures

def download_link(link):
    print(f"downloading '{link}'")
    link_content = requests.get(link).content
    with open(f'{link.split("/")[-1]}.pdf', 'wb') as file:
        file.write(link_content)
    print(f"done downloading {link}...")

URL = "https://maxniessl.com"

page = requests.get(urljoin(URL, "tabs.html"))

soup = BeautifulSoup(page.content, "html.parser")

links = soup.find_all('a', class_='btn btn-sm btn-light')

## https://abdulrwahab.medium.com/python-threadpoolexecutor-use-cases-for-parallel-processing-3d5c90fd5634

with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
    all_links = map(lambda link: urljoin(URL, link.get('href')), links)

    futures = [executor.submit(download_link, link) for link in all_links]

    # Pass each link and the base URL to the download_link function
    results = [future.result() for future in concurrent.futures.as_completed(futures)]

print("Downloaded all links concurrently.")
print("Done!")

