####In dieser Datei können Tests definiert werden######

from app.__init__ import create_app

def test_BeispielTest():
    add = 1+1
    assert 2
    return add

def test_app():
    app = create_app()
    assert app is not None
    
    hello = app.hello()
    assert hello is not None
