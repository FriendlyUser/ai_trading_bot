
loop_count = 0

def get_loop_count():
    return loop_count

def increment_loop_count():
    global loop_count
    return loop_count + 1

def set_loop_count(new_value):
    global loop_count
    loop_count = new_value

def reset_loop_count():
    global loop_count
    loop_count = 0
