"""Part 1 includes 4 functions and a global variable.
function 1 - text_to_list:
    import the text file and go through the text character by character - only A to z are included,
    all punctuations, numbers, symbols or special chars are excluded
    returns a list of all strings from the given text in lowercase.
    
global variable - a hashmap
function 2 - hash_func 
    Hash Function reference: https://stackoverflow.com/questions/18781106/generate-same-unique-hash-code-for-all-anagrams
    in order to find anagrams, we map letters a to z by the first 26 prime numbers
    the global variable is a dictionary structure with 26 keys from a to z and each letter is assigned a unique prime number
    {'a': 2, 'b': 3, 'c': 5, 'd': 7, 'e': 11... 'z':101}
    
    the function hash_func takes a word and the hash value is computed by product of all letters' prime number together
    only anagrams share same hash value since a given number have a unique set of prime factors
    (unique prime factorization theorem)
    ie: hash value of 'abc' = 2*3*5 = 30, 'cab' = 2*3*5 = 30  

function 3 - textAnalyzer
    takes the list of strings created from function 1, pass each word to the hash_func and computes a hash value
    create a dictionary with hash values as keys and {word:frequency} as values
    if same word is passed, increment the frequency count by 1
    anagram exists when collision occurs
    use concept of chaining to handle collision - update value by the anagram
    create a separate set() variable to store the hash value when collision is spotted
    ie: {4443145: {'could': 61, 'cloud': 1}} - where 4443145 is the computed hash value
    return the dictionary stores all words/frequencies and the set with all anagrams' hash values.
    
function 4 - anagram_printer
    takes the dictionary and all anagrams' hash value set created in last function 
    go through the hash values in the anagrams set and retrieve the words and frequency count from the dictionary
    convert anagrams and frequency to a pandas dataframe as output 
    
                   Anagrams  Frequency
    0        (could, cloud)         62
    1        (dense, needs)          3
    2      (bowels, elbows)          3
    3    (weather, whereat)          9
    4        (these, sheet)         33
    ..                  ...        ...
    110          (has, sha)         23
    111      (tough, ought)          3
    112    (earthy, hearty)          4
    113    (thread, hatred)          3
    114      (words, sword)         12

part 2
function - search:
    use the text dictionary generated from function 3 (textAnalyzer())
    takes a user input and compute its hash value by function 2 (hash_func())
    locate the hash value in the dictionary 
    print out if the word/it's anagram exists in the text and the frequency count
    ie:
    Please enter the string:hash
    The given word is not in the text.
    
    Please enter the string:has
    Anagrams found!
    The anagram set is: ('has', 'sha'), frequency: 23.
    
    Please enter the string:LONDON
    LONDON appears 5 times in the text, no anagrams are found    
"""



"""Part 1 Import given Text and Analyze for Anagrams"""

import numpy as np
import pandas as pd

def txt_to_list(filename):
    """
    import .txt file to list of strings
    since special char (such as '∑') exists in the given text and is not able to remove
    Thus we only keep words with valid A to z letters
    punctuations, numbers and spaces are removed
    """
    text=[]
    # punctuations = '''!()-[]{};:'"\,<>.//?@#$%^&*_~:1234567890∑'''
    letters_only='' #create a string includes A to z for filtering
    for i in range(ord('A'), ord('Z') + 1):
        letters_only+=chr(i)
    for i in range(ord('a'), ord('z') + 1):
        letters_only+=chr(i)
    string=''

    with open(filename, 'rb') as file:
        for ch in file.read().decode(errors='replace'):
            if ch in letters_only:
                string += ch
            else:
                string += ' '
    for word in string.split():
        text.append(word.lower())
    return text

'''
Generate a Global hashmap (dictionary) that map a to z for the first 26 prime numbers
(prime numbers are found from Wikipedia)
hash_dict looks like: {'a': 2, 'b': 3, 'c': 5, 'd': 7, 'e': 11... 'z':101}
'''
prime_numbers = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97,
                     101]
hash_dict = {}
j = 0
while j < 26:
    for i in range(ord('a'), ord('z') + 1):
        hash_dict[chr(i)] = prime_numbers[j]
        j += 1

def hash_func(word):
    """
    Compute the given string's hash value by multiplying each character's prime number
    (using the global var hash_dict created above)
    return the hash value
    *anagrams have same hash value since it's multiplied by same set of prime numbers
    (according to uniqueness of prime factorization)
    """
    hash_code=1
    for ch in word:
        hash_code*=hash_dict[ch]
    return hash_code


def textAnalyzer(data):
    """
    takes a list of words, hash each word by hash_func()
    and store all words in a dictionary by {hashvalue: {word: count}}
    if same word appears again, increase the frequency counter
    for words return the same hash value - they are anagrams
    if so, mark down the hash value at a separate set for further review
    return the text dictionary with all texts (anagrams or not) and frequency count,
    and a set of hash values represent anagrams
    """
    text_dict={}
    anagram_set=set()
    for word in data:
        key = hash_func(word)
        value = {word:1}
        if key not in text_dict:
            text_dict[key]=value
        else:
            if word in text_dict[key]:
                #same word is found again, increase counter by 1
                text_dict[key][word]+=1

            else:
                #anagram is found
                #append the word to dictionary and markdown the hashvalue in anagram set
                text_dict[key].update(value)
                anagram_set.add(key)

    return text_dict, anagram_set


def anagram_printer(text_dict, anagram_set):
    """
    take the text dictionary and set of anagram hash values
    locate all anagrams and the frequency from text dictionary (using hash value)
    convert to pandas DataFrame and display
    """
    anagram_list = []
    anagram_frequency = []
    for i in anagram_set:
        key = tuple(text_dict[i])
        anagram_list.append(key)
        freq = sum(text_dict[i].values())
        anagram_frequency.append(freq)
    anagram_data = {'Anagrams': anagram_list, 'Frequency': anagram_frequency}
    df = pd.DataFrame(anagram_data)
    return df


"""Part 2 Search Function"""

def search(text_dict):
    """
    takes a word input and return if the word and it's anagrams find in the given file
    """
    word=input("""Please enter the string:""")
    hash_value = hash_func(word.lower())

    if (hash_value not in text_dict) or (word.lower() not in text_dict[hash_value]):
        print("The given word is not in the text.")
    else:
        if len(text_dict[hash_value]) ==1:
                print('{} appears {} times in the text, no anagrams are found'.format(word, text_dict[hash_value][word.lower()]))
        else:
            words = tuple(text_dict[hash_value])
            freq = sum(text_dict[hash_value].values())
            print('Anagrams found!')
            print('The anagram set is: {}, frequency: {}.'.format(words, freq))
    return


def main():
    file = 'finn.txt'
    # filename='test.txt'
    print('---- Part 1 ----')
    data = txt_to_list(file)
    (text_dict,anagram_set) = textAnalyzer(data)
    print(anagram_printer(text_dict,anagram_set))
    print('---- Part 2 ----')
    search(text_dict)




if __name__ == "__main__":
       main()
