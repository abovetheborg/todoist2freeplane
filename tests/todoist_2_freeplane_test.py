import pytest
import os
import yaml
import logging
import sys

from .context import TodoistDocument

OUTPUT_PREFIX = os.path.join("output", "text_output_")

@pytest.fixture
def logger_during_tests():
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    handler = logging.FileHandler('log.txt', mode='w')
    handler.setFormatter(formatter)
    screen_handler = logging.StreamHandler(stream=sys.stdout)
    screen_handler.setFormatter(formatter)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.addHandler(screen_handler)
    return logger

@pytest.fixture
def todoist_document(logger_during_tests):
    with open("data.yml", 'r') as ymlfile:
        data = yaml.load(ymlfile, Loader=yaml.FullLoader)

        t = TodoistDocument('login', 'password', logger=logger_during_tests)
        t.remote_data = data

        return t


def test_freeplane_document_creation(todoist_document):
    filename = OUTPUT_PREFIX + 'simple_creation.mm'
    todoist_document.dump_to_freeplane(todoist_document.remote_data, filename)






