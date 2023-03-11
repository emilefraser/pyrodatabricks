from binary_search_trees_traversals_balancing.exercise.binary_tree_implementation import display_keys
from binary_search_trees_traversals_balancing.exercise.height_of_tree import tree_height
from binary_search_trees_traversals_balancing.exercise.user_registration import User
from binary_search_trees_traversals_balancing.exercise.verify_binary_search_tree import BSTNode
from test_data import tree_tuple, jadhesh, biraj, sonaksh, rushikesh, aakash, siddhant, hemanth, vishal


def insert(node, key, value):
    '''Node Insertion function'''
    if node is None:
        node = BSTNode(key, value)
    elif key < node.key:
        node.left = insert(node.left, key, value)
        node.left.parent = node
    elif key > node.key:
        node.right = insert(node.right, key, value)
        node.right.parent = node
    return node


def find(node, key):
    '''Finding Node in BST'''
    if node is None:
        return None
    if key == node.key:
        return node
    if key < node.key:
        return find(node.left, key)
    if key > node.key:
        return find(node.right, key)


def update(node, key, value):
    '''Updating value in BST'''
    target = find(node, key)
    if target is not None:
        target.value = value


def list_all_node(node):
    '''List all present nodes'''
    if node is None:
        return []
    return list_all_node(node.left) + [(node.key, node.value)] + list_all_node(node.right)


def is_balanced(node):
    '''Checking for is tree balanced or not'''
    if node is None:
        return True, 0
    balanced_l, height_l = is_balanced(node.left)
    balanced_r, height_r = is_balanced(node.right)
    balanced = balanced_l and balanced_r and abs(height_l - height_r) <=1
    height = 1 + max(height_l, height_r)
    return balanced, height


if __name__ == "__main__":
    tree = insert(None, jadhesh[0], jadhesh)
    insert(tree, biraj[0], biraj)
    insert(tree, rushikesh[0], rushikesh)
    insert(tree, sonaksh[0], sonaksh)
    insert(tree, aakash[0], aakash)
    insert(tree, hemanth[0], hemanth)
    insert(tree, siddhant[0], siddhant)
    insert(tree, vishal[0], siddhant)
    tree_keys = display_keys(tree)
    print(f"Tree Keys after insertion, {tree_keys}")
    tree2 = insert(None, aakash[0], aakash)
    insert(tree2, biraj[0], biraj)
    insert(tree2, hemanth[0], hemanth)
    insert(tree2, jadhesh[0], jadhesh)
    insert(tree2, siddhant[0], siddhant)
    insert(tree2, sonaksh[0], sonaksh)
    insert(tree2, vishal[0], vishal)
    tree2_keys = display_keys(tree2)
    # the order of insertion of nodes change the structure of the resulting tree.
    print(f"keys, {tree2_keys}")
    print(f"Tree Height, {tree_height(tree2)}")
    node = find(tree, 'hemanth')
    print(f"Node key, {node.key}, Node Value, {node.value}")
    update(tree, 'hemanth', User('hemanth', 'Hemanth J', 'hemanthj@example.com'))
    node = find(tree, 'hemanth')
    print(f"Node Value, {node.value}")
    all_nodes = list_all_node(tree)
    print(f"List all Nodes, {all_nodes}")
    result = is_balanced(tree)
    print(f"Is tree balanced, {result}")
    result = is_balanced(tree2)
    print(f"Is tree2 balanced, {result}")
    
