#  for looping through all files
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import os

folder_path = "Data/"
output_folder = "filtered_files"


# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Get the list of all files in the folder
files = os.listdir(folder_path)

for i in files:
    # ---------------- took text data from file 
    file_path = os.path.join(folder_path, i)
    with open(file_path, "r", encoding='utf-8') as file_object:
        texts = file_object.read()

    # --------------- Cleaning using Stop Words Lists

    # converts the words in word_tokens
    word_tokens = word_tokenize(texts)

    # List of filters
    filters = [
        'StopWords_Auditor.txt',
        'StopWords_Currencies.txt',
        'StopWords_DatesandNumbers.txt',
        'StopWords_Generic.txt',
        'StopWords_GenericLong.txt',
        'StopWords_Geographic.txt',
        'StopWords_Names.txt'
    ]

    for filter_file in filters:
        filter_path = os.path.join('StopWords', filter_file)
        with open(filter_path, "r", encoding='utf-8', errors='ignore') as stopword_file:
            stopword_text = stopword_file.read()

        word_tokens = [w for w in word_tokens if w not in stopword_text]

    output_file_path = os.path.join(output_folder, i)
    with open(output_file_path, 'a', encoding='utf-8') as output_file:
        output_file.write(" ".join(word_tokens))


