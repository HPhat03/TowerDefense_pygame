def foo(func):
    def inner():
        print("foo")
        func()
    return inner

@foo
def bar():
    print("bar")

bar()