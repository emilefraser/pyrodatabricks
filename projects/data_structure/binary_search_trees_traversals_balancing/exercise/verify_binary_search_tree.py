from binary_search_trees_traversals_balancing.exercise.user_registration import User
from binary_tree_implementation import parse_tuple, display_keys
from test_data import tree_tuple, jadhesh, biraj, sonaksh


def remove_none(nums):
    return [x for x in nums if x is not None]


def is_bst(node):
    if node is None:
        return True, None, None

    is_bst_l, min_l, max_l = is_bst(node.left)
    is_bst_r, min_r, max_r = is_bst(node.right)

    is_bst_node = (is_bst_l and is_bst_r and
                   (max_l is None or node.key > max_l) and
                   (min_r is None or node.key < min_r))

    min_key = min(remove_none([min_l, node.key, min_r]))
    max_key = max(remove_none([max_l, node.key, max_r]))

    # print(node.key, min_key, max_key, is_bst_node)

    return is_bst_node, min_key, max_key


class BSTNode(object):
    def __init__(self, key, value=None):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.parent = None


if __name__ == "__main__":
    tree = parse_tuple(tree_tuple)
    result = is_bst(tree)
    print(f"Is this tree is BST, {result}")
    tree1 = parse_tuple((('rushikesh', 'biraj', 'hemanth'), 'jadhesh', ('siddhant', 'sonaksh', 'vishal')))
    result = is_bst(tree1)
    print(f"\nIs this tree is BST, {result}")
    jadhesh = User(jadhesh[0], jadhesh[1], jadhesh[2])
    biraj = User(biraj[0], biraj[1], biraj[2])
    sonaksh = User(sonaksh[0], sonaksh[1], sonaksh[2])
    tree = BSTNode(jadhesh.username, jadhesh)
    print(f"tree key {tree.key} and value {tree.value}")
    tree.left = BSTNode(biraj.username, biraj)
    tree.right = BSTNode(sonaksh.username, sonaksh)
    print(f"tree left key, {tree.left.key}, tree left value, {tree.left.value}, "
          f"tree right key, {tree.right.key}, tree right value, {tree.right.value}")
    display_keys(tree)

