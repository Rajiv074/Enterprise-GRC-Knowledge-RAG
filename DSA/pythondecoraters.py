
from functools import wraps
import time
# def logger(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         print(f"Function {func.__name__} called with arguments: {args} and keyword arguments: {kwargs}")
#         result = func(*args, **kwargs)
#         print(f"Function {func.__name__} returned: {result}")
#         return result
#     return wrapper

# @logger
# def add(a,b):
#     return a+b

# add(10,20)
# print("************************")
# def timer(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         start_time = time.time()
#         result = func(*args, **kwargs)
#         end_time = time.time()
#         print(f"Function {func.__name__} took {end_time - start_time:.4f} seconds to execute.")
#         return result
#     return wrapper

# @timer
# def process_data():
#     time.sleep(2)  # Simulate a time-consuming process
#     print("Data processed successfully!")
    
# process_data()
  
# print("************************")   

# def my_decorator(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):   
#         print("Before the function call.")
#         func(*args, **kwargs)
#         print(f"Function {func.__name__} called with arguments: {args} and keyword arguments: {kwargs}")
#         print("After the function call.")
#     return wrapper
# @my_decorator
# def greet(name):
#     print("Hello, welcome to the program!"+name)

# greet("Rajiv")  # Output: Hello, welcome to the program!

# print("************************")
import matplotlib.pyplot as plt

# Data for the top 10 countries by GDP
countries = [
    "United States", "China", "Germany", "Japan", "India",
    "United Kingdom", "France", "Italy", "Brazil", "Canada"
]

gdp_values = [
    26954, 17786, 4430, 4231, 3730,
    3332, 3052, 2190, 2132, 2122
]

# Create a bar chart
plt.figure(figsize=(12, 6))
plt.bar(countries, gdp_values, color='skyblue')
plt.title('Top 10 Countries by GDP in 2023')
plt.xlabel('Country')
plt.ylabel('GDP (in billion USD)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

