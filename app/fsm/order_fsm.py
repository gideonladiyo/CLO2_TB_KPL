from enum import Enum

class OrderState(Enum):
    NEW = "New"
    PAID = "Paid"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"

class OrderTrigger(Enum):
    PAY = "Pay"
    SHIP = "Ship"
    DELIVER = "Deliver"

order_transitions = {
    OrderState.NEW: {
        OrderTrigger.PAY: OrderState.PAID,
    },
    OrderState.PAID: {
        OrderTrigger.SHIP: OrderState.SHIPPED,
    },
    OrderState.SHIPPED: {
        OrderTrigger.DELIVER: OrderState.DELIVERED,
    }
}

def change_order_state(current_state, trigger):
    if isinstance(current_state, str):
        try:
            current_state = OrderState[current_state]
        except ValueError:
            raise ValueError(f"Invalid current state: {current_state}")

    if isinstance(trigger, str):
        try:
            trigger = OrderTrigger[trigger]
        except ValueError:
            raise ValueError(f"Invalid trigger: {trigger}")

    if (
        current_state in order_transitions
        and trigger in order_transitions[current_state]
    ):
        return order_transitions[current_state][trigger]
    raise Exception("Invalid transition")