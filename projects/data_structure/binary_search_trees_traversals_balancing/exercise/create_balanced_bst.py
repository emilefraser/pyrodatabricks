import cProfile
import math
from binary_search_trees_traversals_balancing.exercise.binary_tree_implementation import display_keys
from binary_search_trees_traversals_balancing.exercise.insert_into_bst import insert, list_all_node
from binary_search_trees_traversals_balancing.exercise.verify_binary_search_tree import BSTNode
from test_data import users


def make_balanced_bst(data, lo=0, hi=None, parent=None):
    '''To create a balanced BST from a sorted list/array of key-value pairs'''
    if hi is None:
        hi = len(data) - 1
    if lo > hi:
        return None

    mid = (lo + hi) // 2
    key, value = data[mid]

    root = BSTNode(key, value)
    root.parent = parent
    root.left = make_balanced_bst(data, lo, mid -1, root)
    root.right = make_balanced_bst(data, mid +1, hi, root)

    return root


def balance_bst(node):
    return make_balanced_bst(list_all_node(node))


if __name__ == "__main__":
    data = [(user[0], user) for user in users]
    print(f"Print all users list, {data}")
    tree = make_balanced_bst(data)
    display_keys(tree)
    tree3 = None
    for username, user in data:
        tree3 = insert(tree3, username, user)
    tree1 = None
    for user in users:
        tree1 = insert(tree1, user[0], user)
    print(f"\nDisplaying tree1 unbalanced \n")
    display_keys(tree1)
    tree2 = balance_bst(tree1)
    print("\nDisplaying tree2 by making balanced tree1\n")
    display_keys(tree2)
    print("\nTesting Thoroughly\n")
    output = math.log(100000000, 2)
    print(f"Test output, {output}")
    
    # Testing Thoroughly to check system performance
    cProfile.run("c = [i*i for i in range(100000000)]")

