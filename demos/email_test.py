import random
import context
from makogram.grammar import Grammar


def rand_str():
    return ''.join(random.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(5))
def user():
	return random.choice(['jamiez', 'michal', 'brian', 'amie'])
def group():
	return random.choice(['admissions', 'testing', 'GTFF'])
def company():
	return random.choice(['gmail', 'uoregon', 'symantec', 'usda'])
def dom():
	return random.choice(['edu', 'com', 'gov', 'org'])


g = Grammar()
g.prod("email", "${Prefix()}@${Suffix()}", max_uses=4, weight=2)
g.prod("Prefix", "${username()}")
g.prod("Prefix", rand_str)
g.prod("username", user)
g.prod("username", group)

g.prod("Suffix", "${Service()}.${Domain()}")
g.prod("Service", company)
g.prod("Service", rand_str)
g.prod("Domain", dom)
g.prod("Domain", rand_str)

for _ in range(20):
	print(g.gen("email"))