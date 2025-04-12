def my_function(a, b, /, *, c, d):
    print(a + b + c + d)
my_function(5, 8, c = 7, d = 8)