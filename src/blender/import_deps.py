import subprocess
import sys

def import_deps():
    real_path_b = subprocess.check_output(["python3", "-c", "import sys; print(sys.path)"])
    real_path = eval(real_path_b.decode())
    for r in real_path:
        sys.path.append(r)


if __name__ == "__main__":
    import_deps()
