import threading

# Shared variable
shared_variable = 0

# Lock to ensure exclusive access to the shared variable
lock = threading.Lock()

def thread_function():
    global shared_variable
    # Access the shared variable
    with lock:
        shared_variable += 1

# Create the thread
thread = threading.Thread(target=thread_function)

# Start the thread
thread.start()

# Access the shared variable from the main program
with lock:
    print(shared_variable)