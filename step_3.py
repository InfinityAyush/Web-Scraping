import pandas as pd
import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re


df  = pd.read_csv('Output.csv')

folder_path= "MasterDictionary"
data_path = "stopwords_filtered"

file_path = os.path.join(folder_path, "negative-words.txt")
with open(file_path, "r") as file_object:
    NegWords = file_object.read()

file_path = os.path.join(folder_path, "positive-words.txt")
with open(file_path, "r") as file_object:
    PosWords = file_object.read()

# Get the list of all files in the folder
files = os.listdir(data_path)

df_id = df['URL_ID']
df['URL_ID'] = df['URL_ID'].astype(int)


for p in files:
    file_path = os.path.join(data_path, p)
    with open(file_path, "r",encoding='utf-8') as file_object:
        curr = file_object.read()

    # -------------- positive negative score
    positive = 0
    negative = 0

    word_tokens = word_tokenize(curr)

    for i in word_tokens:
        if i in PosWords:
            positive +=1
        if i in NegWords:
            negative +=1




    # ------------------ total words
    stop_words_nltk = set(stopwords.words('english'))
    Words = [word for word in word_tokens if word.lower() not in stop_words_nltk]
    


    # ---------------------- polarity 
    Polarity = (positive  - negative ) / ((positive  + negative ) + 0.000001)



    # ----------------- Subjectivity
    Subjectivity = (positive + negative)/ ((len(Words)) + 0.000001)
    

    # ------------------  total number of sentances
    sentances=0
    for i in word_tokens:
        if i ==".":
            sentances +=1


    # --------------------  Average sentance lenght
    if sentances ==0:
        AvgSenLen = len(Words)
    else:
        AvgSenLen = len(Words)/sentances

    


    # ------------------- Percentage of Complex words

    complexWord = 0
    # Function to count syllables in a word
    def count_syllables(word):
        vowels = "aeiouAEIOU"
        count = 0
        prev_char = ''

        for char in word:
            if char in vowels and prev_char not in vowels:
                count += 1
            prev_char = char

        if word.endswith(('es', 'ed')):
            count -= 1  # Adjust for exceptions

        return max(1, count)  # At least one syllable for any word

    syllables = []
    # Count the number of complex words
    complex_word_count = 0
    for word in Words:
        syllable_count = count_syllables(word)
        syllables.append(syllable_count)
        if syllable_count > 2:
            complex_word_count += 1

    # Calculate the percentage of complex words
    total_words = len(Words)
    percentage_complex_words = (complex_word_count / total_words) * 100

    syllableWords = sum(syllables) / len(syllables)
    


    # ---------------------- fog index

    fogIndex = 0.4 * (AvgSenLen + percentage_complex_words)
    

    # ------------------------ avg number of words per sentance
    # print("AVG NUMBER OF WORDS PER SENTENCE : ",AvgSenLen)


    # ------------------------ PERSONAL PRONOUNS

    # Define the regex pattern for personal pronouns
    pronoun_pattern = re.compile(r'\b(?:I|we|my|our|ours|us)\b', flags=re.IGNORECASE)

    # Find all matches in the text
    matches = pronoun_pattern.findall(curr)

    # Count the occurrences of personal pronouns
    pronoun_count = len(matches)



    # ---------------------- AVG WORD LENGTH
    lenths = []
    for i in Words:
        lenths.append(len(i))
    AvgWordLen = sum(lenths)/len(lenths)
    


    # ---------------------------------------  Setting dataset -------------------------------------------------

    
    # Using boolean indexing
    row = df[df["URL_ID"] == int(p[:-4])].index[0]

    df.loc[row, "POSITIVE SCORE"] = round( positive, 2)
    df.loc[row, "NEGATIVE SCORE"] = round(negative,2)
    df.loc[row, "POLARITY SCORE"] = round(Polarity,2)
    df.loc[row, "SUBJECTIVITY SCORE"] = round(Subjectivity,2)
    df.loc[row, "AVG SENTENCE LENGTH"] = round(AvgSenLen,2)
    df.loc[row, "PERCENTAGE OF COMPLEX WORDS"] = round(percentage_complex_words,2)
    df.loc[row, "FOG INDEX"] = round(fogIndex,2)
    df.loc[row, "AVG NUMBER OF WORDS PER SENTENCE"] = round(AvgSenLen,2)
    df.loc[row, "COMPLEX WORD COUNT"] = round(complex_word_count,2)
    df.loc[row, "WORD COUNT"] = round(len(Words),2)
    df.loc[row, "PERSONAL PRONOUNS"] = round(pronoun_count,2)
    df.loc[row, "AVG WORD LENGTH"] =round( AvgWordLen,2)
    df.loc[row, "SYLLABLE PER WORD"] = round(syllableWords,2)

    print(p,"done.")


df['URL_ID'] = df_id

print(df.head())
df.to_csv("Output.csv")


