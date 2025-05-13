from helloworld import HelloWorld

def test_HelloWorld():
    assert HelloWorld() == "Hello World"

def test_HelloWorld_returns_string():
    result = HelloWorld()
    assert isinstance(result, str)