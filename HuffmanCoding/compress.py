"""This is a Huffman compressor, as explained by Tom Scott in "The Basics" series on Youtube.
Once the tree is generated, you can use it to compress the file.

generate_tree: Create the Huffman Tree using the BinaryTree class
	- BinaryTree nodes include the character, its frequency, and pointers to the children
dictionary: Map each character in the tree to a unique binary code based on its location in the tree
	- This is used to prevent searching for every character during compression
compress: Uses the Huffman Tree to compress the file, using the dictionary provided
	- Returns the original file's size in bits, as well as that of the compressed file
		- Keep in mind that the Huffman file has been extended to the nearest byte by padding the end with 0s
		This is to ensure that the file is still readable as byte data, as well as that the final string
		when written in bytes is not front-padded, which disrupts the codes"""

from queue import SimpleQueue
from sys import argv
from pickle import dump

"""This version end-pads the Huffman file with enough 0s to fulfill the byte. 
Thus the final (<8) bits are NOT front-padded. 
GUESS: In the decompression, those padded 0s do not reach a leaf 
( does it never reach off the tree, into None territory?)"""

""" The goal of this version was to not front-pad ( automatic if there are not 8 bits) or back-pad ( see huffman2) 
the bit stream from compress. However, this may not be possible as computers may only store bytes, 
not specific numbers of bits. Additionally, front padding is worse than back-padding, since that has to wait 
for the final character to delete the padding, so we will most likely stick to the back-padding in huffman2"""


def generate_tree(fname):
	nodes = {}
	"""Create a dictionary that maps a character to its Tree Node"""
	with open(fname) as read:
		for line in read:
			for char in line:
				if char not in nodes:
					nodes[char] = BinaryTree(char)
				nodes[char].increment()

	"""Create a list of Tree Nodes, sorted in descending order by their frequency"""
	freqtable = sorted(nodes.values(), key=lambda node: node.freq, reverse=True)
	del nodes, read, line, char

	"""Reassemble the list as Tree using the left and right tree variables"""
	while len(freqtable) != 1:  # Reassemble as a tree
		one, two = freqtable.pop(), freqtable.pop()
		subtree = BinaryTree('*', one.freq + two.freq, one, two)
		freqtable = insert(freqtable, subtree)

	del one, two, subtree
	return freqtable.pop()  # Final element in the list, full tree


def dictionary(peach):
	q = SimpleQueue()
	new_dict = {}
	q.put(('', peach))
	while not q.empty():
		code, node = q.get()
		if not node:
			continue
		new_dict[node.char] = code
		q.put((code + '0', node.left))
		q.put((code + '1', node.right))
	return new_dict  # key: character, value: binary code for Huffman tree


def compress(fname, kiwi: dict):
	fsize, csize = 0, 0
	bitstring = ''
	with open(fname) as read, open('Huffman_' + fname, 'wb') as write:
		for line in read:
			for char in line:
				bitstring += kiwi[char]
				fsize += 8  # every char will be a byte (8 bits)
				if len(bitstring) >= 8:
					write.write(bytes([int(bitstring[:8], 2)]))  # write 8 bits at a time
					csize += 8
					bitstring = bitstring[8:]  # discard read byte
		bitstring += '0' * [0, 7, 6, 5, 4, 3, 2, 1][len(bitstring) % 8]  # adds enough 0s to get a full byte
		write.write(bytes([int(bitstring, 2)]))  # write final byte

	return fsize, csize


def insert(apple: list, node):
	i = 0
	for i in range(len(apple)):
		if apple[i].freq <= node.freq:  # list is sorted greatest to least, find the earliest smaller item
			break
	return apple[:i] + [node] + apple[i:]  # insert before the earliest smaller


class BinaryTree:
	def __init__(self, char, freq=0, left=None, right=None):
		self.char = char
		self.freq = freq
		self.left = left
		self.right = right

	def __str__(self):
		return "Char:{}\nCount:{}".format(self.char, self.freq)

	def increment(self):
		self.freq += 1




if __name__ == '__main__':
	filename = argv[1]
	tree = generate_tree(filename)
	with open('PickledTree_' + filename, 'wb') as rick:
		dump(tree, rick)
	filesize, compsize = compress(filename, dictionary(tree))
	print(' Original Size: %d bits' % filesize)
	print('  Huffman Size: %d bits' % compsize)
	print('Size Reduction: {:.2%}'.format(1 - compsize / filesize))
	print()

# def compress(fname, kiwi: dict):
# 	fsize = 0
# 	bitstring = ''
# 	with open(fname) as read:
# 		for line in read:
# 			for char in line:
# 				bitstring += kiwi[char]
# 				fsize += 8  # every char will be a byte (8 bits)
#
# 	bitstring += '0' * [0, 7, 6, 5, 4, 3, 2, 1][len(bitstring) % 8]  # adds enough 0s to get a full byte
# 	csize = len(bitstring)
# 	with open('Huffman_' + fname, 'wb') as write:
# 		while bitstring:
# 			write.write(bytes([int(bitstring[:8], 2)]))  # write 8 bits at a time
# 			bitstring = bitstring[8:]
# 	return fsize, csize
