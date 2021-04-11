import logging

from scrapper import AdvfnScrapper

if __name__ == '__main__':
	logging.basicConfig( format='%(asctime)s - %(module)s - %(funcName)s - %(levelname)s - %(message)s', level=logging.INFO)
	scrapper = AdvfnScrapper('https://br.advfn.com')
	news_url = scrapper.fetch_news('ENJU3')

	news_content = [scrapper.parse_news(new) for new in news_url]

	print(news_content)