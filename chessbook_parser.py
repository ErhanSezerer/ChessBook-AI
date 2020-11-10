import os
from diagram_extractor import *
#from move_operations import *
import re
import string
import numpy as np
import csv



###############################################################################################################################
#########################   LOCAL FUNCTIONS (HELPER FUNCTIONS)   ##############################################################
###############################################################################################################################
###
###
###
###
###
def detect_paragraph_transitions(book_paragraphs):
	addition_terms = {"furthermore","moreover","in addition","also","besides","further","and","not only…but also","both X and Y","as well as"}
	addition_terms_refined = {"Diagram","furthermore","moreover","in addition","also","besides","further","as well as"}
	example_terms = {"for example","for instance","to illustrate","specifically","such as","in particular","namely","one example is","for one","not the least"}
	example_terms_refined = {"case","example","for example","for instance","to illustrate","specifically","such as","in particular","namely","one example is","for one","not the least"}
	contrast_terms = {"in contrast","however","yet","at the same time","nevertheless","though","although","conversely","while","on the one hand","on the other hand","on the contrary"}
	comparison_terms = {"similarly","likewise","similar to","by comparison","in a similar manner","in the same way","by the same token","in similar fashion"}
	emphasis_terms = {"indeed","of course","in fact","most importantly","above all","certainly","besides","further","undoubtedly","especially","truly"}
	addition_terms_refined.update(example_terms_refined)
	addition_terms_refined.update(contrast_terms)
	addition_terms_refined.update(comparison_terms)
	addition_terms_refined.update(emphasis_terms)
	bag_of_transition_paragraphs = dict()
	for paragraph in book_paragraphs:
		for term in addition_terms_refined:
			result = paragraph.find(term)
			if result != -1 and result < 120:
				paragraph_index = book_paragraphs.index(paragraph)
				if paragraph[0].isupper():
					try:
						bag_of_transition_paragraphs[paragraph_index].append(term)
					except KeyError:
						bag_of_transition_paragraphs[paragraph_index] = [term]

	return bag_of_transition_paragraphs
###
###
###
###
###
def print_bag_of_transition_paragraphs(book_paragraphs,bag_of_transition_paragraphs):
	for item in bag_of_transition_paragraphs:
		print(book_paragraphs[item] + "\n")
		print(bag_of_transition_paragraphs.get(item))
		print("\n")
###
###
###
###
###
def segment_numbered_items(context, paragraph_ids, print_all=False):
	updated_paragraphs = []
	updated_ids = []
	for i in range(len(context)):
		new_paragraph = context[i].replace('\n',' ')
		diagrams, moves, text_moves, num_items = extract_special_tokens(new_paragraph, num_item=True)
		if num_items == None:
			updated_paragraphs.append(context[i])
			updated_ids.append(paragraph_ids[i])
		else:
			temp_par = segment_numbered_items_helper(new_paragraph)
			updated_paragraphs.extend(temp_par)
			for item in temp_par:
				updated_ids.append(paragraph_ids[i])
				
	if print_all:
		for item in new_paragraphs:
			print(item)
			print("--------------")

	return updated_paragraphs, updated_ids
