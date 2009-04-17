import operator
def prod(x, z=None):
    """
    EXAMPLES:
        sage: from sage.misc.misc_compat import prod
        sage: prod([1,2,34])
        68
        sage: prod([2,3], 5)
        30
        sage: prod((1,2,3), 5)
        30
        sage: F = factor(-2006); F
        -1 * 2 * 17 * 59
        sage: prod(F)
        -2006
    """
    try:
        return x.prod()
    except AttributeError:
        pass
    try:
        return x.mul()
    except AttributeError:
        pass
    if z is not None:
        return reduce(operator.mul, x, z)
    else:
        return reduce(operator.mul, x)

def running_total(L, start=None):
    """
    EXAMPLES:
        sage: from sage.misc.misc_compat import running_total
        sage: running_total(range(5))
        [0, 1, 3, 6, 10]
        sage: running_total("abcdef")
        ['a', 'ab', 'abc', 'abcd', 'abcde', 'abcdef']
        sage: running_total([1..10], start=100)
        [101, 103, 106, 110, 115, 121, 128, 136, 145, 155]
    """
    first = True
    for x in L:
        if first:
            total = L[0] if start is None else L[0]+start
            running = [total]
            first = False
            continue
        total += x
        running.append(total)
    return running

