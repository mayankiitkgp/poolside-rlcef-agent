"""
Bug Description: Tree traversal missing None check
Category: recursion
Difficulty: medium
Expected Fix: Add check for None node before accessing attributes
"""

BUGGY_CODE = '''
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def inorder_traversal(root):
    result = []
    result.extend(inorder_traversal(root.left))  # Missing None check
    result.append(root.val)
    result.extend(inorder_traversal(root.right))
    return result
'''

TEST_CODE = '''
import sys
sys.path.insert(0, '.')
from temp_module import TreeNode, inorder_traversal

def test_single_node():
    root = TreeNode(1)
    assert inorder_traversal(root) == [1]

def test_left_child():
    root = TreeNode(2, TreeNode(1))
    assert inorder_traversal(root) == [1, 2]

def test_full_tree():
    root = TreeNode(2, TreeNode(1), TreeNode(3))
    assert inorder_traversal(root) == [1, 2, 3]

def test_empty_tree():
    assert inorder_traversal(None) == []

'''

if __name__ == "__main__":
    print(f"Bug ID: bug_003")
    print(f"Description: Tree traversal missing None check")
    print(f"Category: recursion")
    print(f"Difficulty: medium")
    print("\nBuggy Code:")
    print(BUGGY_CODE)
    print("\nTest Code:")
    print(TEST_CODE)