###
###
###
###
###
def segment_numbered_items_helper(paragraph):
	#regex for finding numbered items to catch move pairs
	r_seq_start = r'(\s?[\d]+\.)(\s*)?'
	r_seq_mid = r',?(\s+)'
	r_formal_seq_special = r'((Castles|castles)( )?(QR|KR)?|\.\.\.)'
	r_formal_seq = r'(R|Kt|B|Q|K|P)(\n)?(R|Kt|B|Q|K|P)?(\n)?(-|x|X)(\n| )?(R|Kt|B|Q|K|P)(R|Kt|B|Q|K|P)?(\d)?(\s)?(double)?(\s)?(ch)?(\s)?(mate)?'
	r_formal_seq_end = r'(\!+|\?+|;|,|\.)'
	re_numbered_item = re.compile("(%s(%s|%s)%s?(%s(%s|%s)%s?)?)"%(r_seq_start, r_formal_seq, r_formal_seq_special, r_formal_seq_end, r_seq_mid, r_formal_seq, r_formal_seq_special, r_formal_seq_end))

	#get the starting and ending indices of each numbered item in paragraph
	found_numbered_items = re_numbered_item.finditer(paragraph)
	new_paragraphs = []
	sub_paragraph = ""
	start = 0
	next_start = 0
	next_end = len(paragraph)
	end = len(paragraph)

	#segment them from text
	for item in found_numbered_items:
		next_start = item.start()
		next_end = item.end()
		if start==0 and next_start==0:
				sub_paragraph += paragraph[next_start:next_end]
		else:
			if next_start > start:
				if sub_paragraph:
					new_paragraphs.append(sub_paragraph)
				new_paragraphs.append(paragraph[start:next_start])
				sub_paragraph = paragraph[next_start:next_end]
			else:
				sub_paragraph += paragraph[next_start:next_end]
		
		start = next_end
	if sub_paragraph:
			new_paragraphs.append(sub_paragraph)
			new_paragraphs.append(paragraph[next_end:end])

	return new_paragraphs
###
###
###
###
###
def extract_special_tokens(paragraph, diagram=False, move=False, text_move=False, num_item=False, print_all=False):

	#tokens to search for
	diagrams = None
	moves = None
	text_moves = None
	num_items = None


	#regex for finding diagram referrals
	r_single_refer = r'(Diagram|diagram|diag.|Diag.)(\n)?\s{1}?(\n)?[0-9]+'
	r_multi_refer = r'(Diagrams|diagrams)(\n)?\s{1}?(\n)?[0-9]+(\n)?\s{1}?(\n)?and(\n)?\s{1}?(\n)?[0-9]+'
	re_diagram  = re.compile("(%s|%s)"%(r_single_refer,r_multi_refer))

	#regex for finding formal moves
	r_formal = r'\s{1}(R|Kt|B|Q|K|P)(R|Kt|B|Q|K|P)?\s?(-|x|X)\s?(\n)?(R|Kt|B|Q|K|P)(R|Kt|B|Q|K|P)?(\d)?(\s)?(double)?(\n)?(\s)?(ch)?(mate)?'
	re_move = re.compile("(%s)"%(r_formal))

	#regex for finding textual move descriptions
	r_move_desc = r'(\w+)\s{1}(from|to|at|on|with)(\s|\n)?(R|Kt|B|Q|K|P)?-?(R|Kt|B|Q|K|P)\d'
	re_movetextual = re.compile("(%s)"%(r_move_desc))

	#regex for finding numbered items to catch move pairs
	r_seq_start = r'(\s?[\d]+\.)(\s*)?'
	r_seq_mid = r',?(\s+)'
	r_formal_seq_special = r'((Castles|castles)( )?(QR|KR)?|\.\.\.)'
	r_formal_seq = r'(R|Kt|B|Q|K|P)(\n)?(R|Kt|B|Q|K|P)?(\n)?(-|x|X)(\n| )?(R|Kt|B|Q|K|P)(R|Kt|B|Q|K|P)?(\d)?(\s)?(double)?(\s)?(ch)?(\s)?(mate)?'
	r_formal_seq_end = r'(\!+|\?+|;|,|\.)'
	re_numbered_item = re.compile("(%s(%s|%s)%s?(%s(%s|%s)%s?)?)"%(r_seq_start, r_formal_seq, r_formal_seq_special, r_formal_seq_end, r_seq_mid, r_formal_seq, r_formal_seq_special, r_formal_seq_end))
	

	if diagram:
		found_diag = re_diagram.findall(paragraph)
		if len(found_diag)!=0:
			diagrams = found_diag
			if print_all:
				print("diagrams:")
				for i in range(len(found_diag)):
					print(found_diag[i][0])

	if move:
		found_move = re_move.findall(paragraph)
		if len(found_move)!=0:
			moves = found_move
			if print_all:
				print("moves:")
				for i in range(len(found_move)):
					print(found_move[i][0])

	if num_item:
		found_numbered_item = re_numbered_item.findall(paragraph)
		if len(found_numbered_item)!=0:
			num_items = found_numbered_item
			if print_all:
				print("numbered items:")
				#initial_board_fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
				#play_move_sequence(found_numbered_item,initial_board_fen)
				for item in found_numbered_item:
					print(item[0].strip())
				
	if text_move:
		found_textual_move = re_movetextual.findall(paragraph)
		if len(found_textual_move)!=0:
			text_moves = found_textual_move
			if print_all:
				print("textual move descriptions:")
				for i in range(len(found_textual_move)):
					print(found_textual_move[i][0])

	if print_all:
		print("Paragraph:\n" + paragraph)
		print("----------------------------")

	return 	diagrams, moves, text_moves, num_items
