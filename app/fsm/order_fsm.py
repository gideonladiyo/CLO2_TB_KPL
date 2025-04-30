from enum import Enum
from fastapi import HTTPException


class OrderState(Enum):
    NEW = "New"
    PAID = "Paid"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"
    CANCELED = "Canceled"


class OrderTrigger(Enum):
    PAY = "Pay"
    SHIP = "Ship"
    DELIVER = "Deliver"
    CANCEL = "Cancel"


order_transitions = {
    OrderState.NEW: {
        OrderTrigger.PAY: OrderState.PAID,
        OrderTrigger.CANCEL: OrderState.CANCELED,
    },
    OrderState.PAID: {
        OrderTrigger.SHIP: OrderState.SHIPPED,
    },
    OrderState.SHIPPED: {
        OrderTrigger.DELIVER: OrderState.DELIVERED,
    },
}


def change_order_state(current_state, trigger):
    if isinstance(current_state, str):
        try:
            current_state = OrderState[current_state]
        except (KeyError, ValueError):
            raise HTTPException(status_code=400,detail=f"Invalid current state: {current_state}")

    if isinstance(trigger, str):
        try:
            trigger = OrderTrigger[trigger]
        except (KeyError, ValueError):
            raise HTTPException(status_code=400, detail=f"Invalid trigger: {trigger}")

    if (current_state in order_transitions and trigger in order_transitions[current_state]):
        return order_transitions[current_state][trigger]

    raise HTTPException(
        status_code=422,
        detail=f"Invalid transition from {current_state.name} using {trigger.name}",
    )