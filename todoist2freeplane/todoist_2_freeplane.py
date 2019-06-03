import todoist
import yaml
import pprint as pp

from freeplane_schema.freeplane_schema import FreeplaneSchema


class TodoistDocument(object):
    def __init__(self, todoist_user, todoist_password):
        self.todoist_api = todoist.TodoistAPI()
        self.todoist_api.user.login(todoist_user, todoist_password)
        self.remote_data = None

    def fetch_remote_data(self):
        self.remote_data = self.todoist_api.sync()

    def dump_to_freeplane(self, data, file_location, left_side=list()):
        fp_doc = FreeplaneSchema()

        projects = data['projects']
        tasks = data['items']
        notes = data['notes']

        for prj in projects:
            if prj['parent_id'] is None:
                id_to_find = "root"
            else:
                id_to_find = str(prj['parent_id'])

            fp_doc.add_node_by_id(fp_doc.get_node_by_id(id_to_find), str(prj['id']))
            fp_doc.set_node_text_by_id(str(prj['id']), prj['name'])
            fp_doc.set_node_style_by_id(str(prj['id']), "bubble")
            if prj['name'] in left_side:
                fp_doc.set_node_position_by_id(str(prj['id']), 'left')

        for item in tasks:
            if isinstance(item, dict):
                id_to_find = str(item['project_id'])

                fp_doc.add_node_by_id(fp_doc.get_node_by_id(id_to_find), str(item['id']))
                fp_doc.set_node_text_by_id(str(item['id']), item['content'])
                fp_doc.set_node_style_by_id(str(item['id']), "fork")
            else:
                print("Trapped something interesting")

        for note in notes:
            fp_doc.add_node_note_by_id(str(note['item_id']), note['content'])

        fp_doc.write_document(file_location, pretty_print_it=True)


if __name__ == '__main__':
    # Load the configuration
    with open("todoist_2_freeplane_config.yml", 'r') as ymlfile:
        CFG = yaml.load(ymlfile, Loader=yaml.FullLoader)

    # Create Todoist document
    my_todoist = TodoistDocument(todoist_user=CFG['todoist_user'], todoist_password=CFG['todoist_passwd'])

    # Go get the data
    my_todoist.fetch_remote_data()

    # Dump the data in freeplane format
    my_todoist.dump_to_freeplane(my_todoist.remote_data, CFG['freeplane_location'] + "toto2.mm", CFG['left_side'])


# Notes:
# item_id maps to the task
# content is the content of the note (string, not html)