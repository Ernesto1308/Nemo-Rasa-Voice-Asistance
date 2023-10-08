import base64


# Serialize bytes to a string representation
def serialize_bytes(data: bytes) -> str:
    encoded_bytes = base64.b64encode(data).decode('utf-8')
    return encoded_bytes


# Deserialize string representation to bytes
def deserialize_bytes(encoded_bytes: str) -> bytes:
    decoded_bytes = base64.b64decode(encoded_bytes)
    return decoded_bytes
