import threading

# Function that performs a lot of computation
def heavy_computation():
    result = 0
    for i in range(10**8):  # Performing a very large number of computations
        result += i
    print(f"Result: {result}")

# Creating threads to run heavy_computation function
threads = []
for _ in range(10):  # Creating 10 threads
    thread = threading.Thread(target=heavy_computation)
    threads.append(thread)

# Starting threads
for thread in threads:
    thread.start()

# Waiting for all threads to complete
for thread in threads:
    thread.join()
