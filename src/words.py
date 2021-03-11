"""
Code to generate all relevant words
"""

def wordgen(iters, base_cases, rule, return_all=False):
    """generate arbitrary recursive words

    Args:
        iters (int): number of iterations to run on top of base cases
        base_cases (list of strings): strings which your rule can refer to
        rule (method): A function that takes in previous strings and returns a new string
        return_all (bool): return all of the strings generated for this call

    rule's call signature is rule(words:list of strings) -> string.  
    it gets passed previous words, including base cases.

    returns:
        word
    """
    words = base_cases
    n_base_case = len(base_cases)
    for _ in range(n_base_case, iters):
        words.append(rule(words))
    
    if return_all:
        return words
    else:
        return words[iters-1]

def knacci_rule(k):
    knacci = lambda ws: ws[-1] * k + ws[-2] 
    return knacci

def knacci(n, k, return_all=False):
    w_0 = '0'
    w_1 = '0'*(k-1) + '1'
    return wordgen(
        iters=n, 
        base_cases=[w_0, w_1], 
        rule=knacci_rule(k=k), 
        return_all=return_all
    )

def t(word):
    return word[:-2] + word[-2:][::-1]

def biperiodic_rule(a,b):
    a_rule = lambda ws: ws[-1] * a + ws[-2]
    b_rule = lambda ws: ws[-1] * b + ws[-2]
    biper = lambda ws: a_rule(ws) if len(ws)%2==0 else b_rule(ws)
    return biper

fibonacci_rule = lambda ws: ws[-1] + ws[-2]

def biperiodic(n, a, b, return_all=False):
    w_0 = '0'*(a-1) + '1'
    w_1 = '0'*(b-1) + '1'
    return wordgen(
        iters=n, 
        base_cases=[w_0, w_1], 
        rule=biperiodic_rule(a,b), 
        return_all=return_all
    )

def fibonacci(n, return_all=False):
    return wordgen(
        iters=n, 
        base_cases=['0','01'], 
        rule=fibonacci_rule, 
        return_all=return_all
    )

def depth_bonacci_rule(depth):
    """rule for generating tribonacci or other arbitrary depth words

    Args:
        depth (int): number of consecutive previous words to concatenate

    Returns:
        lambda w: w[-1] + w[-2] + ... + w[-(depth+1)]
        For example, if depth is 3, you get the tribonacci words.
        (there is already a tribonacci and quadbonacci words method) 
    """
    return lambda w: "".join(w[-1:-depth-1:-1])

def depth_bonacci(n, depth, return_all=False):
    return wordgen(
        iters=n, 
        base_cases=["0"*i+"1" for i in range(depth)], 
        rule=depth_bonacci_rule(depth), 
        return_all=return_all
    )

def tribonacci(n, return_all=False):
    return depth_bonacci(n, depth=3, return_all=return_all)

def quadbonacci(n, return_all=False):
    return depth_bonacci(n, depth=4, return_all=return_all)

def i_fibonacci(n, i, return_all=False):
    return wordgen(
        iters=n, 
        base_cases=['0','0' * (i-1) + '1'], 
        rule=fibonacci_rule, 
        return_all=return_all
    )


