'''
This file will contain different variable ordering heuristics to be used within
bt_search.

1. ord_dh(csp)
    - Takes in a CSP object (csp).
    - Returns the next Variable to be assigned as per the DH heuristic.
2. ord_mrv(csp)
    - Takes in a CSP object (csp).
    - Returns the next Variable to be assigned as per the MRV heuristic.
3. val_lcv(csp, var)
    - Takes in a CSP object (csp), and a Variable object (var)
    - Returns a list of all of var's potential values, ordered from best value 
      choice to worst value choice according to the LCV heuristic.

The heuristics can use the csp argument (CSP object) to get access to the 
variables and constraints of the problem. The assigned variables and values can 
be accessed via methods.
'''

import random
from copy import deepcopy

def ord_dh(csp):
    all_var = csp.get_all_unasgn_vars()
    max_var = all_var[0]
    max_con = 0

    for var1 in all_var:
        con1 = set(csp.get_cons_with_var(var1))
        count = -len(con1)
        for var2 in all_var:
            con2 = set(csp.get_cons_with_var(var2))
            count += len(con1&con2)

        if count < max_con:
            max_con = count
            max_var = var1
        
    return max_var    


def ord_mrv(csp):
    # TODO! IMPLEMENT THIS!
    all_var = csp.get_all_unasgn_vars()
    min_var = all_var[0]
    min_domain = min_var.cur_domain_size()

    for var in all_var:

        if min_domain > var.cur_domain_size():
            min_var = var
            min_domain = min_var.cur_domain_size()

    
    return min_var


def val_lcv(csp, var):
    # TODO! IMPLEMENT THIS!
    all_var = csp.get_all_unasgn_vars()
    all_val = var.cur_domain()
    val_dict = {}

    for val in all_val:
        prunes = 0
        var.assign(val)
        for i in all_var:
            for j in i.cur_domain():
                for c in csp.get_cons_with_var(i):
                    if not c.has_support(i, j):
                        prunes += 1
                        break

        val_dict[val] = prunes
        var.unassign()

    values = sorted(val_dict, key=val_dict.get)
    
    return values
