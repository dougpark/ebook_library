import os
import uuid

def create_testxy_files(num_files=1):
    assert 1 <= num_files <= 1000, "num_files must be between 1 and 1000"
    test_folder = os.path.join('ebooks', 'testxy')
    os.makedirs(test_folder, exist_ok=True)
        # code_gen = CodeGenerator()  # Commented out as we are using UUIDs now
    for _ in range(num_files):
        # Generate a 10-digit UUID (hex, not cryptographically secure, but unique enough for test files)
        code = uuid.uuid4().hex[:10]
        filename = f"testxy-{code}.pdf"
        filepath = os.path.join(test_folder, filename)
        # Create an empty file
        with open(filepath, 'wb'):
            pass
    print(f"Created {num_files} testxy files in {test_folder}")

if __name__ == "__main__":
    import sys
    num = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    create_testxy_files(num)
