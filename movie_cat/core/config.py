from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
MOVIE_STORAGE_FILE_PATH = BASE_DIR / "storage.json"


if __name__ == "__main__":
    print(BASE_DIR)
    print(MOVIE_STORAGE_FILE_PATH)
