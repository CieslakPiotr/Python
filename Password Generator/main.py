import random
from tkinter import messagebox

#Lists with letters, numbers and symbols
letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "u", "y", "z", "A", "B", "C", "D",
          "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "U", "Y", "Z"]
numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
symbols = ["!", "#", "$", "%", "&", "(", ")", "*", "+"]

#Variables
all_symbols = []
password = ""

#User input
number_of_letters = int(input("How many letters does your password have to consist of?:"))
number_of_numbers = int(input("How many numbers does your password have to consist of?:"))
number_of_symbols = int(input("how many symbols does your password have to consist of?:"))

#Add specified amount of numbers to the list
for _ in range(number_of_letters):
    all_symbols.append(random.choice(letters))

for _ in range(number_of_numbers):
    all_symbols.append(random.choice(numbers))

for _ in range(number_of_symbols):
    all_symbols.append(random.choice(symbols))

#Radomize symbols
random.shuffle(all_symbols)

#Add symbols to the string
for i in all_symbols:
    password += i

#Display new password
messagebox.showinfo(title="Password", message=password)
print(password)