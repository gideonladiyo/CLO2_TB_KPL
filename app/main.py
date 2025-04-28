from fsm.order_fsm import *

current_status = "NEW"
trigger = "PAY"

new_state = change_order_state(current_status, trigger)
print(new_state)
print(new_state.name)