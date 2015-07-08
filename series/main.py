import codecs
import re


file = open('handles.csv')
doi = dict()

for line in file:
    line = line.strip()

    pattern = '^([0-9]+),([0-9/]*)'
    match = re.match(pattern, line)

    doi[int(match.group(1))] = match.group(2)



file = codecs.open('series.txt', encoding='utf-8')
outfile = codecs.open('../src/misc/s7_series_list.tex', 'w', 'utf-8')

for line in file:
    line = line.strip()

    if len(line) <= 1:
        continue

    pattern = "^([0-9]+).\s*([^\(]*)\(([0-9]+)\). (.*)$"

    match = re.match(pattern, line)

    if not match:
        print "Parse error: " + line
        break

    nr = match.group(1).strip()
    author = match.group(2).strip()
    year = match.group(3).strip()

    remainder = match.group(4)

    #print remainder[::-1]


    pattern = '([^,]*),([^,]*),([^.]*).(.*)'
    match = re.match(pattern, remainder[::-1])

    if not match:
        print "Parse error:" + remainder
        print "Line: " + line
        break

    country = match.group(1)[::-1].strip()
    city = match.group(2)[::-1].strip()
    university = match.group(3)[::-1].strip()
    title = match.group(4)[::-1]

    if country[-1] == ".":
        country = country[0:-1]

    if title[-1] != '.':
        title = title + '.'

    outfile.write("\\dientry{" + nr + "}{" + author + "}")
    outfile.write("{" + year + "}\n\t{" + title + "}\n\t")
    outfile.write("{" + university + "}{" + city + "}{" + country + "}")

    if int(nr) in doi:
        outfile.write("{" + doi[int(nr)] + "}")
    else:
        outfile.write("{}")
        print "Missing DOI:"
        print "\t" + author + " (" + year + ")"
        print "\t" + title

    outfile.write("\n")

outfile.close()
