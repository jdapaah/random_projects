"""This file is used in accompaniment to compress.py
for recovering the original file from compressed versions using the 'adjacent' tree"""
from pickle import load
from sys import argv
# from HuffmanCoding.compress import BinaryTree
from compress import BinaryTree


def decompress(fname, peach):
	max_len = 0
	with open("Huffman_" + fname, 'rb') as read, open('Decoded_' + fname, 'w') as write:
		bitstring = ''
		for line in read:  # will stop at but include newlines
			for byte in line:  # read 8 bits
				bits = bin(int(byte))[2:]  # bin() looses some front-padding 0 bits
				bits = '0' * [0, 7, 6, 5, 4, 3, 2, 1][len(bits) % 8] + bits  # add back 0s lost by bin()
				bitstring += bits
				max_len = max(max_len, len(bitstring))
				chars, bitstring = letters(bitstring, peach)  # get as many as letters as you can
				write.write(chars)
	print(max_len)


def letters(path, peach):
	collected = ''
	last_starting_point = 0
	node = peach
	for index, bit in enumerate(path):  # trace down the tree
		node = node.left if bit == '0' else node.right  # import BinaryTree
		if node.char != '*':
			collected += node.char
			last_starting_point = index+1
			node = peach
	return collected, path[last_starting_point:]


if __name__ == '__main__':
	filename = argv[1][8:]
	with open('PickledTree_' + filename, 'rb') as rick:
		tree = load(rick)
	print(tree)
	decompress(filename, tree)
