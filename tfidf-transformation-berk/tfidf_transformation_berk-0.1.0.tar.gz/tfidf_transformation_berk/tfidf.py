# import required module
from .tfidf_transformation_berk import TfidfTransformer

# assign documents
doc0 = 'A Scandal in Bohemia'
doc1 = 'The Red-headed League'
doc2 = 'A Case of Identity'
doc3 = 'The Boscombe Valley Mystery'
doc4 = 'The Five Orange Pips'
doc5 = 'The Man with the Twisted Lip'
doc6 = 'The Adventure of the Blue Carbuncle'
doc7 = 'The Adventure of the Speckled Band'
doc8 = "The Adventure of the Noble Bachelor"

# merge documents
documents = [doc0,doc1,doc2,doc3,doc4,doc5,doc6,doc7,doc8]

# create object
tfidf = TfidfTransformer()

# fit documents 
tfidf.fit(documents)

# transform documents 
transform = tfidf.transform(documents)
# display tf-idf scores 
print(transform)

# get tf-idf values
# this steps generates word counts for the words in documents
fit_transform = tfidf.fit_transform(documents)
# display tf-idf values
print(fit_transform)

# We have 9 rows (9 docs) and 27 columns (27 unique words, minus single character words)
fit_transform.shape

# get feature names
feature_names = tfidf.get_feature_names()[0:5]
# display feature names
print(feature_names)