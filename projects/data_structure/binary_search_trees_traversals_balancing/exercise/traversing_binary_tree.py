from test_data import tree_tuple
from binary_tree_implementation import parse_tuple, display_keys


def traverse_in_order(node):
    if node is None:
        return []
    return(traverse_in_order(node.left) +
           [node.key] +
           traverse_in_order(node.right))


def traverse_preorder(node):
    if node is None:
        return []
    return([node.key] +
           traverse_preorder(node.left) +
           traverse_preorder(node.right))


def traverse_postorder(node):
    if node is None:
        return []
    return (traverse_postorder(node.right) +
            [node.key] + traverse_postorder(node.left))


def tree_to_tuple(node):
    if node is None:
        return None
    if node.left is None and node.right is None:
        return node.key
    return tree_to_tuple(node.left), node.key, tree_to_tuple(node.right)


if __name__ == "__main__":
    tree = parse_tuple(((1, 3, None), 2, ((None, 3, 4), 5, (6, 7, 8))))
    display_keys(tree, ' ')
    print("Traversing Inorder Tree")
    inorder = traverse_in_order(tree)
    print(f"Inorder Traversed nodes list, {inorder} \n")
    print("Traversing Preorder Tree")
    preorder = traverse_preorder(tree)
    print(f"Preorder Traversed nodes list, {preorder} \n")
    print("Traversing Postorder Tree")
    postorder = traverse_postorder(tree)
    print(f"Postorder Traversed nodes list, {postorder} \n")
    print("Convert Binary tree to Tuple.")
    to_tuple = tree_to_tuple(tree)
    print(f"Tuple values, {to_tuple}")

