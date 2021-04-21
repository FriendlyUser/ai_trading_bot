# loop count for tracking iterations for timer events
loop_count = 0
# global state counter
counter = 0

def increment_counter():
    global counter
    counter = counter + 1

def get_counter():
    return counter

def get_loop_count():
    return loop_count

def increment_loop_count():
    global loop_count
    global counter
    return loop_count + 1

def set_loop_count(new_value):
    global loop_count
    loop_count = new_value

def reset_loop_count():
    global loop_count
    loop_count = 0


