"""This file is used in accompaniment to compress.py
for recovering the original file from compressed versions using the 'adjacent' tree"""
from pickle import load
from sys import argv
from compress import BinaryTree


# def decompress(fname, peach):
# 	with open(fname, 'rb') as read, open('Decoded_' + fname[8:], 'w') as write:
# 		bitstring = ''
# 		node = peach
# 		ind = 0
# 		for line in read:
# 			for byte in line:  # read 8 bits
# 				one = bin(int(byte))[2:]  # bin() looses some front-padding 0s
# 				one = '0' * [0, 7, 6, 5, 4, 3, 2, 1][len(one) % 8] + one  # add back 0s lost by bin()
# 				bitstring += one
# 				node
# 				if node.char != '*':
# 					write.write(node.char)



# 		del line, byte, one, read
# 		code = ''
# 		for bit in bitstring:
# 			code += bit
# 			char, code = letter(code, peach)  # get the character to print and the code for the next letter



def decompress(fname, peach):
	with open(fname, 'rb') as read, open('Decoded_' + fname[8:], 'w') as write:
		bitstring = ''
		for line in read:
			for byte in line:  # read 8 bits
				one = bin(int(byte))[2:]  # bin() looses some front-padding 0s
				one = '0' * [0, 7, 6, 5, 4, 3, 2, 1][len(one) % 8] + one  # add back 0s lost by bin()
				bitstring += one
		del line, byte, one, read
		code = ''
		for bit in bitstring:
			code += bit
			char, code = letter(code, peach)  # get the character to print and the code for the next letter
			write.write(char)


def letter(path, peach):
	for bit in path:  # trace down the tree
		peach = peach.left if bit == '0' else peach.right  # import BinaryTree
	if peach.char == '*':
		return '', path  # if the code does not map to a leaf, this will write nothing
	return peach.char, ''  # if the code maps to a leaf, clear the code for the next character


if __name__ == '__main__':
	filename = argv[1]
	with open('PickledTree_'+filename[8:], 'rb') as rick:
		tree = load(rick)
	decompress(filename, tree)
