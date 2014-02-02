creatures = []

with open('creatures.txt') as f:
	for line in f.readlines():
		line = line.strip()
		if '(' in line:
			line = line.split('(')[0]
		if ',' in line:
			line = ' '.join(line.split(',')[::-1])
		creatures.append(line.strip())

print "char* creatures[%d] = {" % len(creatures)
for creature in creatures:
	print "\t\"" + creature + "\","
print "};"