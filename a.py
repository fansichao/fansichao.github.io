
func_lis = []
for i in range(4):
    def makefunc(i):
        def func(x):
            return x*i
        return func
    func_lis.append(makefunc(i))

for f in func_lis:
    print(f(2))
 