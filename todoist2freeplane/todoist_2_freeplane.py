import todoist
import yaml
import pprint as pp

from freeplane_schema.freeplane_schema import FreeplaneSchema

#Load the configuration
with open("todoist_2_freeplane_config.yml", 'r') as ymlfile:
    CFG = yaml.load(ymlfile, Loader=yaml.FullLoader)

# Establishing connection with Todoist
todoist_api=todoist.TodoistAPI()
todoist_api.user.login(CFG['todoist_user'],CFG['todoist_passwd'])

# Creating a Freeplane Document in memory
fp_doc = FreeplaneSchema()

todoist_all_data = todoist_api.sync()
todoist_project_data = todoist_all_data['projects']
todoist_item_data = todoist_all_data['items']
todoist_notes_data = todoist_all_data['notes']

for prj in todoist_project_data:
    # print(prj['parent_id'])
    # print(prj['name'])
    if prj['parent_id'] is None:
        id_to_find = "root"
    else:
        id_to_find = str(prj['parent_id'])

    fp_doc.add_node_by_id(fp_doc.get_node_by_id(id_to_find), str(prj['id']))
    fp_doc.set_node_text_by_id(str(prj['id']), prj['name'])
    fp_doc.set_node_style_by_id(str(prj['id']), "bubble")
    if prj['name'] in CFG['left_side']:
        fp_doc.set_node_position_by_id(str(prj['id']), 'left')


for item in todoist_item_data:
    if isinstance(item, dict):
        id_to_find = str(item['project_id'])

        fp_doc.add_node_by_id(fp_doc.get_node_by_id(id_to_find), str(item['id']))
        fp_doc.set_node_text_by_id(str(item['id']), item['content'])
        fp_doc.set_node_style_by_id(str(item['id']), "fork")
    else:
        print("Trapped something interesting")


for notes in todoist_notes_data:
    fp_doc.add_node_note_by_id(str(notes['item_id']), notes['content'])



fp_doc.write_document(CFG['freeplane_location'] + "toto.mm")


# Notes:
# item_id maps to the task
# content is the content of the note (string, not html)