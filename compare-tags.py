import difflib
import lxml.html
import sys


def main():
    if len(sys.argv) == 3:
        path1 = sys.argv[1]
        path2 = sys.argv[2]
    else:
        usage = "Usage: %s <file 1> <file 2>"
        sys.stderr.write(usage % sys.argv[0])
        sys.exit(1)

    tags1 = get_tags(lxml.html.parse(path1))
    tags2 = get_tags(lxml.html.parse(path2))

    diff = difflib.SequenceMatcher()
    diff.set_seq1(tags1)
    diff.set_seq2(tags2)
    print(diff.ratio() * 100)


def get_tags(doc):
    tags = list()

    for el in doc.getroot().iter():
        if isinstance(el, lxml.html.HtmlElement):
            tags.append(el.tag)
        elif isinstance(el, lxml.html.HtmlComment):
            tags.append('comment')
        else:
            raise ValueError('Don\'t know what to do with element: %s' % el)

    return tags


if __name__ == '__main__':
    main()
