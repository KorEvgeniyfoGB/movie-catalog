from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent
MOVIE_STORAGE_FILE_PATH = BASE_DIR / "storage.json"


# if __name__ == "__main__":
#     print(MOVIE_STORAGE_FILE_PATH)
#     print(IS_MOVIE_STORAGE_EXIST)
