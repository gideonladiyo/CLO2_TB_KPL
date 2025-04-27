from fsm.order_fsm import OrderState, OrderTrigger, change_order_state

current_state = OrderState.NEW
print(f"Current: {current_state}")

current_state = change_order_state(current_state, OrderTrigger.PAY)
print(f"After paying: {current_state}")

current_state = change_order_state(current_state, OrderTrigger.SHIP)
print(f"After shipping: {current_state}")

current_state = change_order_state(current_state, OrderTrigger.DELIVER)
print(f"After delivering: {current_state}")