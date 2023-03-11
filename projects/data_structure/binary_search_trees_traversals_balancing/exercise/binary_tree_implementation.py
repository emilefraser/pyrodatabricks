from test_data import tree_tuple


class TreeNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


def parse_tuple(data):
    print(data)
    if isinstance(data, tuple) and len(data) == 3:
        node = TreeNode(data[1])
        node.left = parse_tuple(data[0])
        node.right = parse_tuple(data[2])
    elif data is None:
        node = None
    else:
        node = TreeNode(data)
    return node


def display_keys(node, space='\t', level=0):
    # print(node.key if node else None, level)
    # If the node is empty
    if node is None:
        print(space * level + '∅')
        return
        # If the node is a leaf
    if node.left is None and node.right is None:
        print(space * level + str(node.key))
        return
    # If the node has children
    display_keys(node.right, space, level + 1)
    print(space * level + str(node.key))
    display_keys(node.left, space, level + 1)


if __name__ == "__main__":
    node0 = TreeNode(2)
    node1 = TreeNode(3)
    node2 = TreeNode(4)
    print(f"\nnode0, {node0}")
    print(f"\nnode0 Key, {node0.key}")
    node0.left = node1
    node0.right = node2
    tree = node0
    print(f"\nKey is {tree.key}, left, {tree.left}, right, {tree.right}")

    # Binary Tree
    tree2 = parse_tuple(tree_tuple)
    print(f"{tree2}")
    print(f"tree key, {tree2.key}")
    print(f"tree left key, {tree2.left.key} , tree right key, {tree2.right.key}")
    print(f"tree left left key, {tree2.left.left.key}, tree left right key {tree2.left.right}, "
          f"tree right left key, {tree2.right.left.key}, tree right right key, {tree2.right.right.key}")
    print(f"tree right left right key, {tree2.right.left.right.key}, tree right right left key{tree2.right.right.left.key},"
          f"tree right right right key, {tree2.right.right.right.key}")
    print(f"\n\nPrinting tree structure nodes")
    display_keys(tree2, ' ')

