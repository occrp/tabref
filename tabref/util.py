import sys
import six
import fingerprints


def normalize_value(text):
    if text is None:
        return

    try:
        # see if this the cell value clearly numeric:
        float(text)
        return
    except:
        pass

    text = fingerprints.generate(text, keep_order=True)
    if text is None:
        return

    if len(text) <= 3:
        return

    text = u' %s ' % text
    return text.encode('utf-8')


def decode_path(file_path):
    if file_path is None:
        return
    if isinstance(file_path, six.binary_type):
        file_path = file_path.decode(sys.getfilesystemencoding())
    return six.text_type(file_path)
