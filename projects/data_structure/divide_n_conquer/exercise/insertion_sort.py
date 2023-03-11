from tests import *


def insertion_sort(nums):
    nums = list(nums)
    for i in range(len(nums)):
        cur = nums.pop(i)
        j = i-1
        while j >=0 and nums[j] > cur:
            j -= 1
        nums.insert(j+1, cur)
    return nums


if __name__ == "__main__":
    nums0, output0 = random_test0['input']['nums'], random_test0['output']

    print('Input:', nums0)
    print('Expected output:', output0)
    result0 = insertion_sort(nums0)
    print('Actual output:', result0)
    print('Match:', result0 == output0)
