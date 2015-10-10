from __future__ import division
import sys,json
import pcfg
from collections import defaultdict
import time


def backtrack(bp, i, j, x, line):
	
	if i == j:
		##print "Found terminal: i = ", i, "j= ",j," word = ", line[i], "tag = ", x
		return (x, line[i])
	
	else:

		bptuple = bp[i, j, x] ## format: ([Y, Z], s)
		##print "bptuple[",i,",",j,",",x,"] = ", bptuple
		y = bptuple[0][0];
		z = bptuple[0][1];
		s = bptuple[1];
		
		return (x, backtrack(bp, i, s, y, line), backtrack(bp, (s+1), j, z, line))

def backtrack_init(p, bp, line, taglist):
	
	##print p[(0,len(line)-1, "S")]

	
	if p.get((i,len(line)-1, "S"), 0) != 0:
		
		prob = p[(0, len(line)-1, "S")]
		return backtrack(bp, 0, len(line)-1, "S", line)

	else: 
		
		##print "p(", line[0] , line[len(line)-1] , "S) is impossible.....?"

		maxp = 0
		end = []
		
		for x in taglist:

			if p.get((0, len(line)-1, x), 0) > maxp:
				maxp = p[(0, len(line)-1, x)]
				end.append(x)

		##print "end candidates include ", end ## no end candidates!
		
		return backtrack(bp, 0, len(line)-1, end[-1], line)





if __name__ == "__main__":

## the viterbi algorithm
## let args[1] be the count file
## let args[2] be the key data

	start_time = time.time()

	freq = pcfg.Freq(open(sys.argv[1]))

	taglist = freq.tagList();

	corpus = open(sys.argv[2])

	## start reading file
	for l in corpus:

		line = l.strip().split() ## get new line, split into array
		
		## get the tables ready
		p = {}
		p = defaultdict(float)
		bp = {}
		## format: key of p is (i, j, X), where X is a member of taglist
		## the value of p is the max probability of (i, j ,X)
		
		## bp has the same key, but the value is a tuple of ([Y, Z], s)
		## when back tracking, we would use the information to access 
		## (i, s, Y) and (s+1, j, Z)

		## start filling in the initial values

		##i = 0;

		for i in range(0, len(line)): ## iterate over each word
			for x in taglist: ## iterate over tag list
				p[(i,i,x)] = freq.qXw(x, line[i])
				##if p[(i,i,x)] != float("-inf"):
					##print "congrats! found a good unary rule for word", line[i], ", corresponding to", x, ", prob = ", p[(i,i,x)]


		## DEBUG: UNARY RULE SHOULD BE GOOD! BEWARE OF THE RANGE OF INDEX!
		
		## initial table filled

		## now we start the actual table filling algorithm

		for l in range(1, len(line)):
			
			for i in range(0, len(line)-l):	
				
				j = i+l
				
				##print "i = ", i, " j=",j,", l = ",l,"word ", i, " is", line[i], "word", j, " is", line[j]

				
				for x in taglist:

					
					##if freq.has_binary_root(x) == 1:
						
						binarylist = freq.binary_rule_list(x) ## note this is a list of tuple [Y,Z], an empty list otherwise
						
						for yz in binarylist:

							p.setdefault((i, j ,x), 0) ## set default to be -inf if no value already
							##bp.setdefault((i,j,x), ())

							##if ()
							for s in range(i, j):
								
								prob_candidate = freq.qXYZ(x, yz) * p.get((i, s, yz[0]), 0) * p.get((s+1, j, yz[1]), 0)
								##if prob_candidate > float("-inf"):
									##print "testing: x = ", x, "y = ", yz[0], "z = ", yz[1], "s = ", s, "line[s] = ", line[s]
									##print "prob_candidate  = " , prob_candidate
								
								if p[(i, j, x)] < prob_candidate: 
									##print "Max prob found...", p[(i, j, x)], "<",prob_candidate
									##print "p(",i,",",j,",",x,") has a new prob of ", prob_candidate
									p[(i,j,x)] = prob_candidate
									bp[(i,j,x)] = (yz, s)

		## now we are done with the table! we need a recursive backtracking algorithm to output the tree
		##print p[(0,len(line)-1, "S")]
	
		print json.dumps(backtrack_init(p, bp, line, taglist))

	print("--- %s seconds ---" % (time.time() - start_time))










