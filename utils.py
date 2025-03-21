import os


def exists_file(path: str):
    try:
        assert os.path.exists(path) \
            and os.path.isfile(path)
        return path
    except AssertionError:
        raise AssertionError(f"Caminho inválido: {path}")
    
def mk_dir(path: str):
    try:
        os.makedirs(path, exist_ok=True)
        assert os.path.exists(path) and os.path.isdir(path)
        return path
    except AssertionError:
        raise AssertionError(f"Caminho inválido: {path}")