from binary_search_trees_traversals_balancing.assignment.dictionary_and_hash_tables import get_index


class HashTable:
    def __init__(self, max_size=0):
        self.data_list = [None] * max_size

    def get_valid_index(self, key):
        # Use Python's in-built `hash` function and implement linear probing
        idx = get_index(self.data_list, key)
        while True:
            # Get the key-value pair stored at idx
            try:
                kv = self.data_list[idx]
            except IndexError:
                kv = None

            # If it is None, return the index
            if kv is None:
                return idx

            # If the stored key matches the given key, return the index
            k, v = kv
            if k == key[0]:
                return idx

            # Move to the next index
            idx += 1

            # Go back to the start if you have reached the end of the array
            if idx == len(self.data_list):
                idx = 0

    def __getitem__(self, key):
        # Implement the logic for "find" here
        idx = self.get_valid_index(key)
        kv = self.data_list[idx]
        return None if kv is None else kv[1]

    def __setitem__(self, key, value):
        # Implement the logic for "insert/update" here
        idx = self.get_valid_index(key)
        self.data_list[idx] = (key, value)

    def __iter__(self):
        return (x for x in self.data_list if x is not None)

    def __len__(self):
        return len([x for x in self])

    def __repr__(self):
        from textwrap import indent
        pairs = [indent("{} : {}".format(repr(kv[0]), repr(kv[1])), '  ') for kv in self]
        return "{\n" + "{}".format(',\n'.join(pairs)) + "\n}"

    def __str__(self):
        return self.__repr__()


if __name__ == "__main__":
    # Create a hash table
    table = HashTable(4096)

    # Insert some key-value pairs
    table['a'] = 1
    table['b'] = 34

    # Retrieve the inserted values
    print("\nRetrieve status of inserted values, ", table['a'] == 1 and table['b'] == 34)

    # Update a value
    table['a'] = 99

    # Check the updated value
    print("\nchecking updated value, ", table['a'] == 99)

    # Get a list of key-value pairs
    print("\nKey-Value Pairs List, ", list(table) == [('a', 99), ('b', 34)])

    print("\nprints tables values, ", table)

