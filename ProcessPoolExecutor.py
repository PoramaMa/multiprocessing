from concurrent.futures import ProcessPoolExecutor

# Function that performs a lot of computation
def heavy_computation():
    result = 0
    for i in range(10**8):  # Performing a very large number of computations
        result += i
    print(f"Result: {result}")

# Creating a ProcessPoolExecutor with 10 processes
with ProcessPoolExecutor(max_workers=10) as executor:
    # Submitting heavy_computation function 10 times to the pool
    futures = [executor.submit(heavy_computation) for _ in range(1)]

    # Gathering results (optional)
    for future in futures:
        result = future.result()
        print(f"Got result: {result}")
