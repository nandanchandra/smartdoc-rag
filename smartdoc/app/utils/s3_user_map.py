import os
from typing import Tuple


def extract_user_id_filename(s3_key: str) -> Tuple[str, str]:
    user_id, filename_with_ext = os.path.split(s3_key)
    return [user_id, filename_with_ext]
