from gensim import corpora
from gensim.models import LdaModel, CoherenceModel, LsiModel
import pickle
import matplotlib.pyplot as plt

CORPUS_FILE_PATH = 'SRS Topic Models/Corpora/'
DICTIONARY_FILE_PATH = 'SRS Topic Models/Dictionaries/'
PROCESSED_TEXT_FILE_PATH = 'SRS Topic Models/Processed Text/'
file_name = 'Supermarket'
corpus_file_name = file_name + "_srs_corpus"
dictionary_file_name = file_name + "_srs_dictionary"
texts_file_name = file_name + "_text"

corpus = corpora.MmCorpus(CORPUS_FILE_PATH + corpus_file_name)
id2word = corpora.Dictionary.load(DICTIONARY_FILE_PATH + dictionary_file_name)
processed_text_file = open(PROCESSED_TEXT_FILE_PATH+texts_file_name,'rb')
processed_text = pickle.load(processed_text_file)

coherence_values = []
lsa_model_list = []
if __name__ == '__main__':
    start = 1
    step = 1
    limit = 40
    # Create LSA MODELS
    for x in range(start, limit, step):
        lsa_model = LsiModel(corpus=corpus, id2word=id2word, num_topics=x, chunksize=100)
        coherence_model_lsa = CoherenceModel(model=lsa_model, texts=processed_text, dictionary=id2word, coherence='c_v')
        lsa_model_list.append(lsa_model)
        coherence_values.append(coherence_model_lsa.get_coherence())
        print("Num Topics = "+str(len(lsa_model.get_topics()))+" Coherence Score = "+str(round(coherence_model_lsa.get_coherence(),4)))

    limit = 40
    start = 1
    step = 1
    x = range(start, limit, step)
    plt.plot(x, coherence_values)
    plt.xlabel("Number of topics")
    plt.ylabel("Coherence score")
    plt.title("LSA Topic Models")
    plt.show(block=True)
    topic_number = int(input("Enter the number of topics with the desired coherence score:"))
    print("You have selected to save the LSA model with "+str(topic_number)+" topics and coherence of: "+str(
        coherence_values[topic_number-1]))
    lsa_model_list[topic_number-1].save("SRS Topic Models/LSA TOPIC MODELS/"+file_name+"_lsa")