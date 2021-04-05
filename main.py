import os
import csv
import requests
from bs4 import BeautifulSoup


def save_to_file(jobs, name):
    name = name.replace("/", " ")
    file = open(f"{name}.csv", mode="w", newline="", encoding="utf-8")
    writer = csv.writer(file)
    writer.writerow(["place", "title", "time", "pay", "date"])
    for job in jobs:
        writer.writerow(list(job.values()))
    print(f"Created {name}.csv\n")
    return


os.system("clear")
alba_url = "http://www.alba.co.kr"
result = requests.get(alba_url)
soup = BeautifulSoup(result.text, "html.parser")
mainSuperBrands = soup.find("div", {"id": "MainSuperBrand"}).find_all(
    "li", {"class": "impact"})

companies = []
for brand in mainSuperBrands:
    link = brand.find("a", {"class": "goodsBox-info"})["href"]
    name = brand.find("span", {"class": "company"}).text
    companies.append({"name": name, "link": link})

for company in companies:
    url = company['link']
    print(f"Parsing URL : {url}")
    name = company['name']
    try:
        result = requests.get(url)
        soup = BeautifulSoup(result.text, "html.parser")
        job_count = soup.find(
            "p", {"class": "jobCount"}).text[:-1].replace(",", "")
        last_page = int(job_count)//50+1
    except:
        print("error")
        continue
    jobs = []
    for page in range(last_page):
        try:
            print(f"Page[{page+1}/{last_page}]")
            p_result = requests.get(
                f"{url}job/brand/?page={page+1}&pagesize=50&agelimit=0&careercd=%20&totalCount={job_count}")
            soup = BeautifulSoup(p_result.text, "html.parser")
            trs = soup.find("div", {"id": "NormalInfo"}).find(
                "tbody").find_all("tr", {"class": ""})
        except:
            print("error")
            continue
        for tr in trs:
            try:
                place = tr.find("td", {"class": "local"})
                place = place.text.strip()
                title = tr.find("span", {"class": "company"}).text.strip()
                work_time = tr.find("td", {"class": "data"}).text.strip()
                pay = tr.find("td", {"class": "pay"}).text.strip()
                enroll_date = tr.find("td", {"class": "regDate"}).text.strip()
                jobs.append({"place": place, "title": title,
                            "time": work_time, "pay": pay, "date": enroll_date})
            except:
                print("error")
    save_to_file(jobs, name)
    print()
