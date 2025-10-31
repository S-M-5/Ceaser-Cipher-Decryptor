from english_words import get_english_words_set
from wordfreq import top_n_list
from nltk.corpus import words , names
import nltk
import os
import string
nltk.download('words')
nltk.download('names')


english1 = get_english_words_set(['web2'], lower = True)
english2 = set(top_n_list('en' , 10**9))
english3 = set(words.words())
english4 = set(names.words())


all_words = english1 | english2 | english3 | english4  # Merge all 4 English dictionary sources
alphabet = "abcdefghijklmnopqrstuvwxyz0123456789,./?!"
char_to_index = {}
index_to_char = {}

for index,char in enumerate(alphabet): # Storing alphabet into a char:index and index:char dictionary
    char_to_index[char] = index
    index_to_char[index] = char

def decrypt(file):
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
                    char = char.lower()
                    if char not in char_to_index:
                        decrypted_text += char
                        continue
                    dec = (char_to_index[char] - key) % len(alphabet)
                    decrypted_text += index_to_char[dec]
                word1, word2, word3 = decrypted_text.strip().strip(string.punctuation).split()
                if (word1 in all_words) and (word2 in all_words) and (word3 in all_words):
                    break
                else:
                    decrypted_text = ''
                    word1 = ''
                    word2 = ''
                    word3 = ''


            decrypted_text = ''
            decrypted_chars = []
            words_to_chars = list(file_line.lower())
            for c in words_to_chars:        # Decrypts the rest of the line using the correct key
                if c not in char_to_index:
                    decrypted_chars.append(c)
                    continue
                c = (char_to_index[c] - key) % len(alphabet)
                decrypted_chars.append(index_to_char[c])
            for i in decrypted_chars:
                decrypted_text += i
            final_text += '\n'+decrypted_text+"\nKey: "+str(key)+"\n\n"

        i = 1
        while os.path.exists(f"decrypted-file-{i}.txt"): # Creating a file name based on previously created files
            i+=1
        dec_file = f'decrypted-file-{i}.txt'
        with open(dec_file, 'w') as file:
            file.write(final_text)
        print(final_text+ f"\nFile successfully saved to {os.path.abspath(dec_file)}")


def display(file):
    with open(file, "r") as file:
        print(file.read())


if __name__ == '__main__':
    try:
        file = input("Enter file name: ")+".txt"
        option = input("Decrypt and find keys or Print encoded file? (d/p):")
        if option.lower() == "d":
            decrypt(file)
        elif option.lower() == "p":
            display(file)
        else:
            print("\nInvalid option.\nChoose 'd' to decrypt, or 'p' to print encoded file")
    except FileNotFoundError:
        print("\nFile not found. Please try again.")

