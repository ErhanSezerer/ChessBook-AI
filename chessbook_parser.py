import os
from diagram_extractor import *
import re
from args import args



def parse():
	#for parsing diagrams
	diagram_parse = False
	diagram_count = 0
	board = []
	diagram_string = ""
	book = ""


	#START PARSING
	path = os.path.join(args.book_path, args.chapter_name)
	with open(path, "r", encoding="utf8") as file_handler:

		for line in file_handler:

			#diagram start
			if line.strip()=="---------------------------------------" and not diagram_parse:
				board.append(line)
				diagram_string += line
				diagram_parse = True
				diagram_count += 1
			#diagram cont.
			elif diagram_parse and not any(x in line for x in ["Diag.","diag.","DIAG.","Diagram 19."]):
				#empty line
				if line==None or line=="" or line=="\n":
					continue
				board.append(line)
				diagram_string += line
			#diagram end
			elif diagram_parse and any(x in line for x in ["Diag.","diag.","DIAG.","Diagram 19."]):
				diagram_parse = False
				if args.out_diag:
					FEN_notation = get_FEN_notation(board)
					diagram_string += ("\nFEN:" + FEN_notation)

					filename = "Diagram" + str(diagram_count) + ".txt"
					output_file = os.path.join(args.diagram_path,filename)
					with open(output_file, "w") as file2write:
						file2write.write(diagram_string)
				diagram_string = ""
			#not a diagram
			else:		
				book += line


	

	#split the book into paragraphs
	book_paragraphs = book.split("\n\n")[3:]#first three are chapter headlines
	
	return book_paragraphs











