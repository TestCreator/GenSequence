import random
import context
import re
import dns.resolver
import socket
import smtplib
import sys
from makogram.grammar import Grammar


def rand_str():
	return ''.join(random.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(4))
def user():
	return random.choice(['jamiez', 'michal', 'brian', 'amie'])
def group():
	return random.choice(['uoadmit', 'testing', 'GTFF'])
def company():
	return random.choice(['gmail', 'uoregon', 'symantec', 'usda'])
def dom():
	return random.choice(['edu', 'com', 'gov', 'org'])


g = Grammar()
g.prod("email", "${Prefix()}@${Suffix()}", max_uses=4, weight=2)
g.prod("Prefix", "${username()}")
g.prod("Prefix", rand_str, rand_flag=True)
g.prod("username", user)
g.prod("username", group)

g.prod("Suffix", "${Service()}.${Domain()}")
g.prod("Service", company)
g.prod("Service", rand_str, rand_flag=True)
g.prod("Domain", dom)
g.prod("Domain", rand_str, rand_flag=True)



class TestCaseSuite:
	'''
	a test case suite has a reference to the grammar and all the rules (productions) in it
	a test case suite also has a mapping between test case generations and the oracle paired with it
	say for example, the email grammar, everytime a g.gen("email") is called,
	the result and its oracle are stored key,value pair in table

	->in email case, the grammar rules are printed as:
	for symbol in self.grammar_env:
	            rep += "\n{} -> {}".format(symbol, self.grammar_env[symbol])
	        rep += "\n*** ------ ***"
	-> the rhs is printed as 
	self.desc="{}|{}".format(self.desc,choice.desc) # if Choice


	->and here are the productions:
	***GRAMMAR***
	Service -> N_3|<function company at 0x101cc22f0>|<function rand_str at 0x100756f28>
	Suffix -> ${Service()}.${Domain()}
	Domain -> N_4|<function dom at 0x101cc2378>|<function rand_str at 0x100756f28>
	email -> ${Prefix()}@${Suffix()}
	username -> N_2|<function user at 0x101ead8c8>|<function group at 0x101cc4a60>
	Prefix -> N_1|${username()}|<function rand_str at 0x100756f28>
	*** ------ ***
	'''
	def __init__(self, grammar):
		self.gram = grammar
		self.table = {}

	def __repr__(self):
		return str(self.gram)

	def gen(self):
		'''
		call self.grammar.gen
		in gen, if the random flag is set, mark an oracle object as "expect false"
		post generation (test case instance) and oracle as key-value pair in table
		'''

testcases = TestCaseSuite(g)
print(testcases)

'''
*** NOTE: oracle definition may not be necessary, I think I can do it with just a string
after all, it's just a word description!
class Oracle:
	def __init__(self):
		self.expected = ''
		self.actual = ''
'''

def isValidEmail(addressToVerify):
	"""
	args:
	addressToVerify -> email address string we want to test validity of
	returns:
	boolean - True if the email is valid, False if not
	*** IN THIS PROJECT'S CURRENT ITERATION:
	SMTP checking does not work - unfixable by time of deadline:( This code only checks email formatting
	An email is valid if it doesn't have syntax errors, i.e.:
	dinosaur@gmail.com is valid, but 'dinosaur@gmail.com is not (note the quote)
	This function also checks the domain (@uoregon.edu, @gmail.com, @nsa.gov, etc.)
	Finally, the function will spin up a tiny SMTP server that attempts to connect to the emails_to_send
	if it can send a message, it's a valid email.
	For example, admissions@uoregon.edu is valid, but yellow@yellow.com doesn't exist
	"""

	#check for valid format
	match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', addressToVerify)
	if match is None:
		return False

	domain = addressToVerify.split('@')[-1] #example: gmail.com, uoregon.edu
	#print("\tthe email is {} and the domain is: {}".format(addressToVerify, domain))
	try:
		records = dns.resolver.query(domain, 'MX')
		print(records)
		mxRecord = records[0].exchange
		mxRecord = str(mxRecord)
	except:
        	#print(sys.exc_info()[0])
        	#print("\tgetting error in dns")
        	return False

    # move on to next round - at this point the email is properly formatted and the domain exists
    # Get local server hostname
	host = socket.gethostname()
    # SMTP lib setup (use debug level for full output)
	server = smtplib.SMTP()
	server.set_debuglevel(0)
    # SMTP Conversation
	print("\temail is {}".format(addressToVerify))
	print("\tmx record is {}".format(mxRecord))
	print("\tserver is {}".format(server))
	try:
		server.connect(mxRecord)
	except (TimeoutError, ConnectionRefusedError):
		return False
	server.helo(host)
	server.mail('me@domain.com')  # parameter is sender's address
	code, message = server.rcpt(str(addressToVerify))
	print("\tthe code is {} and message {}".format(code, message))
	try:
		server.quit()
	except smtplib.SMTPServerDisconnected:
		pass
    # Assume 250 as Success
	if code == 250:
		return True
	return False


for _ in range(30):
	email = g.gen("email")
	print("{} {}".format(email.ljust(25), isValidEmail(email)))







