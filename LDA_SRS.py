from gensim import corpora
from gensim.models import LdaModel, CoherenceModel
import pickle
import matplotlib.pyplot as plt

# FILE PATHS
CORPUS_FILE_PATH = 'SRS Topic Models/Corpora/'
DICTIONARY_FILE_PATH = 'SRS Topic Models/Dictionaries/'
PROCESSED_TEXT_FILE_PATH = 'SRS Topic Models/Processed Text/'

# SAVED RESULTS FILE NAMES
file_name = 'Supermarket'
corpus_file_name = file_name + "_srs_corpus"
dictionary_file_name = file_name + "_srs_dictionary"
texts_file_name = file_name + "_text"

corpus = corpora.MmCorpus(CORPUS_FILE_PATH + corpus_file_name)
id2word = corpora.Dictionary.load(DICTIONARY_FILE_PATH + dictionary_file_name)
processed_text_file = open(PROCESSED_TEXT_FILE_PATH+texts_file_name,'rb')
processed_text = pickle.load(processed_text_file)

start = 1
step = 1
limit = 40

coherence_values = []
lda_model_list = []
if __name__ == '__main__':
    limit = 40
    start = 1
    step = 1
    # Create LDA MODELS
    for x in range(start, limit, step):
        lda_model = LdaModel(corpus=corpus, id2word=id2word, num_topics=x, random_state=100,
                         update_every=1, chunksize=100, passes=10, alpha='auto', per_word_topics=True)
        coherence_model_lda = CoherenceModel(model=lda_model, texts=processed_text, dictionary=id2word, coherence='c_v')
        lda_model_list.append(lda_model)
        coherence_values.append(coherence_model_lda.get_coherence())
        print("Num Topics = "+str(x)+" Coherence Score = "+str(round(coherence_model_lda.get_coherence(), 4)))

    x = range(start, limit, step)
    plt.plot(x, coherence_values)
    plt.xlabel("Number of topics")
    plt.ylabel("Coherence score")
    plt.title("LDA Topic Models")
    plt.show(block=True)
    topic_number = int(input("Enter the number of topics with the desired coherence score:"))
    print("You have selected to save the LDA model with "+str(topic_number)+" topics and coherence of: "+str(
        coherence_values[topic_number-1]))
    lda_model_list[topic_number-1].save("SRS Topic Models/LDA TOPIC MODELS/"+file_name+"_lda")
    print("LDA TOPIC TERMS")

