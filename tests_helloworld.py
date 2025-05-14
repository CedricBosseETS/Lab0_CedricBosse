from helloworld import hello_world

"""Test qui regarde le output de hello_world"""
def test_hello_world():
    assert hello_world() == "Hello World"

"""Test qui regarde si le output de hello_world est du bon type"""
def test_hello_world_returns_string():
    result = hello_world()
    assert isinstance(result, str)