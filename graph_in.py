import sys
import re

# filename is a graph.txt file
for filename in sys.stdin:
    filename = filename.strip()
    print 'Processing file: '+filename
    # get directory path and filename
    # TODO tighten regex
    match = re.search('(.*/).+.txt', filename)
    # save directory path for referencing problems
    dirPath = match.group(1)
    dirPieces = dirPath.split('/')
    category = str.lower(dirPieces[1])
    context = str.lower(dirPieces[2])
        # create seed_file for file
    o = open(filename + '_seed', 'w')
    # open source file
    i = open(filename)
    with i, o:
        # add comment seperation for seed file organization
        o.write('#GRAPH TUPLES FROM '+filename+"\n")
        # write graph tuple(s)
        batch_number = 0
        order = -1
        for line in i:
            # remove formatting characters
            line = line.strip()
            makeup_flag = 'false'
            # if it is a whitespace-only line, begin new batch
            if line == '':
                batch_number += 1
                # TODO opportunity to save max order of previous batch?
                # reset order
                order = -1
            # if it is a problem file line
            elif re.match('.*theory.*\.html', line) is None:
                # increase order
                order += 1
                # check if makeup, remove makeup flag
                if line[:1] == '+':
                    makeup_flag = 'true'
                    line = line[1:]
                # find problem_id
                o.write('p = Problem.find_by!(category: \''+category
                        +'\', context: \''+context
                        +'\', filename: \''+line+'\')\n')
                # write graph tuple
                # (filename, context, batch_number, makeup, foreign_key_problem_id)
                batch = str(batch_number)
                makeup = str(makeup_flag)
                o.write('Graph.create!(typ: \'prob\', context: \''+context
                        +'\', batch: '+batch+', makeup: '+makeup
                        +', category: \''+category
                        +'\', order: '+str(order)
                        +', file_id: p.id)\n')
            # must be theory file line
            else:
                # increase order
                order += 1
                # find theory_id
                o.write('t = Theory.find_by!(filename: \''+dirPath+line+'\')\n')
                # write theory tuple
                batch = str(batch_number)
                o.write('Graph.create!(typ: \'theory\', context: \''
                        +context+'\', batch: '+batch+', file_id: t.id, '
                        +'makeup: false'
                        +', order: '+str(order)
                        +', category: \''+category+'\')\n')
