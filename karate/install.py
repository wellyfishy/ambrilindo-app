import subprocess

def start_install():
    try:
        subprocess.run(f'pip install -r requirements.txt')
    except KeyboardInterrupt:
        # Handle Ctrl+C (KeyboardInterrupt) gracefully.
        print("Stop")
        input()

if __name__ == "__main__":
    start_install()