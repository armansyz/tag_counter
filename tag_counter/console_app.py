from process_url import count_tags, url_format, url_name
from db_manager import TagManager
from loguru import logger
import pickle
import argparse


def get_insert(argsa):
    """Get tags from db or insert if they do not exist"""

    t = TagManager()
    logger.info('Attempting to create tables if they do not exist')
    t.create_tables()

    logger.info('Attempting to retrieve data from db')
    s = t.get_tag(full_url=url_format(argsa.get)).first()
    if not s:
        try:
            logger.info('No such tag info in the database')
            logger.info('Attempting to process the tags')
            tag_data = count_tags(url_format(argsa.get)).items()
            logger.info('Attempting to insert tags into db')
            t. \
                insert_tag(url_name(argsa.get),
                           url_format(argsa.get),
                           pickle.dumps(list(tag_data)))
            for tag, count in tag_data:
                print(tag, ':', count)
        except Exception as e:
            logger.error('Error has occurred \n Exception:{}'.format(e))
    else:
        logger.info('Tags found in the database')
        for tag, count in pickle.loads(s.tag_data):
            print(tag, ':', count)


def view_data(argsb):
    """Retrieve the info on tags from the database"""

    t = TagManager()
    logger.info('Attempting to create tables if they do not exist')
    t.create_tables()

    logger.info('Attempting to retrieve data from db')
    s = t.get_tag(full_url=url_format(argsb.view)).first()

    if not s:
        logger.info('No such tag info in the database')
        print('no data on {}'.format(argsb.view))
    else:
        logger.info('Tags found in the database')
        print("id:{} \nsite_name:{} \nfull_url:{} \nquery_date:{} \ntag_data:".
              format(s.id, s.site_name, s.full_url, s.query_date))
        for tag, count in pickle.loads(s.tag_data):
            print(tag, ':', count)


def console():
    """Console app"""

    parser = argparse.ArgumentParser(description="This is a tag counter app")
    parser.add_argument('-g',
                        '--get',
                        metavar='url', default="", action='store', help='count html tags in a web page')
    parser.add_argument('-vw',
                        '--view',
                        metavar='url', default="", action='store', help='view data stored in db')

    args = parser.parse_args()
    if args.get:
        logger.info('Received a get command')
        get_insert(args)
    elif args.view:
        logger.info('Received a view command')
        view_data(args)

