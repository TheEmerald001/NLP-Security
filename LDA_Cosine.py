# Gensim
import copy
import gensim
import pandas as pd
import gensim.corpora as corpora

'''Variables that need user input.'''
models_corpus = corpora.MmCorpus('SRS Topic Models/Corpora/Supermarket_srs_corpus')
models_dictionary = corpora.Dictionary.load('SRS Topic Models/Dictionaries/Supermarket_srs_dictionary')
csv_filename = "Supermarket_results.csv"


def caluclate_cosine_similarity_lda():
    lda_result_local = {}
    for w in range(0, lda_srs_num_topics):
        for x in range(0, 544):
            lda_result_local.update({x: gensim.matutils.cossim(lda_vector[w], capec_vector_list_lda[x])})
        lda_cosine_result_list.append(copy.deepcopy(lda_result_local))
        lda_result_local.clear()


def create_CAPEC_vectors_lda():
    capec_vector = []
    capec_number = 1
    vector_list = []
    for x in range(1, 545):
        capec_lda = gensim.models.LdaModel.load("CAPEC/LDA/capec_lda_" + str(capec_number))
        for topic_number in range(0, 4):
            capec_vector.extend(capec_lda.get_topic_terms(topicid=topic_number, topn=10))
        vector_list.append(capec_vector[:])
        capec_vector.clear()
        capec_number += 1
    return vector_list


def get_CAPEC_IDs(capec_list):
    CAPEC_IDs = pd.read_csv("CAPEC/Comprehensive CAPEC Dictionary.csv", usecols=["ID"])
    list_with_topics_and_capec_ids = []
    for pattern in capec_list:
        topic_list = []
        for value in pattern:
            index = value[0] - 1
            new_tuple = tuple((CAPEC_IDs.iloc[index].values[0], value[1]))
            topic_list.append(new_tuple)
        list_with_topics_and_capec_ids.append(copy.deepcopy(topic_list))
    return list_with_topics_and_capec_ids


capec_vector_list = []
lda_vector = []
similarity_results = {}

capec_num = 1
srs_lda = gensim.models.LdaModel.load("SRS Topic Models/LDA TOPIC MODELS/Supermarket_lda")

lda_srs_num_topics = len(srs_lda.get_topics())

# Load in the LDA model from the SRS document into
for topic_num in range(0, lda_srs_num_topics):
    lda_vector.append(srs_lda.get_topic_terms(topicid=topic_num, topn=30))

# Load in the capec lda models into vectors
capec_vector_list_lda = create_CAPEC_vectors_lda()

lda_cosine_result_list = []
caluclate_cosine_similarity_lda()
# Sort the values of the list from highest similarity value to lowest similarity value.
lda_sorted_lists = []

for y in range(0, lda_srs_num_topics):
    lda_sorted_lists.append(sorted(lda_cosine_result_list[y].items(), key=lambda x: x[1], reverse=True))

# Returns a new list with the CAPEC IDS of the Attack Pattern for all topics
lda_result = get_CAPEC_IDs(lda_sorted_lists)

# Convert the list of lists into a Pandas Dataframe. For easier manipulation.
pandas_frame_lda = pd.DataFrame(lda_result)
# Transpose the Data Frame
pandas_frame_lda = pandas_frame_lda.transpose()
top_LDA_patterns = {}
for topic in range(0, lda_srs_num_topics):
    items_added = 0
    for values in lda_result[topic]:
        if items_added == 20:
            break
        if not (values[0] in top_LDA_patterns):
            top_LDA_patterns[values[0]] = values[1]
            items_added += 1
        else:
            top_LDA_patterns[values[0]] = max(values[1], top_LDA_patterns[values[0]])

lda_top_results = [(k, v) for k, v in top_LDA_patterns.items()]
lda_top_results = sorted(lda_top_results, key=lambda x: x[1], reverse=True)

# Rename the columns of the Pandas DataFrame
for x in range(0, lda_srs_num_topics):
    pandas_frame_lda.rename(columns={x: "Topic-" + str(x + 1)}, inplace=True)

# Save the results to a csv file.
pandas_frame_lda.to_csv("SIMILARITY RESULTS/" + "lda_" + csv_filename, encoding="utf-8", index=False)

print("LDA TOP 10 ATTACK Patterns")
for x in range(0, 10):
    print(lda_top_results[x])
