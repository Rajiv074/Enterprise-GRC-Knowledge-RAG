# def str_reverse(org_str):
#     new_str = ""
#     for i in range(len(org_str)-1, -1, -1):
#         new_str += org_str[i]
#     return new_str

# print(str_reverse("Hello, World!"))  # Output: !dlroW ,olleH


##Flatten a list of lists normally
# arr = [[1, 2], [3, 4], [5, 6]]
# def flatten_list(lst):
#     result = []
#     for item in lst:
#         if isinstance(item, list):
#             result.extend(flatten_list(item))
#         else:
#             result.append(item)
#     return result
            
# flatten_list(arr)

# def count_occurrences(lst):
#     count_dict = {}
#     for item in lst:
#         if item in count_dict:
#             count_dict[item] += 1
#         else:
#             count_dict[item] = 1
#     return count_dict

# print(count_occurrences("Rajiv"))

##First non-repeated character in a string
# def first_non_repeated_char(s):
#     char_count = {}
#     for char in s:
#         if char in char_count:
#             char_count[char] += 1
#         else:
#             char_count[char] = 1
#     for char in s:
#         if char_count[char] == 1:
#             return char
#     return None

# first_non_repeated_char("swiss")  # Output: 'w'

## sum of two number based on target number
# def two_sum(nums, target):
#     num_dict = {}
#     for i, num in enumerate(nums):
#         complement = target - num
#         if complement in num_dict:
#             return [num_dict[complement], i]
#         num_dict[num] = i
#     return None

# two_sum([2, 7, 11, 15], 9)  # Output: [0, 1] because nums[0] + nums[1] = 2 + 7 = 9

# ##Find the missing number in an array of 1 to n
# def find_missing_number(nums):
#     n = len(nums) + 1  # Since one number is missing
#     expected_sum = n * (n + 1) // 2  # Sum of first n natural numbers
#     actual_sum = sum(nums)
#     return expected_sum - actual_sum

# def find_missing_number_simple(nums):
#     n = len(nums)
#     print("n:", n)
#     print("range(n + 1):", range(n + 1))
#     for i in range(n + 1):
#         if i not in nums:
#             return i
#     return None

# print(find_missing_number_simple([0, 1, 2, 3, 4, 5]))  # Output: 3
    
# def print_numbers():
#     for i in range(0,6):
#         print(i)
# print_numbers()

# def printStar(n):
#     for i in range(1,n):
#         for j in range(0,i):
#             print("*",end=" ")
#         print(" ")
  
# printStar(5); 


## isinstance

# my_obj = {"name": "John", "age": 30}
# for key in my_obj:
#     if isinstance(my_obj[key], str):
#         print(f"{key} is a string with value: {my_obj[key]}")
#     elif isinstance(my_obj[key], int):
#         print(f"{key} is an integer with value: {my_obj[key]}")
#     else:
#         print(f"{key} is of type {type(my_obj[key])} with value: {my_obj[key]}")
        
# ##hasattr() example

# print(hasattr(my_obj, 'name'))  # Output: False, because my_obj is a dictionary, not an object with attributes

# class Person:
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age
        
# user = Person("Alice", 25)
# print(hasattr(user, 'name'))  # Output: True

# from typing import Any

# def tutorial(x: Any) -> str:
#     if isinstance(x, str):
#         return f"{x} is a string"
#     elif isinstance(x, int):
#         return f"{x} is an integer"
#     elif isinstance(x, list):
#         return f"{x} is a list"
#     elif isinstance(x, dict):
#         return f"{x} is a dictionary"
#     else:
#         return f"{x} is of type {type(x)}"
    
# print(tutorial("Hello"))  # Output: "Hello is a string"

### inheritance example
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        print(f" This Animal name is {self.name}")

class Dog(Animal):
    def __init__(self, name,size):
        super().__init__(name)
        self.size = size
    def size_of_dog(self):
        print(f" This Dog name is {self.name} and size is {self.size}")

d = Dog("Buddy", "Medium")
d.speak()  # Output: This Animal name is Buddy
d.size_of_dog()  # Output: This Dog name is Buddy and size is Medium


#enumurate example
# my_list = ['a', 'b', 'c']
# for index, value in enumerate(my_list):
#     print(f"Index: {index}, Value: {value}")  



 
  
            
            
            

    