###
###
###
###
###
### rearrange context for paragraphs between two move sequences depending on diagram referrals
### inputs: list of strings (paragraphs)
###			list of int (paragraph flags)
### output: inputs: list of strings (newly organized paragraphs)
###			list of int (newly organized paragraph flags)
def parse_book_enhanceWdiags(contexts, contexts_flags):
	new_contexts = []
	new_context =[]	
	new_contexts_flags = []
	new_context_flags = []
	last_diagram = 0
	found_diag = False		
	found_seqend = False
	found_start = False
	for i in range(len(contexts_flags)):
		num_seq = contexts_flags[i].count(1)
		
		for j in range(len(contexts_flags[i])):
			#case 0  -> no diag, no seq
			if contexts_flags[i][j] == 0:
				new_context.append(contexts[i][j])
				new_context_flags.append(0)
			#case 1  -> seq
			elif contexts_flags[i][j] == 1:
				if not found_start:
					found_start=True
					new_contexts.append(new_context)
					new_contexts_flags.append(new_context_flags)
					new_context = []
					new_context_flags = []
				if found_seqend:
					found_seqend = False
					
				new_context.append(contexts[i][j])
				new_context_flags.append(1)
				num_seq -= 1
				if num_seq == 0:
					found_seqend = True
			#case -1 -> diag, no seq
			elif contexts_flags[i][j] == -1:

				diagrams, _, _, _ = extract_special_tokens(contexts[i][j], diagram=True)
				diag_ref = []
				for diagram in diagrams:
					diag_ref.append(re.findall(r'\d+', diagram[0].strip())[0])
				min_diagref = min(diag_ref)
				max_diagref = max(diag_ref)
				if last_diagram == 0:
					last_diagram = max_diagref

				if not found_start:
					found_start=True
					new_contexts.append(new_context)
					new_contexts_flags.append(new_context_flags)
					new_context = []
					new_context_flags = []
			
				if found_seqend:
					if min_diagref > last_diagram:
						new_contexts.append(new_context)
						new_contexts_flags.append(new_context_flags)
						new_context = []
						new_context_flags = []
						found_diag = True
						new_context_flags.append(-1)
						new_context.append(contexts[i][j])
					else:
						new_context.append(contexts[i][j])
						new_context_flags.append(-1)
				else:
					new_context.append(contexts[i][j])
					new_context_flags.append(-1)
		if not found_diag:
			new_contexts.append(new_context)
			new_contexts_flags.append(new_context_flags)
			new_context = []
			new_context_flags = []
		found_diag = False
	if len(new_context_flags) != 0:
		new_contexts.append(new_context)
		new_contexts_flags.append(new_context_flags)

	return new_contexts, new_contexts_flags
	#bag_of_transition_paragraphs = detect_paragraph_transitions(book_paragraphs)
	#print_bag_of_transition_paragraphs(book_paragraphs, bag_of_transition_paragraphs)














###############################################################################################################################
#########################   GLOBAL FUNCTIONS (LIBRARY FUNCTIONS)   ############################################################
###############################################################################################################################
###
###
###
###
###
def parse_text(path, write_diagrams=False):
	diagram_parse = False
	diagram_count = 0
	board = []
	diagram_string = ""
	book = ""

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
				if write_diagrams:
					FEN_notation = get_FEN_notation(board)
					diagram_string += ("\nFEN:" + FEN_notation)

					filename = "Diagram" + str(diagram_count) + ".txt"
					output_file = os.path.join(PARAM.diagram_path,filename)
					with open(output_file, "w") as file2write:
						file2write.write(diagram_string)
				diagram_string = ""
			#not a diagram
			else:		
				book += line
	return book
