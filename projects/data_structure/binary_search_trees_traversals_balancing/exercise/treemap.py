from binary_search_trees_traversals_balancing.exercise.binary_tree_implementation import display_keys
from binary_search_trees_traversals_balancing.exercise.create_balanced_bst import balance_bst
from binary_search_trees_traversals_balancing.exercise.height_of_tree import tree_size
from binary_search_trees_traversals_balancing.exercise.insert_into_bst import find, insert, update, list_all_node
from binary_search_trees_traversals_balancing.exercise.user_registration import User
from test_data import users, rushikesh, jadhesh, sonaksh


class TreeMap():
    def __init__(self):
        self.root = None

    def __setitem__(self, key, value):
        node = find(self.root, key)
        if not node:
            self.root = insert(self.root, key, value)
            self.root = balance_bst(self.root)
        else:
            update(self.root, key, value)

    def __getitem__(self, key):
        node = find(self.root, key)
        return node.value if node else None

    def __iter__(self):
        return (x for x in list_all_node(self.root))

    def __len__(self):
        return tree_size(self.root)

    def display(self):
        return display_keys(self.root)


if __name__ == "__main__":
    print(f"Printing Users, {users}\n")
    treemap = TreeMap()
    print(f"treemap display, {treemap.display()}\n")
    treemap['rushikesh'] = rushikesh
    treemap['jadhesh'] = jadhesh
    treemap['sonaksh'] = sonaksh
    print(f"treemap display, {treemap.display()}\n")
    result = treemap['jadhesh']
    print(f"result of treemap of jadhesh, {result}\n")
    print(f"length of treemap, {len(treemap)}\n")
    print(f"treemap display, {treemap.display()}\n")
    for key, value in treemap:
        print(key, value)
    print(f"list of treemap, {list(treemap)}\n")
    treemap['rushikesh'] = User(username='rushikesh', name='Rushikesh V M', email='rushikesh@example.com')
    result = treemap['rushikesh']
    print(f"\nresult of treemap after update, {result}")

