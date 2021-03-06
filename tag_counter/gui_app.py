from tkinter import *
from tkinter.messagebox import showinfo, showerror
from tag_counter.db_manager import TagManager
from tag_counter.process_url import url_format, url_name, count_tags
from loguru import logger
import yaml
import pickle


def gui():
    """Gui app"""

    def output():
        """Gui command"""

        s = entry.get()

        url = None
        logger.info('Scanning yaml synonyms for the key:{}'.format(s))
        try:
            syn = yaml.load(open("tag_counter/synonyms.yaml"), yaml.SafeLoader)
            url = syn[s] if (s in syn) else s
        except KeyError as ke:
            logger.error('Wrong key! \n Exception:{}'.format(ke))
        except FileNotFoundError as fe:
            logger.error('File was not found \n Exception:{}'.format(fe))
        except Exception as e:
            logger.error('Something bad happened \n Exception:{}'.format(e))

        t = TagManager()
        logger.info('Attempting to create tables if they do not exist')
        t.create_tables()

        logger.info('Attempting to retrieve data from db')
        tags = t.get_tag(full_url=url_format(url)).first()

        tag_data = None
        if not tags:
            try:
                logger.info('No such tag info in the database')
                logger.info('Attempting to process the tags')
                tag_data = count_tags(url_format(url)).items()

                logger.info('Attempting to insert tags into db')
                t. \
                    insert_tag(url_name(url),
                               url_format(url),
                               pickle.dumps(list(tag_data)))
            except Exception as e:
                logger.error('Error has occurred \n Exception:{}'.format(e))
                text.delete(1.0, END)
        else:
            logger.info('Tags found in the database')
            tag_data = pickle.loads(tags.tag_data)

        if tag_data:
            num_tags = 'tag: count \n'
            logger.info('Output the tags')

            for tag, count in tag_data:
                num_tags += '{}: {} \n'.format(tag, count)
            try:
                text.delete(1.0, END)
                text.insert(1.0, num_tags)
            except TclError as te:
                logger.error('Failed to output the data \n Exception:{}'.format(te))
            showinfo(title='info', message='processed!')
        else:
            showerror(title='error', message='not a valid url!')

    logger.info('Initializing the gui interface')

    window = None

    try:
        window = Tk()

        button = Button(window, text='start', command=output)
        entry = Entry(width=100)
        text = Text(height=30, wrap=WORD)

        entry.pack()
        button.pack()
        text.pack()
    except TclError as tcl:
        logger.error('Gui interface failed to initialize \n Exception:{}'.format(tcl))
    except Exception as exc:
        logger.error('Something bad happened \n Exception:{}'.format(exc))

    try:
        window.mainloop()
    except TclError as tcl:
        logger.error('Something went wrong during the execution of the program \n Exception:()'.format(tcl))
    except Exception as exc:
        logger.error('Not sure what happened \n Exception:{}'.format(exc))
