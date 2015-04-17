import difflib
import glob
import json
import lxml.html
import sys


def main():
    if len(sys.argv) == 2:
        data_dir = sys.argv[1]
    else:
        usage = "Usage: %s <data dir>\n"
        sys.stderr.write(usage % sys.argv[0])
        sys.exit(1)

    data_dir = data_dir.rstrip('/') + '/'
    html_paths = glob.glob(data_dir + '/*.html')
    diff = difflib.SequenceMatcher()

    total = len(html_paths)
    results = list()

    for i, path1 in enumerate(html_paths):
        print('%s (%d/%d)' % (path1, i+1, total))

        diff.set_seq1(get_tags(lxml.html.parse(path1)))

        for path2 in html_paths:
            if path1 >= path2:
                continue

            diff.set_seq2(get_tags(lxml.html.parse(path2)))
            similarity = diff.ratio() * 100

            results.append({
                'path1': path1,
                'path2': path2,
                'similarity': similarity
            })

            # print("%s -> %s: %0.1f%% Predicted:%s Actual:%s" % (path1, path2, similarity, predict_same, actual_same))

    with open('compare-tags.json', 'w') as json_out:
        json.dump(results, json_out, indent=4)

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
