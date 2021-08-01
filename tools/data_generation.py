import random as rand

def generate_data(len_, sparcity):
    data = [0 for _ in range(len_)]
    
    for _ in range(int(sparcity*len_)):
        found = False
        while not found:
            i = rand.randint(0, len_-1)
            if not data[i]:
                data[i] = 1
                found = True
    return data