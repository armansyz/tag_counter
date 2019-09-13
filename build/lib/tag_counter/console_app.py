from tag_counter.process_url import count_tags, url_format, url_name
from tag_counter.db_manager import TagManager
from loguru import logger
import pickle
import argparse
import yaml


def get_insert(argsa):
    """Get tags from db or insert if they do not exist"""

    t = TagManager()
    logger.info('Attempting to create tables if they do not exist')
    t.create_tables()

    url = None
    logger.info('Scanning yaml synonyms for the key:{}'.format(argsa.get))
    try:
        syn = yaml.load(open("tag_counter/synonyms.yaml"), yaml.SafeLoader)
        url = syn[argsa.get] if (argsa.get in syn) else argsa.get
    except KeyError as ke:
        logger.error('Wrong key! \n Exception:{}'.format(ke))
    except FileNotFoundError as fe:
        logger.error('File was not found \n Exception:{}'.format(fe))
    except Exception as exc:
        logger.error('Something bad happened \n Exception:{}'.format(exc))

    logger.info('Attempting to retrieve data from db')
    s = t.get_tag(full_url=url_format(url)).first()
    if not s:
        try:
            logger.info('No such tag info in the database')
            logger.info('Attempting to process the tags')
            tag_data = count_tags(url_format(url)).items()
            logger.info('Attempting to insert tags into db')
            t. \
                insert_tag(url_name(url),
                           url_format(url),
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

    url = None
    logger.info('Scanning yaml synonyms for the key:{}'.format(argsb.view))
    try:
        syn = yaml.load(open("tag_counter/synonyms.yaml"), yaml.SafeLoader)
        url = syn[argsb.view] if (argsb.view in syn) else argsb.view
    except KeyError as ke:
        logger.error('Wrong key! \n Exception:{}'.format(ke))
    except FileNotFoundError as fe:
        logger.error('File was not found \n Exception:{}'.format(fe))
    except Exception as exc:
        logger.error('Something bad happened \n Exception:{}'.format(exc))

    logger.info('Attempting to retrieve data from db')
    s = t.get_tag(full_url=url_format(url)).first()

    if not s:
        logger.info('No such tag info in the database')
        print('no data on {}'.format(url))
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

