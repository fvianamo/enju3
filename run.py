import logging
import time
import os

from scrapper import AdvfnScrapper
from repository import Repository

if __name__ == '__main__':
	logging.basicConfig( format='%(asctime)s - %(module)s - %(funcName)s - %(levelname)s - %(message)s', level=logging.INFO)
	SLEEP_TIME = int(os.environ['SLEEP_TIME'])

	logging.info('starting scrapper')

	while True:
		scrapper = AdvfnScrapper('https://br.advfn.com')
		news_url = scrapper.fetch_news('ENJU3')

		news_content = [scrapper.parse_news(new) for new in news_url]

		repository = Repository(database='scrapper', collection='enju3')
		repository.save(news_content)

		logging.info(f'going to sleep for {SLEEP_TIME} minutes')
		time.sleep(60*SLEEP_TIME)