def commonLetters(str1,str2):
    s1 = set(str1.lower())
    s2 = set(str2.lower())
    common_str = s1 & s2
    return common_str
print(commonLetters("Rajiv","Ranjan"))

# Count the frequency of letters in a string
def countLetters(str1):
    str1 = str1.lower()
    letter_count = {}
    for letter in str1:
        if letter.isalpha():
            if letter in letter_count:
                letter_count[letter] += 1
            else:
                letter_count[letter] = 1
    return letter_count
print(countLetters("Rajiv Ranjan"))

# Convert a list to dictionary with index as key and element as value
def listToDict(lst):
    return {i: lst[i] for i in range(len(lst))}
print(listToDict(["Rajiv", "Ranjan", "Python", "Java"]))

## Convert a dictionary to list of tuples
def dictToList(dct):
    return [(key, value) for key, value in dct.items()]
print(dictToList({"Rajiv": 1, "Ranjan": 2, "Python": 3, "Java": 4}))

## Covert dictionary to tuple
def dictToTuple(dct):
    return tuple((key, value) for key, value in dct.items())
print(dictToTuple({"Rajiv": 1, "Ranjan": 2, "Python": 3, "Java": 4}))

### Convert a tuple to dictionary
def tupleToDict(tpl):
    return {tpl[i][0]: tpl[i][1] for i in range(len(tpl))}
print(tupleToDict((("Rajiv", 1), ("Ranjan", 2), ("Python", 3), ("Java", 4))))

##Conert a list to tuple
def listToTuple(lst):
    return tuple(lst)
print(listToTuple(["Rajiv", "Ranjan", "Python", "Java"]))

## Convert a tuple to list
def tupleToList(tpl):
    return list(tpl)
print(tupleToList(("Rajiv", "Ranjan", "Python", "Java")))

## Reverse a string with for loop
def reverseString(str1):
    reversed_str = ""
    for i in range(len(str1)-1, -1, -1):
        reversed_str += str1[i]
    return reversed_str
print(reverseString("Rajiv Ranjan"))

## Remove duplicates from a list
def removeDuplicates(lst):
    return list(set(lst))
print(removeDuplicates(["Rajiv", "Ranjan", "Python", "Java", "Rajiv", "Python"]))   

## Remove duplicates from a list while preserving order
def removeDuplicatesPreserveOrder(lst):
    seen = set()
    result = []
    for item in lst:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result
print(removeDuplicatesPreserveOrder(["Rajiv", "Ranjan", "Python", "Java", "Rajiv", "Python"]))

# Remove duplicates from a list of dictionaries based on a key
def removeDuplicatesFromDictList(lst, key):
    seen = set()
    result = []
    for d in lst:
        if d[key] not in seen:
            seen.add(d[key])
            result.append(d)
    return result
print(removeDuplicatesFromDictList([{"name": "Rajiv", "age": 30}, {"name": "Ranjan", "age": 25}, {"name": "Python", "age": 20}, {"name": "Java", "age": 35}, {"name": "Rajiv", "age": 30}], "name"))

