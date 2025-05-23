def contains(nums):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums [i] == nums[j]:
                return True
    return False
print(contains([1, 2, 3, 4]))
print(contains([1, 1, 1, 3, 3, 4, 3, 2, 4, 2]))
print(contains([1, 2, 3, 1]))
