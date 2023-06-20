# Gensim
import copy
import gensim
import pandas as pd
import gensim.corpora as corpora

'''Variables that need user input'''
models_corpus = corpora.MmCorpus('SRS Topic Models/Corpora/Supermarket_srs_corpus')
models_dictionary = corpora.Dictionary.load('SRS Topic Models/Dictionaries/Supermarket_srs_dictionary')
csv_filename = "Supermarket_results.csv"

def caluclate_cosine_similarity_lsa():
    lsa_result = {}
    for y in range(0, lsa_srs_num_topics):
        for z in range(0, 544):
            lsa_result.update({z: gensim.matutils.cossim(lsa_vector[y], capec_vector_list_lsa[z])})
        lsa_cosine_result_list.append(copy.deepcopy(lsa_result))
        lsa_result.clear()

# returns a list
def lsa_get_topic_terms(topicid, topwords,lsa_model):
    lsa_show_topics = lsa_model.show_topic(topicno=topicid, topn=topwords)
    lsa_topic_terms = []
    # ISSUES WITH LOOP
    for pair in lsa_show_topics:
        for wordID in models_dictionary:
            if models_dictionary[wordID] in pair[0] and models_dictionary[wordID] == pair[0]:
                lsa_topic_terms.append((wordID, abs(pair[1])))
    return copy.deepcopy(lsa_topic_terms)


def create_CAPEC_vectors_lsa():
    capec_vector = []
    capec_num = 1
    vector_list = []
    for x in range(1, 545):
        capec_lsa = gensim.models.LsiModel.load("CAPEC/LSA/capec_lsa_" + str(capec_num))
        for topic_number in range(0, len(capec_lsa.get_topics())):
            capec_vector.extend(lsa_get_topic_terms(topicid=topic_number,topwords=10,lsa_model=capec_lsa))
        vector_list.append(capec_vector[:])
        capec_vector.clear()
        capec_num += 1
    return vector_list


def get_CAPEC_IDs(capec_list):
    CAPEC_IDs = pd.read_csv("CAPEC/Comprehensive CAPEC Dictionary.csv", usecols=["ID"])
    list_with_topics_and_capec_ids = []
    for topic in capec_list:
        topic_list = []
        for value in topic:
            index = value[0] - 1
            new_tuple = tuple((CAPEC_IDs.iloc[index].values[0], value[1]))
            topic_list.append(new_tuple)
        list_with_topics_and_capec_ids.append(copy.deepcopy(topic_list))
    return list_with_topics_and_capec_ids




capec_vector_list = []
lda_vector = []
lsa_vector = []
lsa_terms = []
similarity_results = {}



capec_num = 1


srs_lsa = gensim.models.LsiModel.load("SRS Topic Models/LSA TOPIC MODELS/Supermarket_lsa")


lsa_srs_num_topics = len(srs_lsa.get_topics())

# Load in the LDA model from the SRS document into
for topic_num in range(0, lsa_srs_num_topics):
    lsa_vector.append(lsa_get_topic_terms(topicid=topic_num, topwords=30, lsa_model=srs_lsa))


capec_vector_list_lsa = create_CAPEC_vectors_lsa()


lsa_cosine_result_list = []

caluclate_cosine_similarity_lsa()

# Sort the values of the list from highest similarity value to lowest similarity value.

lsa_sorted_lists = []

for y in range(0, lsa_srs_num_topics):
    lsa_sorted_lists.append(sorted(lsa_cosine_result_list[y].items(), key=lambda x: x[1], reverse=True))


lsa_result = get_CAPEC_IDs(lsa_sorted_lists)
# Convert the list of lists into a Pandas Dataframe. For easier manipulation.

pandas_frame_lsa = pd.DataFrame(lsa_result)
# Transpose the Data Frame

pandas_frame_lsa = pandas_frame_lsa.transpose()


top_LSA_patterns = {}

for topic in range(0, lsa_srs_num_topics):
    items_added = 0
    for values in lsa_result[topic]:
        if items_added == 20:
            break
        if not (values[0] in top_LSA_patterns):
            top_LSA_patterns[values[0]] = values[1]
            items_added+= 1
        else:
            top_LSA_patterns[values[0]] = max(values[1], top_LSA_patterns[values[0]])

lsa_top_results = [(k,v) for k, v in top_LSA_patterns.items()]
lsa_top_results = sorted(lsa_top_results, key=lambda x: x[1], reverse=True)


for x in range(0, lsa_srs_num_topics):
    pandas_frame_lsa.rename(columns={x: "Topic-" + str(x + 1)}, inplace=True)


pandas_frame_lsa.to_csv("SIMILARITY RESULTS/" + "lsa_" + csv_filename, encoding="utf-8", index=False)


print("LSA TOP TEN RESULTS")
for x in range(0, 10):
    print(lsa_top_results[x])