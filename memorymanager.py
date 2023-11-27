#Memory manger is responsible for memory allocation and deallocation for processes. 
#Memory blocks are managed using a free list, and blocks can be split and merged to
#delegate memory efficiently. 


import threading

class MemoryBlock:
    def __init__(self, start_address, size, synchronization):
        # Initialize a memory block with a start address, size, and no associated process
        self.start_address = start_address
        self.size = size
        self.process_id = None
        self.synchronization = synchronization 

class MemoryManager:
    def __init__(self, total_memory_size, synchronization):
        # Initialize the MemoryManager with total memory size, a free list containing the entire memory initially,
        # and a lock for thread safety
        self.total_memory_size = total_memory_size
        self.free_list = [MemoryBlock(0, total_memory_size, synchronization)]
        self.lock = threading.Lock()
        self.synchronization = synchronization  

    def allocate_memory(self, process_id, size):
        # Allocate memory for a process with the specified ID and size
        with self.lock:
            block_index = self.find_free_block(size)
            if block_index is not None:
                allocated_block = self.split_block(block_index, size, process_id)
                return allocated_block
            else:
                print(f"Not enough memory available for process {process_id}")
                return None

    def deallocate_memory(self, process_id):
        # Deallocate memory associated with a process
        with self.lock:
            for block in self.free_list:
                if block.process_id == process_id:
                    # Mark the block as unallocated and merge adjacent free blocks
                    block.process_id = None
                    print(f"Memory released for process {process_id}")

                    # Check if the process holds the shared resource and release it
                    if self.synchronization.shared_resource == process_id:
                        print(f"{process_id} is releasing the shared resource.")
                        self.synchronization.shared_resource = None
                        self.synchronization.condition.notify_all()

                    break  # Break out of the loop after deallocating memory

            self.merge_free_blocks()  # Merge adjacent free blocks outside the lock


    def find_free_block(self, size):
        # Find a free block that can accommodate the specified size
        for i, block in enumerate(self.free_list):
            if block.size >= size:
                return i
        return None

    def split_block(self, block_index, size, process_id):
        # Split a free block to allocate memory for a process
        block = self.free_list[block_index]
        remaining_size = block.size - size
        allocated_block = MemoryBlock(block.start_address, size, block.synchronization)
        allocated_block.process_id = process_id

        if remaining_size > 0:
            # If there is remaining space in the block, create a new free block
            new_block = MemoryBlock(block.start_address + size, remaining_size, block.synchronization)
            self.free_list.insert(block_index + 1, new_block)

        # Update the allocated block size and process ID
        block.start_address += size
        block.size -= size

        print(f"Memory allocated for process {process_id} - {allocated_block.start_address}-{allocated_block.start_address + allocated_block.size}")
        return allocated_block

    def merge_free_blocks(self):
        # Merge adjacent free blocks in the free list
        self.free_list.sort(key=lambda block: block.start_address)
        merged_list = [self.free_list[0]]

        for block in self.free_list[1:]:
            prev_block = merged_list[-1]

            if prev_block.start_address + prev_block.size == block.start_address:
                # Merge the current block with the previous block
                prev_block.size += block.size
            else:
                # Add the current block to the merged list
                merged_list.append(block)

        self.free_list = merged_list