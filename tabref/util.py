import fingerprints


def normalize_value(text):
    text = fingerprints.generate(text, keep_order=True)
    if text is not None:
        return text.encode('utf-8')
