import os
from args import args


piecesFEN = {"#R": "r", "#Kt": "n", "#B": "b", "#Q": "q", "#K": "k", "#P": "p",
	      	"^R": "R", "^Kt": "N", "^B": "B", "^Q": "Q", "^K": "K", "^P": "P"}



# Turns the board info into FEN notation from the given array of rows from Lasker's book
def get_FEN_notation(board):
	notation = ""

	for line in board:
		row = ""
		for piece in line.split("|"):
			if piece.isspace():
				row+="1"
			elif piece.strip() in list(piecesFEN.keys()):
				row += piecesFEN[piece.strip()]
		notation += row + "/"
	notation = notation[:-1]
	
	return notation



#parses diagram from the given file in Lasker's notation in his book
def parse_diagram_file(file_path):
	board = []
	excluded_lines=["|---------------------------------------|","---------------------------------------","A","a"]

	with open(file_path, "r") as file_handle:
		for line in file_handle:
			if not any(x in line.strip() for x in excluded_lines):
				board.append(line.strip())
	return get_FEN_notation(board)




#EXAMPLE USAGE
#filename = "Diagram15.txt"
#path = os.path.join(args.diagram_path,filename)
#notat = parse_diagram_file(path)
#if len(notat) != 71:
#	print("error parsing file")
#else:
#	print(notat)

