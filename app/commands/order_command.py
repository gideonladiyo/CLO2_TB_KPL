from app.commands.base import Command
from app.helper.order_service import order_service
from app.models import OrderCreate

class GetAllOrdersCommand(Command):
    def execute(self):
        return order_service.get_all_orders()

class GetOrderByIdCommand(Command):
    def __init__(self, order_id: str):
        self.order_id = order_id

    def execute(self):
        return order_service.get_order(self.order_id)

class CreateOrderCommand(Command):
    def __init__(self, order_data: OrderCreate):
        self.order_data = order_data

    def execute(self):
        return order_service.create_order(self.order_data)

class ChangeOrderStatusCommand(Command):
    def __init__(self, order_id: str, trigger: str):
        self.order_id = order_id
        self.trigger = trigger

    def execute(self):
        order_service.change_order_state(id=self.order_id, trigger=self.trigger)
        return order_service.get_order(self.order_id)