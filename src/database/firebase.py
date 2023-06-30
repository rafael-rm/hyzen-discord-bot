import firebase_admin
from firebase_admin import credentials
import logging
import os
import dotenv
import sys


class FirebaseDB:
    def __init__(self):
        logging.info('Iniciando conexão com o Firebase')
        try:
            dotenv.load_dotenv()
            database_url = str(os.getenv('FIREBASE_URL'))
            cred = credentials.Certificate("./serviceAccountKey.json")
            firebase_admin.initialize_app(cred, {'databaseURL': database_url})
            logging.info('Conexão com o Firebase iniciada com sucesso.')
        except Exception as error:
            logging.critical(f'Erro ao iniciar conexão com o Firebase: {error}')
            logging.critical('Aplicação encerrada.')
            sys.exit(1)


if __name__ == '__main__':
    firebase = FirebaseDB()
