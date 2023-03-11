from test_data import tree_tuple
from binary_tree_implementation import parse_tuple


def tree_height(node):
    '''To calculate height of the tree'''
    if node is None:
        return 0
    return 1 + max(tree_height(node.left), tree_height(node.right))


def tree_size(node):
    '''Here's a function to count the number of nodes in a binary tree.'''
    if node is None:
        return 0
    return 1 + tree_size(node.left) + tree_size(node.right)


if __name__ == "__main__":
    tree = parse_tuple(tree_tuple)
    height = tree_height(tree)
    print(f"height of Tree, {height}")
    size = tree_size(tree)
    print(f"Size of Tree, {size}")


