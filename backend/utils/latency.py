import time

def measure_latency(start_tick):
    return round((time.perf_counter() - start_tick) * 1000, 3)  # ms
