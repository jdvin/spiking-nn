import random as rand

def populate_vector(vector, n):
    '''
    turn n zeros in vector into ones
    NB: THIS WILL RUN FOREVER IF THERE ARE NOT at least n zeroes 
    '''
    for _ in range(n):
        found = False
        while not found:
            i = rand.randint(0, len(vector)-1)
            if not vector[i]:
                vector[i] = 1
                found = True
    return vector

def unpopulate_vector(vector, n):
    '''
    turn n ones in vector into zeros
    NB: THIS WILL RUN FOREVER IF THERE ARE NOT at least n ones 
    '''
    for _ in range(n):
        found = False
        while not found:
            i = rand.randint(0, len(vector)-1)
            if vector[i]:
                vector[i] = 0
                found = True
    return vector

def generate_data(n, len_, sparcity, overlap):
    data = []
    prototype = [0 for _ in range(len_)]
    prototype_sparticity = int(len_ * overlap)
    prototype = populate_vector(prototype, prototype_sparticity)

    for _ in range(n):
        exemplar = prototype.copy()
        exemplar_sparcity = int(len_ * (sparcity - overlap))
        exemplar = populate_vector(exemplar, exemplar_sparcity)
        data.append(exemplar.copy())
    return data
