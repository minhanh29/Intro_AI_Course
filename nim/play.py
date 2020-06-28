from nim import train, play

choices = {
    1: 500,
    2: 2000,
    3: 10000,
}

print()
print("Welcome to NIM!")
print("Please choose one level!")
print()
print("Level 1", "Level 2", "Level 3", sep='     ')
print()
level = int(input("Your choice: "))

ai = train(choices[level])
play(ai)
