import os
import requests
from bs4 import BeautifulSoup
import csv
from tqdm import tqdm
from colorama import Fore, Style

# Constants
BASE_URL = "https://www.casarosada.gob.ar/informacion/discursos"
OUTPUT_DIR = "scraped_data"
CSV_FILE = os.path.join(OUTPUT_DIR, "speeches.csv")
PROGRESS_FILE = os.path.join(OUTPUT_DIR, "progress.txt")

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)


def get_speech_links(page_url):
    response = requests.get(page_url)
    soup = BeautifulSoup(response.content, "html.parser")
    links = soup.find_all("a", class_="panel")
    speech_links = [link["href"] for link in links]
    return speech_links


def scrape_speech(speech_url):
    # print(f"Scraping speech from {speech_url}...")
    response = requests.get(speech_url)
    soup = BeautifulSoup(response.content, "html.parser")

    title_tag = soup.find("h2", class_="panel-title")
    date_tag = soup.find("time")
    content_tag = soup.find("div", class_="item-page")

    title = title_tag.get_text(strip=True) if title_tag else "No Title"
    date = date_tag.get_text(strip=True) if date_tag else "No Date"
    content = content_tag.get_text(strip=True) if content_tag else "No Content"

    return title, date, content


def save_speech_to_txt(speech_id, date, content):
    # Format the date to remove spaces and special characters
    formatted_date = date.replace(" ", "_").replace(",", "").replace(":", "")
    filename = os.path.join(OUTPUT_DIR, f"{speech_id}_{formatted_date}.txt")
    with open(filename, "w", encoding="utf-8") as file:
        file.write(content)


def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as file:
            return set(line.strip() for line in file)
    return set()


def save_progress(speech_id):
    with open(PROGRESS_FILE, "a") as file:
        file.write(f"{speech_id}\n")


def main():
    all_speeches = []
    page_number = 1
    speech_id = 1
    completed_speeches = load_progress()

    while True:
        page_url = f"{BASE_URL}?start={(page_number - 1) * 40}"
        print(Fore.GREEN + f"Scraping page {page_number}..." + Style.RESET_ALL)
        speech_links = get_speech_links(page_url)

        if not speech_links:
            break

        for link in tqdm(speech_links, desc="Speeches"):
            full_url = f"https://www.casarosada.gob.ar{link}"
            if str(speech_id) in completed_speeches:
                speech_id += 1
                continue

            title, date, content = scrape_speech(full_url)
            all_speeches.append([title, date, full_url])
            save_speech_to_txt(speech_id, date, content)
            save_progress(speech_id)
            speech_id += 1

        page_number += 1

    # Save all speeches to CSV
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Title", "Date", "URL"])
        writer.writerows(all_speeches)

    print(Fore.BLUE + "Scraping completed!" + Style.RESET_ALL)


if __name__ == "__main__":
    main()
