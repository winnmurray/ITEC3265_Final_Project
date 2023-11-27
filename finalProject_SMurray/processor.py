#The processor class is responsible for initializing, scheduling, and executing processes. 
#It takes in processes from process_generator and schedules them using first-come first-serve scheduling.


import time
import random
import threading


class Process:
    def __init__(self, name, burst_time, priority, memory_required):
        self.name = name
        self.burst_time = burst_time
        self.priority = priority
        self.memory_required = memory_required

class Processor:
    def __init__(self, synchronization, memory_manager):
        self.process_queue = []
        self.synchronization = synchronization
        self.memory_manager = memory_manager

    def add_process(self, process):
        self.process_queue.append(process)

    def execute_process(self):
        while True:
            self.schedule_fcfs()

    def schedule_fcfs(self):
        if not self.process_queue:
            return

        process = self.process_queue.pop(0)
        process_name = process.name

        print(f"Processor: Executing {process_name} with priority {process.priority} and burst time {process.burst_time}. Its size is {process.memory_required}")
        self.synchronization.access_shared_resource(process_name, self.memory_manager, process.memory_required)
        time.sleep(process.burst_time)
        self.memory_manager.deallocate_memory(process_name)  # Release memory after the process completes
        self.synchronization.release_shared_resource(process_name, self.memory_manager)
        print(f"Processor: {process_name} completed")


#the process_generator function generates random integer values for processes. The number of processes generated
#is determined by the number in range(x)
def process_generator(processor, synchronization):
    for i in range(100):
        name = f"Process-{i + 1}"
        burst_time = random.randint(1, 5)
        priority = random.randint(1, 5)
        memory_required = random.randint(10, 30)
        process = Process(name, burst_time, priority, memory_required)
        processor.add_process(process)
        print(f"{name} has been scheduled.")
        time.sleep(0.5)

