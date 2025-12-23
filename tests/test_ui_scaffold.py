import os

def test_frontend_scaffold():
    """Verifica que el scaffold de React + Vite + TS existe."""
    base_path = "ui"
    required_files = [
        "package.json",
        "tsconfig.json",
        "vite.config.ts",
        "src/main.tsx",
        "src/App.tsx",
        "index.html",
        "postcss.config.js",
        "tailwind.config.js"
    ]
    
    for file_path in required_files:
        full_path = os.path.join(base_path, file_path)
        assert os.path.exists(full_path), f"Missing expected file: {full_path}"

if __name__ == "__main__":
    try:
        test_frontend_scaffold()
        print("Tests passed!")
    except AssertionError as e:
        print(f"Tests failed: {e}")
        exit(1)
