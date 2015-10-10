from __future__ import division
import sys,json, math
from collections import defaultdict



class Freq:

	def __init__(self, file):
		
		self.wordcount = {}
		self.wordcount = defaultdict(int)
		
		self.nonterm = {}
		self.nonterm = defaultdict(int)
		
		self.unary = {}
		self.unary=defaultdict(int)

		self.unary_rules = {}

		self.binary = {}
		self.binary=defaultdict(int)

		self.binary_rules = {}
		##self.binary_rules = defaultdict() ##key is the root, value is the list of tuples X can generate
	
		self.taglist = []

		self.has_unary = []

		self.has_binary = []

		for l in file:

			line = l.strip().split()
			
			count = float(line[0])
			
			if line[1] == "NONTERMINAL":
				
				self.nonterm[line[2]] = count
				if line[2] in self.taglist: 
					pass
				else: self.taglist.append(line[2])
			
			elif line[1] == "UNARYRULE":
				
				key = (line[2], line[3])
				
				self.unary[key] = count
				
				## keeping a word counter here as well
				self.wordcount.setdefault(line[3], 0)
				
				self.wordcount[line[3]] += count
				
				if line[2] in self.unary_rules:
					if line[3] not in self.unary_rules[line[2]]:
						self.unary_rules[line[2]].append(line[3])
				else:
					self.unary_rules[line[2]] = [line[3]]

				self.has_unary.append(line[2])


			elif line[1] == "BINARYRULE":	
				
				self.binary[tuple(line[2:])] = count
				
				if line[2] not in self.taglist: taglist.append(line[2])
				if line[3] not in self.taglist: taglist.append(line[3])
				if line[4] not in self.taglist: taglist.append(line[4])
				
				if line[2] in self.binary_rules:
					if (line[3], line[4]) not in self.binary_rules[line[2]]:
						self.binary_rules[line[2]].append((line[3], line[4]))
				else:
					self.binary_rules[line[2]] = [(line[3], line[4])]

				self.has_binary.append(line[2])
	

	def tagList(self):
		return self.taglist

	def has_unary_rule(self, x, w):
		if x in self.has_unary:
			if w in self.unary_rules[x]:
				return 1
		else: return 0

	def has_binary_rule(self, x,yz):
		if x in self.has_binary:
			if yz in self.binary_rules[x]:
				return 1
		else: return 0

	def has_binary_root(self, x):
		if x in self.has_binary:
			return 1
		else: return 0

	
	def binary_rule_list(self, tag):

		return self.binary_rules.get(tag, []) ## return an empty list if does not have binary rules

	def nontermcount(self, key):

		return self.nonterm[key]

	def binarycount(self, key):
		return self.binary[key]


	def qXYZ(self, x, yz):

		return float(self.binary[(x, yz[0], yz[1])] / self.nonterm[x])

		 ## if nonterm is zero, we will make the probability 0 by making the denominator infinite


	def qXw(self, x, w):
		
		if self.wordcount[w]<5:

			return float(self.unary[(x, "__RARE__")] / self.nonterm[x])

		else:
			##print "common word identified:", w, " trying tag: ", x
			##print "unary rule occurrence:", self.unary.get((x,w), 0)
			##print "nonterm occurence:", self.nonterm.get(x, 0)

			return float(self.unary[(x, w)] / self.nonterm[x])


	
	def checkRare(self, word):
		if self.wordcount[word]<5:
			return "__RARE__"
		else:
			return word;


class ParseTree:

	def __init__(self, tree, freq):
		
		#for l in treeFile:

			#self.tree = json.loads(l.strip())

		self.freq = freq
		self.treeFile = open(tree)

		
		
	def clean(self):


		line = self.treeFile.readline()
		while line:
			self.tree = json.loads(line)
			self.washTree(self.tree, self.freq)
			print json.dumps(self.tree)
			line = self.treeFile.readline()



	def washTree(self, tree, freq):

		if len(tree) == 3:
			self.washTree(tree[1], freq)
			self.washTree(tree[2], freq)

		elif len(tree) == 2:
			tree[1] = freq.checkRare(tree[1])
			#print "Found rare word! the word is", tree[1]

	def printTree(self):

		print json.dumps(tree)















