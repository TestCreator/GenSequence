#Multiplication practice
def multiplier_of(num):
	def mult(n):
		return n*num
	return mult

x = multiplier_of(5)
t = x(4)
print(t)

#Print Titles
def print_message(prefix):
	def edit(name):
		return prefix + name
	return edit
title = print_message("Dr.")
label = title("Jones")
print(label + '\n')

#Decorator Practice
def jazz_it_up(execute):
	def beautify(guy):
		print("***")
		execute(guy)
		print("***")
	return beautify

@jazz_it_up
def print_name(name):
	print(name)

#really means:
#print_name = jazz_it_up(print_name)
print_name("Mr. Business")
