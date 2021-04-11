import logging
import os
from pymongo import MongoClient

class Repository:
	"""
	Interface para conexão com o repositório de dados, sendo este um MongoDB
	dados para conexão com o mongo deve ser informada via variavel de ambiente MONGO_URL
	Params:
		- database: nome do database a ser utilizado
		- collection: nome da collection onde os dados devem ser armazenados
	"""
	def __init__(self, **kwargs):
		mongo_url = os.environ['MONGO_URL']
		if mongo_url:
			logging.info('found MongoDB string connection on environment')

		assert kwargs['database']
		self.database = kwargs['database']
		assert kwargs['collection']
		self.collection = kwargs['database']

		client = MongoClient(mongo_url)

		try:
			client[self.database][self.collection].count_documents({})
			logging.info(f'MongoClient created successfully')
			self.conn = client
		except Exception as e:
			logging.critical('failed to connect with MongoDB')
			raise e
		

	def save(self, documents):
		if isinstance(documents, list):
			return self.conn[self.database][self.collection].insert_many(documents).inserted_ids
		elif isinstance(documents, dict):
			return self.conn[self.database][self.collection].insert_one(documents).inserted_id
		else:
			raise Exception(f'list or a dict should be provided, received {type(documents)} instead')

if __name__ == '__main__':
	logging.basicConfig( format='%(asctime)s - %(module)s - %(funcName)s - %(levelname)s - %(message)s', level=logging.INFO)
	repository = Repository(database='sadas', collection='dasdas')