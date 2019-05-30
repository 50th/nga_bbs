import hashlib


def md5_convert(source, salt=None):
    md5 = hashlib.md5()
    if salt:
        md5.update((source+salt).encode("utf-8"))
    else:
        md5.update(source.encode("utf-8"))
    r = md5.hexdigest()
    return r
