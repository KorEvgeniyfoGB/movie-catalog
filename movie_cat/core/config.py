import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
MOVIE_STORAGE_FILE_PATH = BASE_DIR / "storage.json"


LOG_LEVEL = logging.INFO
LOG_FORMAT: str = (
    "[%(asctime)s.%(msecs)03d] %(module)12s:%(lineno)-3d %(levelname)-7s - %(message)s"
)

# if __name__ == "__main__":
#     print(BASE_DIR)
#     print(MOVIE_STORAGE_FILE_PATH)
# only for experiments
API_TOKENS = frozenset(
    {
        "9Uzk-h4XiNGleLxqrbJyOA",
        "l5Tqx81w0Ufx_JiOUiRWew",
    }
)
