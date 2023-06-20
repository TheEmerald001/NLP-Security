# Topic Modelling Tool
## Prerequisites (Libraries Required)
* Included in this reposistory is a requirements.txt file that contains a list of all python packages that are used for this project. 
### STEPS TO RUN Topic Modeling Tool
* Note 1 :Once finished running on a given SRS document, I recommend saving the SRS topic models, the corpuses, dictionaries, and processed text and similarity results to a separate folder. Before creating another run on another SRS document. This is so only the pertinent information for the given SRS document is present. This should not affect performance if one does not save their export their results to a different folder ,but I still recommend doing so.
* Note 2 :This uploaded version on github is ready to run for Demonstration purposes. It utilizes an SRS document uploaded to the SRS/SRS documents folder. So if wanted you can follow along and do a test run without needing to replace any variables.  
### 1.SRS DOCUMENT TEXT PREPROCESSING STEPS
* Step 1 is conducted in order to clean up the text data that will be used in the topic models. Particularly this step will help in generating the corpus,dictionary, and cleaned text that will be used by the topic model. 
* Have the desired SRS document (that will be topic modelled) inserted into the folder SRS/SRS Documents.</br>
* Once the srs document has been placed into the folder, modify the SRS Text Preprocessing python file.
* Modify the following variables: <br />
    - file_name - this variable modifies  a couple of variables within the python file. This will affect how the corpus,dictionary, and processed text are saved.
    - filepath - this variable needs to be modified to reflect the path of the SRS document you want to process. (You can utilize the relative path for this.)
* Once the above variables have been modified. Run the SRS Text Preprocessing python file.
* **Once completed, the corpus, dictionary, and cleaned text are saved in the SRS Topic Models folder under the following: Corpora,Dictionaries and Processed Text.** 

### 2. Running LDA Topic Model
* Open the LDA_SRS python file. 
* Modify the variable file_name with the information of the file_name used in Step 1.
* Once the above variable has been modified, run the file. (This step may take some time as there are 40 topic models being generated with a different number of topics.)
* Printed to the console are the coherence scores and number of topics for the topic model. 
* Once all 40 models are generated and the results are printed to the console a popup window will appear.
* This popup window will display a graph that graphs the coherence scores to the number of topics.
* This graph will show where the coherence values reaches a peak. Observe and write down at what point the graph its second peak. (Check for where the graph increases reaches a maximum then decreases and increases again that max point before the second decrease is the number of topics that you will want to remember.)
* **Before continuing onto the next step be sure to have written down or remembered the number of topics that had the highest similarity. (If not written down or remembered you will have to rerun the LDA_SRS Python File.)**
* Once the point has been noted quit the pyplot figure to continue the execution of code. On the terminal or IDE command line you will be asked to enter the number of topics that has the desired coherence score. (Use the number recommend in the previous step.)
* This will save the LDA model and exit execution.
**Once completed, LDA models are saved in the SRS Topic Models folder under LDA Topic Models** 
### 3. Running LSA Topic Model
* Open the LSA_SRS python file. 
* Modify the variable file_name with the information of the file_name used in Step 1.
* Once the above variable has been modified, run the file. (This step may take some time as there are 40 topic models being generated with a different number of topics.)
* Printed to the console are the coherence scores and number of topics for the topic model. 
* Once all 40 models are generated and the results are printed to the console a popup window will appear.
* This popup window will display a graph that graphs the coherence scores to the number of topics.
* This graph will show where the coherence values reaches a peak. Observe and write down at what point the graph its second peak. (Check for where the graph increases reaches a maximum then decreases and increases again that max point before the second decrease is the number of topics that you will want to remember.)
* **Before continuing onto the next step be sure to have written down or remembered the number of topics that had the highest similarity. (If not written down or remembered you will have to rerun the LSA_SRS Python File.)**
* Once the point has been noted quit the pyplot figure to continue the execution of code. On the terminal or IDE command line you will be asked to enter the number of topics that has the desired coherence score. (Use the number recommend in the previous step.)
* This will save the LSA model and exit execution.
**Once completed, LSA models are saved in the SRS Topic Models folder under LSA Topic Models** 
### 4. Running Similarity Measures
* For LDA Results run the LDA_Cosine File. 
* For LSA Results run the LSA_Cosine File. 
* The LDA_Cosine/LSA_Cosine file will require the following to be given
  * models_corpus - (This is the path for the corpus of our SRS document)
  * models_dictionary - (This is the dictionary of our SRS document)
  * csv_filename - (This variable affects what name is given to our csv output file.)
* Once these have been specified, proceed to run the LDA_Cosine/LSA_Cosine.
* This will print out to the console the top 10 Recommended Attack Patterns in the form of (CAPEC ID, Cosine Similarity) for the given Topic Model. For full list of results, navigate to the SIMILARITY RESULTS folder and the results can be found there.
