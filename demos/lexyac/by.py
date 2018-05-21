def serve(name, **kwargs):
	print(name)
	for item in kwargs.items():
		print(item)

b = {"one": 1, "two": 2}
serve("filename", **b)
