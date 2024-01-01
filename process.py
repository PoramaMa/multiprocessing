import multiprocessing

# Function that performs a lot of computation
def heavy_computation():
    result = 0
    for i in range(10**8):  # Performing a very large number of computations
        result += i
    print(f"Result: {result}")

if __name__ == "__main__":
    # Creating a pool of processes with 10 workers
    with multiprocessing.Pool(processes=10) as pool:
        # Mapping the heavy_computation function to the pool
        pool.map(heavy_computation, range(10))
