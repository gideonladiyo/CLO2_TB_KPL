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
    if current_state in order_transitions and trigger in order_transitions[current_state]:
        return order_transitions[current_state][trigger]
    return None  # atau bisa raise Exception("Invalid transition")