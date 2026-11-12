
from lzallright import InputNotConsumed, LZOCompressor


def compress_lzo(input_data, level=1, header=False):
    
    return LZOCompressor().compress(bytes(input_data))


def decompress_lzo(input_data, header=False, expected_size=0):
    
    input_data = bytes(input_data)
    output_size_hint = expected_size if expected_size and expected_size > 0 else None
    try:
        return LZOCompressor.decompress(input_data, output_size_hint=output_size_hint)
    except InputNotConsumed as decompression_error:
        if len(decompression_error.args) >= 2 and isinstance(decompression_error.args[1], (bytes, bytearray)):
            return bytes(decompression_error.args[1])
        raise
