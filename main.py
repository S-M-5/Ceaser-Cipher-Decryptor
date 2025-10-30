from english_words import get_english_words_set
from wordfreq import top_n_list
from nltk.corpus import words
import nltk
nltk.download('words')


english1 = get_english_words_set(['web2'], lower = True)
english2 = set(top_n_list('en' , 10**9))
english3 = set(words.words())


all_words = english1 | english2 | english3   # Merge all 3 English dictionary sources
alphabet = "abcdefghijklmnopqrstuvwxyz0123456789,./?!"
char_to_index = {}
index_to_char = {}

for index,char in enumerate(alphabet): # Storing alphabet into a char:index and index:char dictionary
    char_to_index[char] = index
    index_to_char[index] = char

def decrypt(file):
    correct_keys = []
    final_text = ''
    with open(file, "r") as file:
        while True:
            file_line = file.readline()
            file_chars = file_line.split()
            if not file_line: # Check if it's the last line of the file
                break
            if not file_line.strip(): # Check if there's a line after an empty line
                continue


            decrypted_text = ''
            first_three_words = list(" ".join(file_chars[1:4]))
            for key in range(len(alphabet)): # Loop through the first 2 words of the line and checks if one of them is in the English dictionary
                for char in first_three_words:
                    if char not in char_to_index:
                        decrypted_text += char
                        continue
                    dec = (char_to_index[char] - key) % len(alphabet)
                    decrypted_text += index_to_char[dec]
                word1, word2, word3 = decrypted_text.strip().split()
                if (word1 in all_words) and (word2 in all_words) and (word3 in all_words):
                    correct_keys.append(key)
                    break
                else:
                    decrypted_text = ''
                    word1 = ''
                    word2 = ''
                    word3 = ''


            decrypted_text = ''
            decrypted_chars = []
            words_to_chars = list(file_line)
            for c in words_to_chars:        # Decrypts the rest of the line using the correct key
                if c not in char_to_index:
                    decrypted_chars.append(c)
                    continue
                c = (char_to_index[c] - key) % len(alphabet)
                decrypted_chars.append(index_to_char[c])
            for i in decrypted_chars:
                decrypted_text += i
            final_text += decrypted_text+"Key: "+str(key)+"\n"
        print(final_text)

decrypt('file-e-3.txt') # Problem with file 3






