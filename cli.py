from typing import List, Dict
import logging
import sys
import argparse

try:
    import requests
except ModuleNotFoundError as e:
    print("Install requirements by running ``pip install -r requirements.txt`` in your virtual environment.")
    sys.exit(f"Due missing required package, {e.args[0]}")

from models import (PoemModel,
                    PoetModel,
                    BookModel,
                    create_tables,
                    remove_database,
                    db)


logger = logging.getLogger()
format_string = '[%(asctime)s] [%(levelname)s] [%(pathname)s]'\
        ' [%(funcName)s] [line %(lineno)d]: %(message)s'
logging.basicConfig(format=format_string)
formatter = logging.Formatter(format_string)


ALLEKOK_BASE_API_URL = 'https://allekok.ir/dev/tools'


def retrieve_list_of_poets(requests_session: requests.Session) -> List[Dict]:
    """
    It will retrieve all poets information.
    :return: A json - python list of dictionaries in this case
    """
    logging.info("Getting list of all poets.")
    response = requests_session.get(f"{ALLEKOK_BASE_API_URL}/poet.php",
                                    params={"poet": "all"})
    logging.info("List of poets retrieved.")
    return response.json()


def download_poems(requests_session: requests.Session) -> None:
    """
    Iterates over poets and books and poems. At meanwhile inserts them to db.

    """
    list_of_poets = retrieve_list_of_poets(requests_session)

    for poet in list_of_poets:
        logging.info(f'Inserting poet: `{poet["name"]}` to db.')
        poet_instance = PoetModel.create(full_name=poet['name'],
                                         name=poet['profname'],
                                         surname=poet['takh'],
                                         description=poet['hdesc'])
        for book_name in poet['bks']:
            logging.info(f"Getting list of all poems for poet: {{ id: {poet['id']}"
                         f", name: {poet['profname']}}}, book: {book_name} started.")
            response = requests_session.get(url="https://allekok.ir/dev/tools/poem.php",
                                            params={"poet": poet['id'],
                                                    "book": book_name,
                                                    "poem": "all"})
            logging.info(f"Getting list of all poems for poet:{poet['profname']}, book: {book_name} finished. ")

            result = response.json()
            logging.info(f'Inserting book: `{book_name}` to db.')
            book_instance = BookModel.create(name=book_name,
                                             poet_id=poet_instance)

            list_of_poems = []
            for poem in result['poems']:
                list_of_poems.append(
                    {"name": poem['name'],
                     "description": poem['hdesc'],
                     "link": poem['link'],
                     "text": poem['hon'],
                     "lang": poem['lang'],
                     "tag": poem['tag'],
                     "book_id": book_instance}
                )
            logging.info("Bulk insert poems to db.")
            with db.atomic():
                PoemModel.insert_many(list_of_poems).execute()


def main() -> None:
    logging.info("Process started.")
    with requests.Session() as requests_session:
        download_poems(requests_session)
    logging.info("Process finished.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="A simple CLI for exporting allekok data " \
                                                 "to a sqlite database.\n"
                                                 "It will have a file-based output as well in future.\n"
                                                 "Use -v or -vv to see the logs.",
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-v", "--verbosity",
                        help="increase output verbosity",
                        action="count",
                        default=0)

    args = parser.parse_args()

    if args.verbosity >= 2:
        logger.setLevel(logging.DEBUG)
    elif args.verbosity == 1:
        logger.setLevel(logging.INFO)
    else:
        print("You can use -v or -vv for more verbose output, respectively they set log level to INFO and DEBUG.")
        logger.setLevel(logging.CRITICAL)

    # Do the magic
    remove_database()
    create_tables()
    main()