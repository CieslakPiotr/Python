import random

bot_movements = ["Rock", "Paper", "Scissors"]

game = False
score = 0

decision = input("Do you want to play? Yes/No: ").title()

if decision == "Yes":
    game = True
elif decision == "No":
    game = False
else:
    decision = input("Do you want to play? Yes/No: ").title()

while game:
    game_choice = input("Choose - Rock/Paper/Scissors: ").title()

    move = random.choice(bot_movements)

    if game_choice == "Rock" and move == "Paper":
        print("Computer wins!")
    elif game_choice == "Rock" and move == "Scissors":
        score += 1
        print(f"You win! You score is - {score}.")
    elif game_choice == "Scissors" and move == "Rock":
        print("Computer wins!")
    elif game_choice == "Scissors" and move == "Paper":
        score += 1
        print(f"You win! You score is - {score}.")
    elif game_choice == "Paper" and move == "Scissors":
        print("Computer wins!")
    elif game_choice == "Paper" and move == "Rock":
        score += 1
        print(f"You win! You score is - {score}.")
    elif game_choice == move:
        print("Draft!")
    else:
        print("Invalid move!")

    a = input("Do you want to continue? Yes/No: ").title()

    if a == "No":
        game = False