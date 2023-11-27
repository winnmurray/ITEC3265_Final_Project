#The synchronization class is responsible for making sure that the processor and memorymanager classes 
#work in synchronicity. It's main responsibilities include coordinating access to shared resources
#among multiple threads, enforcing mutual exclusion, and managing thread synchronizaiton. 


import threading
import time
import random

class Synchronization:
    def __init__(self):
        # Initialize the shared resource and synchronization objects
        self.shared_resource = None
        self.mutex = threading.Lock()  # Mutex for mutual exclusion
        self.condition = threading.Condition(self.mutex)  # Condition variable associated with the mutex

    def access_shared_resource(self, process_name, memory_manager, memory_required):
        # Acquire the lock associated with the condition variable
        with self.condition:
            # Wait while the shared resource is already being accessed by another process
            while self.shared_resource is not None:
                print(f"{process_name} waiting for the shared resource to be available.")
                self.condition.wait()

            # The shared resource is available; the process can access it
            print(f"{process_name} is accessing the shared resource.")
            time.sleep(random.randint(1, 3))

            # Simulate memory allocation by generating a random memory requirement
            allocated_memory = memory_manager.allocate_memory(process_name, memory_required)

            if allocated_memory:
                # Memory allocation successful
                print(f"{process_name} has allocated {memory_required} units of memory.")
                self.shared_resource = process_name
                print(f"{process_name} has finished accessing the shared resource.")
                self.condition.notify_all()  # Notify all waiting processes that the shared resource is available
            else:
                # Memory allocation failed; release the shared resource
                print(f"{process_name} failed to allocate memory. Releasing shared resource.")
                self.shared_resource = None
                self.condition.notify_all()  # Notify all waiting processes that the shared resource is available

    def release_shared_resource(self, process_name, memory_manager):
        # Acquire the lock associated with the condition variable
        with self.condition:
            # Release the shared resource and perform memory deallocation
            print(f"{process_name} is releasing the shared resource.")
            memory_manager.deallocate_memory(process_name)
            self.shared_resource = None
            self.condition.notify_all()  # Notify all waiting processes that the shared resource is available

