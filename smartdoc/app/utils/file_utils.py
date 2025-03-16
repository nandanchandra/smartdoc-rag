from loguru import logger

def decode_s3_content(content: bytes, encoding: str = "utf-8") -> str:
    try:
        return content.decode(encoding)
    except UnicodeDecodeError as e:
        logger.error(f"Failed to decode S3 content: {str(e)}")
        return ""