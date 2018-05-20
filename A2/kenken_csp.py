'''
All models need to return a CSP object, and a list of lists of Variable objects 
representing the board. The returned list of lists is used to access the 
solution. 

For example, after these three lines of code

    csp, var_array = kenken_csp_model(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array[0][0].get_assigned_value() should be the correct value in the top left
cell of the KenKen puzzle.

The grid-only models do not need to encode the cage constraints.

1. binary_ne_grid (worth 10/100 marks)
    - A model of a KenKen grid (without cage constraints) built using only 
      binary not-equal constraints for both the row and column constraints.

2. nary_ad_grid (worth 10/100 marks)
    - A model of a KenKen grid (without cage constraints) built using only n-ary 
      all-different constraints for both the row and column constraints. 

3. kenken_csp_model (worth 20/100 marks) 
    - A model built using your choice of (1) binary binary not-equal, or (2) 
      n-ary all-different constraints for the grid.
    - Together with KenKen cage constraints.

'''
from cspbase import *
import itertools as it

def binary_ne_grid(kenken_grid):
    # TODO! IMPLEMENT THIS!
    size = kenken_grid[0][0]
    domain = []
    for n in range(size):
        domain.append(n+1)


    model = CSP("none")
    grid = []

    for i in range(size):
        grid.append([])
        for j in range(size):
            newv = Variable(str(i)+str(j), domain)
            grid[i].append(newv)
            model.add_var(newv)
    

    bne_set = set()
    for i in range(size):
        for j in range(size):
            if i == j:
                continue
            bne_set.add((i+1,j+1))

    for i in range(size):
        for j in range(size):
            for k in range(i+1,size):
                newcon = Constraint(str(i)+str(j)+'&'+str(k)+str(j),[grid[i][j], grid[k][j]])
                newcon.add_satisfying_tuples(bne_set)
                model.add_constraint(newcon)
            for k in range(j+1,size):
                newcon = Constraint(str(i)+str(j)+'&'+str(i)+str(k),[grid[i][j], grid[i][k]])
                newcon.add_satisfying_tuples(bne_set)
                model.add_constraint(newcon)
    
    return model,grid

def nary_ad_grid(kenken_grid):
    # TODO! IMPLEMENT THIS!
    size = kenken_grid[0][0]

    domain = []
    for n in range(size):
        domain.append(n+1)

    model = CSP("none")
    grid = []

    for i in range(size):
        grid.append([])
        for j in range(size):
            newv = Variable(str(i)+str(j), domain)
            grid[i].append(newv)
            model.add_var(newv)

    bne_set = set(it.permutations(range(1,size+1), size))


    for i in range(size):
        newcon = Constraint('row' + str(i),grid[i])
        newcon.add_satisfying_tuples(bne_set)
        model.add_constraint(newcon)

        newcon = Constraint('column' + str(i), [row[i] for row in grid])
        newcon.add_satisfying_tuples(bne_set)
        model.add_constraint(newcon)

    return model,grid


def kenken_csp_model(kenken_grid):
    # TODO! IMPLEMENT THIS!
    size = kenken_grid[0][0]
    model,grid = binary_ne_grid(kenken_grid)
    #model,grid = nary_ad_grid(kenken_grid)

    for i in range(1,len(kenken_grid)):
        newcon = []
        scope = scope_convert(kenken_grid[i][:-2], grid)
        dim = len(scope)
        val = kenken_grid[i][-2]
        op = kenken_grid[i][-1]

        new_list = list(it.product(range(size), repeat=dim))

        for perm in new_list:
            perm = [x+1 for x in perm]
            if constraint_check(perm, val, op):
                newcon.append(perm)


        C = Constraint('Constraint', scope)
        C.add_satisfying_tuples(newcon)
        model.add_constraint(C)

    return model,grid 


def scope_convert(scope, grid):
    newscope1 = []
    for i in scope:
        newscope1.append((int(str(i)[0])-1, int(str(i)[1])-1))

    newscope2 = []
    for i in newscope1:
        newscope2.append(grid[i[0]][i[1]])  

    return newscope2

def constraint_check(new_list, val, op):
    new_list = list(new_list)
    
    if op == 0:
        sum = 0
        for v in new_list:
            sum += v
        if sum == val:
            return True
    if op == 1:
        for perm in it.permutations(new_list):
            #calculate value
            result = perm[0]
            i = 1
            while(i < len(new_list)):
                result -= perm[i]
                i += 1
            if result == val:
                return True
    if op == 2:
        for perm in it.permutations(new_list):
            #calculate value
            result = perm[0]
            i = 1
            while(i < len(new_list)):
                result //= perm[i]
                i += 1
            if result == val:
                return True
    if op == 3:
        prod = 1
        for v in new_list:
            prod *= v
        if prod == val:
            return True

    return False
