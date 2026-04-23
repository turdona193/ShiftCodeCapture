import requests
import re
from datetime import datetime
from scrapers.BaseScraper import BaseScraper
from scrapers.ShiftCode import ShiftCode
from constants import GAME_SYSTEM
from bs4 import BeautifulSoup


class MentalMarsScraper(BaseScraper):

    url = ''
    body = ''

    def __init__(self, url):
        self.url = url
        self.body = self.get_body()

    def get_body(self):
        # Headers are mandatory to avoid 429 Too Many Requests errors
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

        try:
            response = requests.get(self.url, headers=headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f'error: {e}, url: {self.url}, status_code: {response.status_code}')
            return None


        if response.status_code == 200:
            return response.content
        else:
            return f"Error: {response.status_code}"

    def find_codes(self):
        shift_code_return: list[ShiftCode] = []
        bs = BeautifulSoup(scraper.body, 'html.parser')
        tables = bs.find_all('figure', class_='wp-block-table is-style-stripes')
        for table in tables:
            for row in table.find_all('tr')[1:]:
                # print(row.prettify())
                expires_on = None
                elements = row.find_all('td')
                code = elements[2].text.strip()

                # Shift codes have standard formatting, so if a code does not match the pattern, likely means the data is corrupted or we are looking in the wrong spot.
                if not (code and re.match(self.PATTERN,code)):
                    print(f'For the code {code}; Code does not match the pattern {self.PATTERN}')
                    continue

                # Some tables have different formats and only some include an expiration date.
                # [TODO] - Include parsing of table headers to identify when we have access to Expiration date.
                if len(elements) > 3 and elements[3]:
                    try:
                        expires_on = datetime.strptime(elements[3].text.strip(), '%b %d, %Y')
                    except:
                        print (f'For the code {code}; Could not parse date: {elements[3].text.strip()}')

                # [todo] - Add logic to identify Game based on URI.
                shift_code_return.append(ShiftCode(elements[2].text.strip(), datetime.now() , self.url, reward=elements[0].text.strip(), expires=expires_on))

        return shift_code_return

if __name__ == '__main__':
    url = 'https://mentalmars.com/game-news/borderlands-4-shift-codes/'
    scraper = MentalMarsScraper(url)
    print(scraper.find_codes())