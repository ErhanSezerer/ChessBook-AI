from args import args
from chessbook_parser import parse_book, context_parser, parse_text
from bert import test_bert

from nltk.tokenize import sent_tokenize
import pandas as pd
from tqdm import tqdm
import os





	




def main():

	#parse the text and segment out the diagrams
	path = os.path.join(args.book_path, args.chapter_name)
	book = parse_text(path)

	#parse the book and find contexts
	contexts, _ = parse_book(book)
	with open("/media/darg1/Data/Projects/chess/ChessBook-AI/after.txt", "w") as fil:
		for i in range(len(contexts)):
			for j in range(len(contexts[i])):
				fil.write(contexts[i][j] + "\n")
			fil.write("\n---------------\nNEW CONTEXT\n---------------\n")

	#
	exit()
	context_parser(contexts[0])
	exit()

	predictions = []
	

	for paragraph in tqdm(paragraphs):
		paragraph = paragraph.replace('\n',' ')
		sentences = sent_tokenize(paragraph)
		for sentence in sentences:
			row = []
			pred = test_bert(sentence, args.model_path)
			row.append(sentence)
			row.append(pred[0])
			predictions.append(row)

	df_predictions = pd.DataFrame(predictions, columns=["sentence","label"])
	save_path = os.path.join(args.data_path, "sentence_predictions.csv")
	df_predictions.to_csv(save_path, sep='\t')


if __name__ == "__main__":
	main()
