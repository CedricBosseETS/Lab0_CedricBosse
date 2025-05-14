from helloworld import hello_world

def test_hello_world():
    assert hello_world() == "Hello World"

def test_hello_world_returns_string():
    result = hello_world()
    assert isinstance(result, str)