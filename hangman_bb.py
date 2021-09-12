import random
import os
import hangman_pics
import shutil
import time

def clear_screen():
    os.system("clear")

def padToCenter(list):
    return "\n".join(x.center(center_terminal()) for x in list)

def center_terminal():
    return shutil.get_terminal_size().columns

def word_list(word):
    word_list = []
    for chr in word:
        word_list.append(chr)
    return word_list

def underscores_list(word):
    underscores = []
    for chr in word:
        if chr == '-':
            underscores.append('-')
        elif chr == ' ':
            underscores.append(' ')
        else:
            underscores.append('_')
    return underscores    

def country_or_capital(lives):
    if lives == 7:
        return "country"
    elif lives == 5:
        return "capital"
    return "country or capital"

def display_game_screen(type, word, word_, pic_index, missed_letters_list):
    clear_screen()
    print("")
    print(padToCenter(hangman_pics.hangman_title[0]))
    # print("")
    # print("Only for us to know:".center(center_terminal()))
    # print(f"{' '.join(word)}".center(center_terminal()))
    print(f"This is the {country_or_capital(type)} to guess:\n".center(center_terminal()))
    print(f"{' '.join(word_)}\n".center(center_terminal()))
    if len(missed_letters_list) > 0:
        print(f"Missed letters: {missed_letters_list}".center(center_terminal()))
    else:
        print("")
    print(f"You have {type - len(missed_letters_list)} lives left".center(center_terminal()))
    print(padToCenter(hangman_pics.HANGMANPICS[pic_index].splitlines()))

def hangman_index(type, lives):
    index_list = []
    if type == 7:
        index_list = [0, 1, 2, 3, 4, 5, 6, 7]
    elif type == 5:
        index_list = [0, 1, 2, 4, 6, 7]
    else:
        index_list = [0, 1, 3, 7]
    return index_list[type - lives]

def validate_guess():
    while True:
        guess = input(f"{' ' * round((center_terminal() - 18) / 2)} Guess a letter: ")
        if guess.lower() == 'quit':
            return "quit"
        elif not guess.isalpha() or len(guess) > 1:
            print("This is not a valid letter. Try again!\n".center(center_terminal()))
            continue
        return guess.lower()

def check_guess(guess, word):
    if guess in word or guess.upper() in word:
        return True
    return False

def change_letter(word, guess, word_):
    for index in range(len(word)):
        if guess == word[index].lower() or guess == word[index].upper():
            word_[index] = word[index]
    return word_

def play_again():
    while True:
        print("")
        play_again = input("Press 'Y' for playing again or 'N' for quit the game ".center(center_terminal()))
        if not play_again.isalpha():
            continue
        elif play_again.isalpha() and play_again.lower() not in "yn":
            continue
        elif play_again.lower() == 'y':
            return True
        return False

def win(word, type, lives):
    print("")
    print("Congratulation!\n".center(center_terminal()))
    print(f"You could successfully found out {''.join(word)} with only {type - lives} mistakes!".center(center_terminal()))

def lose(word):
    print("")
    print("Sorry Bro!\n".center(center_terminal()))
    print(f"The word to found was {''.join(word)}\n".center(center_terminal()))
    print("Maybe next time!".center(center_terminal()))

def play(word, lives):
    word_set = set(word.lower().replace(" ", ""))
    word_ = underscores_list(word)
    word = word_list(word)
    missed_letters_list = []
    found_letters = []
    type = lives

    while True:
        display_game_screen(type, word, word_, hangman_index(type, lives), missed_letters_list)
        guess = validate_guess()
        if guess == "quit":
            return False
        if check_guess(guess, word):
            word_ = change_letter(word, guess, word_)
            found_letters.append(guess)
            if len(set(found_letters)) == len(word_set):
                display_game_screen(type, word, word_, hangman_index(type, lives), missed_letters_list)
                win(word, type, lives)
                break
        elif guess not in missed_letters_list:
            missed_letters_list.append(guess)
            lives -= 1
            if lives == 0:
                display_game_screen(type, word, word_, hangman_index(type, lives), missed_letters_list)
                lose(word)
                break
        else:
            print("")
            print("This letter was already guessed!".center(center_terminal()))
            time.sleep(1.5)
    return play_again()

def random_word(level):
    with open("countries-and-capitals.txt", 'r') as file:
        word = file.readlines()
    if level == 1:
        return word[random.randint(0, len(word) - 1)].split(sep=" | ")[0]
    elif level == 2:
        return word[random.randint(0, len(word) - 1)].split(sep=" | ")[1].strip()
    return word[random.randint(0, len(word) - 1)].split(sep=" | ")[random.randint(0, 1)].strip()

def level_chooser():
    while True:
        display_menu()
        level = input("Please select your level: ")
        if level.lower() == "quit":
            return 4
        elif not level.isnumeric():
            print("Your input doesn't seems to be a number\n")
            continue
        elif level.isnumeric() and level in "123":
            return int(level)
        print("Please choose from the given list!\n")

def display_menu():
    clear_screen()
    print("Hangman Game\n\nDifficulity levels:\n")
    print("'1' - Easy (countries / 7 misses)")
    print("'2' - Medium (capitals / 5 misses)")
    print("'3' - hard (countries or capitals / 3 misses)\n")
    print("(Enter 'quit' to exit game)")

if __name__ == "__main__":
    play_game = True
    while play_game:
        level = level_chooser()
        if level == 4:
            play_game = False
            continue
        word = random_word(level)
        play_game = play(word, 9 - 2 * level)
    print("GOOD-BYE!")
