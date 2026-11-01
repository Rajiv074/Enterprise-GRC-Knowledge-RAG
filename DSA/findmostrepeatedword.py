text = """
India India development development youth youth
India development India youth
Sabka Saath Sabka Vikas
Sabka Saath Sabka Vikas
"""

def find_most_repeated_word(text):
    words = text.split()
    word_count = {}
    item_list = []
    for word in words:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    for word, count in word_count.items():
        print(f"{word}: {count}")
     
    sorted_word_count = dict(sorted(word_count.items(), key=lambda x: x[1], reverse=True))  
    print("Sorted word count:", sorted_word_count)
    soterd_word_count_list = [{"word": word, "count": count} for word, count in sorted_word_count.items()]
    print("Sorted word count list:", soterd_word_count_list) 
    sorted_word_count_tuple = tuple((word, count) for word, count in sorted_word_count.items())
    print("Sorted word count tuple:", sorted_word_count_tuple)
    # most_repeated_word = max(word_count, key=word_count.get)
    # return most_repeated_word, word_count[most_repeated_word],sorted_word_count 
    return sorted_word_count

print(find_most_repeated_word(text))