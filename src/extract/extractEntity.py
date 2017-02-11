import os
import sys
import re

term = re.compile(r'(<>|)')
def find_term(ttl, st):
    length = len(ttl)
    while st < length and ttl[st] == " ":
        st += 1

    if ttl[st] == "<":
        end_char = ">"
    elif ttl[st] == '"':
        end_char = '"'
    else:
        end_char = " "
    ed = st + 1
    
    while ed < length:
        ed += 1
        if ttl[ed-1] == end_char:
            break
    while ed < length and ttl[ed] != " ":
        ed += 1
    while ed > st and ttl[ed-1] == " ":
        ed -= 1
    return st, ed
    
    

def parse_ttl(ttl):
    ttl = ttl[:-2]
    parts = ttl.split("\t")
    return parts

def parse_label(label):
    r = label.rfind('"')
    return label[1:r]

if __name__ == "__main__":
    # print parse_label(parse_ttl('<Acute_gpericarditis>	<isPreferredMeaningOf>	"Acute pericarditis"@eng .')[2])
    data_file = sys.argv[1]
    label_file = sys.argv[2]
    exactly_match_file = sys.argv[3]
    fuzzy_match_file = sys.argv[4]

    out_exact = file(exactly_match_file, 'w')
    out_fuzzy = file(fuzzy_match_file, 'w')

    fuzzy_labels = set()
    exactly_labels = set()
    terms = set()
    for line in file(data_file):
        line = line.strip()
        if line == "":
            continue
        terms.add(line)
    
    for cnt, line in enumerate(file(label_file)):
        if cnt % 100000 == 0:
            print "\tcnt = %d" %cnt
        if line.startswith("#") or line.startswith("@"):
            continue
        line = line.strip()
        if line == "":
            continue

        parts = parse_ttl(line)
        label = parse_label(parts[2])
        for term in terms:
            if term.startswith(label) or label.startswith(term):
                fuzzy_labels.add(parts[0])
                print "add fuzzy label %s" %parts[0]
            if term == label:
                exactly_labels.add(parts[0])
                print "add exact label %s" %parts[0]

    for label in sorted(exactly_labels):
        out_exact.write(label + "\n")
    out_exact.close()

    for label in sorted(fuzzy_labels):
        out_fuzzy.write(label + '\n')
    out_fuzzy.close()



        