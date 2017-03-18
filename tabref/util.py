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

    if len(text) < 4:
        return

    text = u' %s ' % text
    return text.encode('utf-8')
