import requests
import re
import datetime
from scrapers.BaseScraper import BaseScraper
from scrapers.ShiftCode import ShiftCode
from constants import GAME_SYSTEM


class RedditShiftCodeScraper(BaseScraper):

    url = ''
    body = ''

    def __init__(self, subreddit_url):
        self.url = self.get_reddit_json_url(subreddit_url)
        self.body = self.get_reddit_json()


    def get_reddit_json_url(self, url):
        # Ensure URL ends in .json
        if not url.endswith('.json'):
            json_url = url.rstrip('/') + '.json'
        else:
            json_url = url
        return json_url

    def get_reddit_json(self):
        # Headers are mandatory to avoid 429 Too Many Requests errors
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

        try:
            response = requests.get(self.url, headers=headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f'error: {e}, url: {self.url}, status_code: {response.status_code}')
            return None


        if response.status_code == 200:
            return response.json()
        else:
            return f"Error: {response.status_code}"

    def find_codes(self):
        shift_code_return: list[ShiftCode] = []
        for post in self.body['data']['children']:
            codes = re.findall(self.PATTERN, post['data']['selftext'])
            for code in codes:
                title = post['data']['title'].upper()
                game = ''
                if title in GAME_SYSTEM.keys():
                    game = title
                readable_date = datetime.datetime.fromtimestamp(post['data']['created']).strftime('%Y-%m-%d')
                shift_code_return.append(ShiftCode(code, readable_date, post['data']['url'], game))
        return shift_code_return


if __name__ == '__main__':
    subreddit_url = 'https://www.reddit.com/r/Borderlandsshiftcodes.json'
    scraper = RedditShiftCodeScraper(subreddit_url)
    print(scraper.find_codes())