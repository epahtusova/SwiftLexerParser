def preprocess_comments(content):
    """
    Method combines multiline and inline comments processing
    :param content: source file
    :return: source file with removed comments
    """
    multiline_cleaned = format_multiline_comment(content)
    inline_cleaned = format_inline_comment(multiline_cleaned)
    return inline_cleaned


def format_multiline_comment(content):
    """
    Method removes multiline comments (/* example */)
    :param content: source file
    :return: code without multiline comments
    """
    start = content.find('/*')
    while start != -1:
        end = content.find('*/') + len('*/')
        comment = content[start:end]
        content = content.replace(comment, '')
        start = content.find('/*')
    return content


def format_inline_comment(content):
    """
    Method removes inline comments (//abracadabra)
    :param content: source code
    :return: code without inline comments
    """
    start = content.find('//')
    while start != -1:
        end = content[start:].find('\n')  # End in a substring from start index
        if end == -1:
            end = len(content)
        end = start + end

        comment = content[start:end]
        content = content.replace(comment, '')
        start = content.find('//')
    return content
