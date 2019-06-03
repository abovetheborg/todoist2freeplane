import pytest
import os
import yaml

from .context import TodoistDocument

OUTPUT_PREFIX = os.path.join("output", "text_output_")


@pytest.fixture
def todoist_document():
    with open("data.yml", 'r') as ymlfile:
        data = yaml.load(ymlfile, Loader=yaml.FullLoader)

        t = TodoistDocument('login', 'password')
        t.remote_data = data

        return t


def test_freeplane_document_creation(todoist_document):
    filename = OUTPUT_PREFIX + 'simple_creation.mm'
    todoist_document.dump_to_freeplane(todoist_document.remote_data, filename)






