"""
Some extra utility functions built on top 
of Python's 'random' module. 
"""
import random

def choose_m_n(li,min,max):
    """Choose from m to n items from li"""
    n_items = random.randrange(min,max+1)
    if n_items == 0:
        return [ ]
    sample=random.sample(li,n_items)  # Should it be sorted?
    return sample

def choose_ordered_m_n(li,min,max):
    """Like choose_m_n, but the selection is ordered 
    the same as the source sequence. 
    """
    n_items = random.randrange(min,max+1)
    if n_items == 0:
        return [ ]
    indices = list(range(len(li)))
    sample=random.sample(indices,n_items)  # Should it be sorted?
    return [li[i] for i in sorted(sample)]

# Random string from alphabet --- based on Jamie's code for names
# and student ID numbers. 
# 
def rand_str(length,alphabet="abcdefghijklmnopqrstuvwxyz"):
    return ''.join(random.choice(alphabet) for _ in range(length))




    
