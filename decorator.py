def calculatetime(func):
    def wrapper(A):
        A.name +='decorator'
        func(A)
        print('after')
    return wrapper

class A(object):
    def __init__(self):
        self.name = 'A'
        self.value = 1

    @calculatetime
    def foo(self):
        print(self.name + 'foo')

a =A()
a.foo()

