import random as rand

def populate_vector(vector, n):
    '''
    turn n zeros in vector into ones
    '''
    population = [i for i,element in enumerate(vector) if element == 0]
    sample = rand.sample(population, n)
    
    for i in sample:
        vector[i] = 1

    return vector

def unpopulate_vector(vector, n):
    '''
    turn n ones in vector into zeros
    '''
    population = [i for i,element in enumerate(vector) if element == 1]
    sample = rand.sample(population, n)
    
    for i in sample:
        vector[i] = 0

    return vector
 
def generate_data(n, len_, sparcity, overlap):
    '''
    (sparcity - overlap) * n must be less than overlap
    '''
    data = []
    prototype = [0 for _ in range(len_)]
    prototype_sparticity = int(len_ * overlap)
    prototype = populate_vector(prototype, prototype_sparticity)

    prim_pool = [element for i,element in enumerate(prototype) if element == 0]
    all_exem_prims = rand.sample(prim_pool,  int((len_* (sparcity-overlap) * n)))

    for _ in range(n):
        exemplar = prototype.copy()
        exemplar_prims = rand.sample(all_exem_prims, int(len(all_exem_prims)/n))
        for i in exemplar_prims:
            exemplar[i] = 1
        data.append(exemplar.copy())
    return data
