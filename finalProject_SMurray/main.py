#Stephen Murray
#ITEC3265

#The program is separated into 4 files for organizational purposes. 

#Main serves as the entry point to the system. It is responsible for the execution of the
#simulation by creating instances of the Synchronization, MemoryManager, and Processor
#classes. 


import threading
from processor import Processor, process_generator
from memorymanager import MemoryManager
from synchronization import Synchronization

if __name__ == "__main__":
    total_memory_size = 100

    # Create instances of synchronization, memory manager, and processor
    synchronization = Synchronization()
    memory_manager = MemoryManager(total_memory_size, synchronization) 
    processor = Processor(synchronization, memory_manager)

    # Create threads for process generation and process execution
    process_thread = threading.Thread(target=process_generator, args=(processor, synchronization))
    execute_thread = threading.Thread(target=processor.execute_process)

    # Start the threads
    process_thread.start()
    execute_thread.start()

    # Wait for the threads to finish
    process_thread.join()
    execute_thread.join()

