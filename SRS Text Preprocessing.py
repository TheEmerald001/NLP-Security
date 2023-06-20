"""FILE FOR TEXT PREPROCESSING SRS DOCUMENTS"""
# PyMuPDF python Library
import pickle
import re
import fitz
import string
import spacy
import gensim
from gensim import corpora
from gensim.utils import simple_preprocess
from nltk.corpus import stopwords

stopWords = stopwords.words('english')
stopWords.extend(["from", "subject", "re", "edu", "use"])
nlp = spacy.load("en_core_web_sm", disable=["parser,ner"])

# FILE PATHS
CORPUS_FILE_PATH = 'SRS Topic Models/Corpora/'
DICTIONARY_FILE_PATH = 'SRS Topic Models/Dictionaries/'
PROCESSED_TEXT_FILE_PATH = 'SRS Topic Models/Processed Text/'
filepath = 'SRS/SRS Documents/Supermarket Software Requirement Specification (SRS).pdf'

# SAVED RESULTS FILE NAMES
file_name = 'Supermarket'
corpus_file_name = file_name + "_srs_corpus"
dictionary_file_name = file_name + "_srs_dictionary"
texts_file_name = file_name + "_text"

# PAGES FOR PROCESSING TEXT
start_page = 4
end_page = 13
processed_text = []


def removepunctuation(supplied_text):
    translator = str.maketrans('', '', string.punctuation)
    return supplied_text.translate(translator)


def removewhitespaces(supplied_text):
    return " ".join(supplied_text.split())


def sent_to_words(sentences):
    count = 0
    for sentence in sentences:
        count += 1
        yield gensim.utils.simple_preprocess(str(sentence), deacc=True)


def remove_stopwords(supplied_text):
    return [[word for word in simple_preprocess(str(doc)) if word not in stopWords] for doc in supplied_text]


def lemmatization(supplied_text, allowed_pos=["NOUN", "ADJ", "VERB", "ADV"]):
    text_out = list()
    for sent in supplied_text:
        doc = nlp(" ".join(sent))
        text_out.append([token.lemma_ for token in doc if token.pos_ in allowed_pos])
    return text_out


pdf = fitz.open(filepath)
for x in range(start_page, end_page):
    page = pdf.load_page(x)
    text = page.get_text("text")

    # Covert Text to lower case
    text = text.lower()
    # REMOVE NUMBERS
    text = re.sub(r'\d+', '', text)
    # Remove Punctuation
    text = removepunctuation(text)
    # Remove Whitespaces
    text = removewhitespaces(text)
    text = list(text.split(" "))
    text = list(filter(None, text))
    processed_text.append(text)

data_words = list(sent_to_words(processed_text))
# REMOVE DEFAULT STOPWORDS
data_words_no_stops = remove_stopwords(data_words)

bigram = gensim.models.Phrases(data_words_no_stops, min_count=5, threshold=100)
trigram = gensim.models.Phrases(bigram[data_words_no_stops], min_count=5, threshold=100)

bigram_model = gensim.models.phrases.Phraser(bigram)
trigram_model = gensim.models.phrases.Phraser(trigram)

data_words_bigrams = [bigram_model[doc] for doc in data_words_no_stops]
data_words_trigrams = [x for x in data_words_bigrams if x != []]

#Lemmatization
lemma = lemmatization(data_words_bigrams, allowed_pos=['NOUN', 'ADJ', 'VERB', 'ADV'])

id2word = corpora.Dictionary(lemma)

corpus = [id2word.doc2bow(word) for word in lemma]

# Save corpus and dictionary to disk
corpora.MmCorpus.serialize(CORPUS_FILE_PATH + corpus_file_name, corpus)
id2word.save(DICTIONARY_FILE_PATH + dictionary_file_name)
file = open(PROCESSED_TEXT_FILE_PATH + texts_file_name, 'wb')

# SAVES TEXT AS BYTES IN A FILE TO BE LOADED AGAIN WHEN NEEDED
pickle.dump(lemma, file)
