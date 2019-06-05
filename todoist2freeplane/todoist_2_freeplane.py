import todoist
import logging

from freeplane_schema.freeplane_schema import FreeplaneSchema


class TodoistDocument(object):
    def __init__(self, todoist_user, todoist_password, logger=None):
        self.todoist_api = todoist.TodoistAPI()
        self.todoist_api.user.login(todoist_user, todoist_password)
        self.remote_data = None

        self._logger = (logger or self._build_logger())

    @property
    def logger(self):
        return self._logger

    def _build_logger(self):
        logger = logging.getLogger(self.__module__)
        logger.addHandler(logging.NullHandler())
        return logger

    def fetch_remote_data(self):
        self.remote_data = self.todoist_api.sync()

    def dump_to_freeplane(self, data, file_location, left_side=list()):
        fp_doc = FreeplaneSchema(inherited_logger=self.logger)

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

                try:
                    fp_doc.add_node_by_id(fp_doc.get_node_by_id(id_to_find), str(item['id']))
                except fp_doc.FreeplaneExpectedParentNode:
                    pass
                except fp_doc.FreeplaneNodeNotExisting:
                    pass

                try:
                    fp_doc.set_node_text_by_id(str(item['id']), item['content'])
                except fp_doc.FreeplaneExpectedParentNode:
                    raise self.TodoistDocumentDataCorruption
                except fp_doc.FreeplaneNodeNotExisting:
                    raise self.TodoistDocumentDataCorruption

                try:
                    fp_doc.set_node_style_by_id(str(item['id']), "fork")
                except fp_doc.FreeplaneExpectedParentNode:
                    pass
                except fp_doc.FreeplaneNodeNotExisting:
                    pass

            else:
                print("Trapped something interesting")

        for note in notes:
            try:
                fp_doc.add_node_note_by_id(str(note['item_id']), note['content'])
            except fp_doc.FreeplaneExpectedParentNode:
                pass
            except fp_doc.FreeplaneNodeNotExisting:
                pass

        fp_doc.write_document(file_location, pretty_print_it=True, add_map_styles=True)


    class TodoistDocumentError(Exception):
        """
        General Exception for TodoistDocument
        """

    class TodoistDocumentDataCorruption(TodoistDocumentError):
        """
        Assumption made on the document structure appears to be invalud which point to corrupted data
        """
