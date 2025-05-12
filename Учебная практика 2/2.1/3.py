def contains_duplicate(nums):
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False
print(contains_duplicate([1, 2, 3, 4])) #Ложььььь
print(contains_duplicate([1, 1, 1, 3, 3, 4, 3, 2, 4, 2])) #Правдаааа
print(contains_duplicate([1, 2, 3, 1])) #Правдааааааааааа