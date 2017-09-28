import random
import context
import re
import dns.resolver
import socket
import smtplib
import sys
from makogram.grammar import Grammar


def rand_str(times):
	return ''.join(random.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(times))
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
g.prod("Prefix", rand_str(5))
g.prod("username", user)
g.prod("username", group)

g.prod("Suffix", "${Service()}.${Domain()}")
g.prod("Service", company)
g.prod("Service", rand_str(5))
g.prod("Domain", dom)
g.prod("Domain", rand_str(4))



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
	except TimeoutError:
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




