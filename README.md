# ITEC3265_Final_Project

## 1. Main Program (main.py)

The main program serves as the entry point for the system. It is responsible for the execution of the simulation by creating instances of the Synchronization, MemoryManager, and Processor classes. It then initializes two threads: one for process generation (process_generator) and another for process execution (processor.execute_process). The main program ensures that both threads complete their tasks before terminating.
### 1.1 Classes Used

    Synchronization: Manages access to shared resources, including a shared memory block.

    MemoryManager: Allocates and deallocates memory for processes, maintaining a free list to manage available memory blocks.

    Processor: Executes processes based on a first-come-first-serve scheduling algorithm, coordinating with the Synchronization and MemoryManager classes.

### 1.2 Thread Execution

    Process Generation Thread (process_thread):
        Invokes the process_generator function in the processor module.
        Generates random processes with varying burst times, priorities, and memory requirements.
        Adds the generated processes to the Processor instance.

    Process Execution Thread (execute_thread):
        Calls the processor.execute_process method in an infinite loop.
        Executes processes using a first-come-first-serve scheduling algorithm.
        Manages memory allocation and deallocation using the MemoryManager.
        Coordinates access to shared resources through the Synchronization class.

### 1.3 Program Termination

The main program ensures that both threads complete their execution by using the join() method on each thread. This guarantees a clean termination of the program after all processes have been generated and executed.
## 2. Processor (processor.py)

The Processor class is responsible for executing processes based on a first-come-first-serve scheduling algorithm. It interacts with the Synchronization and MemoryManager classes to coordinate access to shared resources and manage memory allocation and deallocation.
### 2.1 Class Components

    Process Queue (process_queue): Maintains a queue of processes waiting to be executed.

    Synchronization (synchronization): Manages access to shared resources, including a shared memory block.

    MemoryManager (memory_manager): Allocates and deallocates memory for processes.

### 2.2 Methods

    add_process(process): Adds a process to the process queue for execution.

    execute_process(): Infinitely executes processes using first-come-first-serve scheduling.

    schedule_fcfs(): Implements the logic for scheduling processes based on their arrival order.
        Retrieves a process from the process queue.
        Accesses the shared resource and allocates memory using the MemoryManager.
        Executes the process for its burst time.
        Deallocates memory and releases the shared resource.

### 2.3 Execution Logic

The Processor class continuously executes processes in the order they arrive. It coordinates with the MemoryManager for memory allocation and deallocation and interacts with the Synchronization class to access shared resources in a controlled manner.
## 3. Synchronization (synchronization.py)

The Synchronization class provides mechanisms for coordinating access to shared resources among multiple threads. It uses a mutex and a condition variable to enforce mutual exclusion and manage thread synchronization.
### 3.1 Class Components

    Shared Resource (shared_resource): Represents the resource shared among processes.

    Mutex (mutex): Ensures mutual exclusion by allowing only one thread to access the critical section at a time.

    Condition Variable (condition): Enables threads to wait and notify each other about changes in the shared resource.

### 3.2 Methods

    access_shared_resource(process_name, memory_manager, memory_required): Controls access to the shared resource.
        Waits if the shared resource is already in use.
        Allows access once the resource becomes available.
        Simulates memory allocation and notifies waiting threads.

    release_shared_resource(process_name, memory_manager): Releases the shared resource.
        Notifies waiting threads about the availability of the shared resource.

### 3.3 Usage

The Synchronization class is used by the Processor and MemoryManager classes to coordinate access to shared resources, ensuring that processes do not interfere with each other.
## 4. MemoryManager (memory_manager.py)

The MemoryManager class handles memory allocation and deallocation for processes. It maintains a free list of memory blocks, and it uses a lock to ensure thread safety when accessing and modifying the free list.
### 4.1 Class Components

    Total Memory Size (total_memory_size): Represents the total available memory in the system.

    Free List (free_list): Manages memory blocks, both allocated and unallocated.

    Lock (lock): Ensures thread safety when modifying the free list.

### 4.2 Methods

    allocate_memory(process_id, size): Allocates memory for a process with the specified ID and size.

    deallocate_memory(process_id): Deallocates memory associated with a process and releases the shared resource if necessary.

    find_free_block(size): Finds a free block that can accommodate the specified size.

    split_block(block_index, size, process_id): Splits a free block to allocate memory for a process.

    merge_free_blocks(): Merges adjacent free blocks in the free list.

### 4.3 Usage

The MemoryManager class is utilized by the Processor class for memory allocation and deallocation. It interacts with the Synchronization class to coordinate access to shared resources.
