import json
import sys


SCORE_THRESHOLD = 80
NORM = (100 - SCORE_THRESHOLD) / 2

def main():
    if len(sys.argv) == 3:
        json_path = sys.argv[1]
        png_path = sys.argv[2].rstrip('/')
    else:
        usage = "Usage: %s <JSON scores> <PNG dir>\n"
        sys.stderr.write(usage % sys.argv[0])
        sys.exit(1)

    with open(json_path, 'r') as json_file:
        results = json.load(json_file)

    edges = dict()
    hosts_used = set()

    with open(json_path) as scores_file:
        scores = json.load(scores_file)

    score_dict = {s['similarity']:(s['path1'],s['path2']) for s in scores}

    for score, paths in score_dict.items():
        if score > SCORE_THRESHOLD:
            host1 = paths[0][5:-5]
            host2 = paths[1][5:-5]

            hosts_used.add(host1)
            hosts_used.add(host2)

            edges[host1,host2] = (score - SCORE_THRESHOLD) / 3


    print('graph {')
    print('  graph [overlap=scale, splines=true];')
    print('  node [shape=box, fixedsize=false, fontsize=8, margin="0.05", width="0", height="0"];')
    print()

    for k,v in edges.items():
        u1, u2 = k
        weight = v

        print('  "%s" -- "%s" [weight=%0.1f, penwidth=%0.1f]' % (u1, u2, weight, weight))

    print()

    for host in hosts_used:
        print('  "%s" [label="%s", image="%s/%s.png"]' % (host, host, png_path, host))

    print('}')

if __name__ == '__main__':
    main()
