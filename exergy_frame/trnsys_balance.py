path_bal = r"C:\Users\jon\Desktop\Energy_zone.BAL.txt"
path_out = r"C:\Users\jon\Desktop\Energy_zone.BAL.csv"

import csv
f_out = open(path_out, 'w')
writer = csv.writer(f_out, delimiter=';')
#, quotechar='"', quoting=csv.QUOTE_ALL


cnt = 0
line_size = None
with open(path_bal, 'rU') as f:
    for line in f:
        print(line)
        #line.split()
        splitline = line.split()
        #print(len(splitline))
        if line_size:
            assert(len(splitline) == line_size)
        line_size = len(splitline)
        writer.writerow(splitline)
        cnt += 1
        if cnt > 3:
            break