###
###
###
###
###
def parse_book(book, write2file = False, chapter_num=0):

	#split the book into paragraphs
	book_paragraphs = book.split("\n\n")[3:]#first three are chapter headlines

	#write the paragraphs to csv if specified
	if write2file:
		with open(os.path.join(args.data_path, "paragraphs_CH"+str(chapter_num)+".csv"), "w") as csvfile:
			count=1
			csvwriter = csv.writer(csvfile, delimiter='\t')
			csvwriter.writerow(["id","paragraph"])
			for paragraph in book_paragraphs:
				csvwriter.writerow([count, paragraph])
				count += 1	
	
	#divide the text into contexts using numbered move sequences
	contexts = []
	context =[]
	contexts_flags = []
	context_flags = []
	sequence_start = 0
	previous_sequence = 0
	for paragraph in book_paragraphs:
		diagrams, _, _, num_items = extract_special_tokens(paragraph, diagram=True, num_item=True)
		if num_items != None:
			sequence_start = int(re.search(r'^\d+', num_items[0][0].strip()).group())
			sequence_end = int(re.search(r'^\d+', num_items[-1][0].strip()).group())
			if sequence_start < previous_sequence:
				contexts.append(context)
				context = []
				contexts_flags.append(context_flags)
				context_flags = []
			context.append(paragraph)
			context_flags.append(1)
			previous_sequence = sequence_end
		else:
			context.append(paragraph)
			context_flags.append(0)
		if diagrams != None and context_flags[-1]==0:
			context_flags[-1]=-1
	if len(context) != 0:
		contexts.append(context)
		contexts_flags.append(context_flags)
	
	#improve the context separation by using diagram referrals
	contexts,_ = parse_book_enhanceWdiags(contexts, contexts_flags)

	#create paragraph ids
	paragraph_ids = []
	paragraph_count = 0
	for i in range(len(contexts)):
		temp_ids = []
		for j in range(len(contexts[i])):
			paragraph_count +=1
			temp_ids.append(paragraph_count)
		paragraph_ids.append(temp_ids)

	segmented_contexts = []
	segmented_paragraph_ids = []
	for i in range(len(contexts)):
		context, par_ids = segment_numbered_items(contexts[i], paragraph_ids[i])
		segmented_contexts.append(context)
		segmented_paragraph_ids.append(par_ids)

	#write contexts to csv file if specified
	if write2file:
		with open(os.path.join(args.data_path, "contexts_CH"+str(chapter_num)+".csv"), "w") as csvfile:
			csvwriter = csv.writer(csvfile, delimiter='\t')
			csvwriter.writerow(["context", "paragraph", "text"])
			for i in range(len(segmented_contexts)):
				for j in range(len(segmented_contexts[i])):
					csvwriter.writerow([i, segmented_paragraph_ids[i][j], segmented_contexts[i][j]])

	return segmented_contexts, segmented_paragraph_ids
###
###
###
###
###
def context_parser(context):

#TO DO: Do this sentence tokenization and classification for each context here
	for paragraph in context:
		new_paragraph = paragraph.replace('\n',' ')
		diagrams, moves, text_moves, num_items = extract_special_tokens(new_paragraph, num_item=True)
		if num_items == None:
			#paragraph = paragraph.replace('\n',' ')
			#sentences = sent_tokenize(paragraph)
			#for sentence in sentences:
				#diagrams, moves, text_moves, num_items = extract_special_tokens(sentence, diagram=True, move=True, text_move=True)
				#print(sentence)
			pass
		else:
			print("move sequence found")
			print("-------------------\n"+paragraph+"\n-------------------")
			for item in num_items:
				print(item[0].strip() + "\n")
			print("-------------------------------------------------------")			
			par = segment_numbered_items(new_paragraph, print_all=True)
			sentences = sent_tokenize(par[-1])
			for sentence in sentences:
				#diagrams, moves, text_moves, num_items = extract_special_tokens(sentence, diagram=True, move=True, text_move=True)
				print(sentence)
	exit()

