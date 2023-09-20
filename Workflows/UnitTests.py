# test_executability.py
import sys



def test_imports():
    try:
        sys.path.append('..\\app')   
        import controller

    except ImportError as e:
        assert False, f"Importfehler: {e}"

def test_functionality():
    # Hier können Sie Ihre eigenen Funktionen und Tests hinzufügen
    assert 1 + 1 == 2, "1 + 1 sollte 2 ergeben"

if __name__ == "__main__":
   
    test_imports()
    test_functionality()
   
    print(sys.path)
    print("Alle Tests erfolgreich durchgeführt.")
