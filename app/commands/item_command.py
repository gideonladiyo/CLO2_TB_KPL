from app.commands.base import Command
from app.helper.item_service import item_service

class GetItemsCommand(Command):
    def execute(self):
        return item_service.get_all_items()

class GetItemCommand(Command):
    def __init__(self, item_id):
        self.item_id = item_id
    def execute(self):
        return item_service.get_item(self.item_id)

class CreateItemCommand(Command):
    def __init__(self, item_data):
        self.item_data = item_data

    def execute(self):
        return item_service.create_item(self.item_data)

class UpdateItemCommand(Command):
    def __init__(self, item_id, item_data):
        self.item_id = item_id
        self.item_data = item_data
    def execute(self):
        return item_service.update_item(self.item_id, self.item_data)

class DeleteItemCommand(Command):
    def __init__(self, item_id):
        self.item_id = item_id
    def execute(self):
        return item_service.delete_item(self.item_id)