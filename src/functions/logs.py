import logging


def main():
    logging.basicConfig(level=logging.INFO, filename='logs.log', format='%(asctime)s [%(levelname)s] %(name)s (%(filename)s %(lineno)d) - %(message)s', datefmt='%d/%m/%Y %H:%M:%S', encoding='utf-8')
    loggin_format = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s (%(filename)s %(lineno)d) - %(message)s', datefmt='%d/%m/%Y %H:%M:%S')
    console = logging.StreamHandler()
    console.setFormatter(loggin_format)
    logging.getLogger().addHandler(console)


if __name__ == '__main__':
    main()