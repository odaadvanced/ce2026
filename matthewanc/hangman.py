import random
words = ['chicken','dog','mouse','cat','frog']
def pick_a_word():
    return random.choice(words)

print(pick_a_word())