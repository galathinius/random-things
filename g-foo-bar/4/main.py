import numpy as np
from fractions import Fraction

def normalize(mat):
    for i in range(len(mat)):
        row_sum = sum(mat[i])
        for j in range(len(mat[i])):
            mat[i][j] = float(mat[i][j])/ float(row_sum)

    return mat

def remove_unreachable(mat):
    new_mat = np.array(mat)
    unreachable_states = []

    for index_y in range(len(mat)):
        row = mat[index_y]
        reachable = False

        for index_x in range(len(row)):
            item = mat[index_x][index_y]
            if item:
                reachable = True
                break
        
        if not reachable and index_y != 0:
            
            unreachable_states.append(index_y)
            new_mat = np.delete(new_mat, index_y, 0)
            new_mat = np.delete(new_mat, index_y, 1)    

    return[new_mat, unreachable_states]
    
def which_ones_are_term(mat):
    term = []

    for index_y in range(len(mat)):
        row = mat[index_y]
        terminal = True

        for index_x in range(len(row)):
            item = mat[index_y][index_x]
            if item:
                terminal = False
                break
        
        if terminal:   
            term.append(index_y)
            
    return term

def get_terms_no_unreach(terms, unreach):
    no_unreach = []
    for term in terms:
        if term in unreach:
            continue
        else:
            no_unreach.append(term)

    return no_unreach

def separate_terminals(mat, term, bias):
    non_terminals = np.array(mat)
    
    bias1 = bias
    for a_term in term:
        non_terminals = np.delete(non_terminals, a_term - bias1, 0)
        bias1 += 1

    non_terminals = normalize(non_terminals)

    terminals = np.zeros((
        len(non_terminals), len(term)))

    bias2 = bias
    for a_term in term:
        terminals[:, bias2 - bias] = non_terminals[:, a_term - bias2]
        non_terminals = np.delete(non_terminals, a_term - bias2, 1)
        bias2 += 1    

    return [non_terminals, terminals]

def create_unit_mat(n):
    unit_mat = np.zeros((n, n))

    for i in range(n):
        unit_mat[i][i] = 1

    return unit_mat

def get_n_mat(n_terminals):
    n_mat = []
    n_terminals_unit = create_unit_mat(
        len(n_terminals))

    difference = np.subtract(n_terminals_unit, n_terminals)
    
    n_mat = np.linalg.inv(difference) 

    return n_mat

def get_m_mat(n_mat, r_mat):
    m_mat = np.matmul(n_mat, r_mat)

    return m_mat

def make_index_list(unr, term, sol):
    
    result = np.zeros((1, len(term) + 1))[0]
    sol_counter = 0
    for i in range(len(term)):
        if term[i] in unr:
            continue
        else:
            result[i] = sol[sol_counter]
            sol_counter += 1
    
    return result

def denormalize(sol):
    numerators =[]
    denominators = []

    for i in range(len(sol) - 1):
        x = Fraction(sol[i]).limit_denominator()
        numerators.append(x.numerator)
        denominators.append(x.denominator)

    # print denominators
    common =  np.lcm.reduce(denominators)
    # print common

    for i in range(len(sol) - 1):
        sol[i] = int(numerators[i] * (common / denominators[i]))

    sol[-1] = common

    return np.array(sol, dtype=int)

def solution(mat):
    if len(mat[0]) == 1:
        return [1, 1]
    np_array = np.array(mat, dtype=float)
    # print 'initial\n', np_array

    term_list = which_ones_are_term(np_array)
    # print 'terms\n', term_list

    new_mat, unreachable = remove_unreachable(np_array)
    # print 'unrea\n', unreachable
    # print 'new_mat\n', new_mat

    no_unreachable = get_terms_no_unreach(term_list, unreachable)
    # print 'no_unreachable', no_unreachable

    non_term, term = separate_terminals(new_mat, no_unreachable, len(unreachable))
    # print 'non_term, term\n', non_term, term

    n_mat = get_n_mat(non_term)
    # print 'n_mat\n', n_mat

    m_mat = get_m_mat(n_mat, term)
    # print 'm_mat\n', m_mat

    norm_solution = make_index_list(unreachable, term_list, m_mat[0])

    # print 'norm_solution\n', norm_solution

    denorm = denormalize(norm_solution)
    # print 'denorm', list(denorm)

    return list(denorm)

#   according to
#   https://brilliant.org/wiki/absorbing-markov-chains/
