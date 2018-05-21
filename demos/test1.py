class Test:
    def __init__(self, a, b):
        self.a = a
        self.b = b
    def run_operations(self, operation, *args, **kwargs):
        try:
            function = self.functions[operation]
        except KeyError:
            print("bad")
        else:
            function(self, args, kwargs)

    def function_a(self, *args, **kwargs):
        print ("A")

    def function_b(self, *args, **kwargs):
        print ("B")

    functions = {
        'operation_a' : function_a,
        'operation_b' : function_b,
        }

#print(Test.functions)

t = Test(1, 2)
#print(t.functions)
#print(t.functions['operation_a'])
t.function_a()
t.functions['operation_a'](t)