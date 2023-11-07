from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

def word_similarity(word_a, word_b):

    #Compute embedding for both lists
    embeddings1 = model.encode(word_a, convert_to_tensor=True)
    embeddings2 = model.encode(word_b, convert_to_tensor=True)

    #Compute cosine-similarits
    cosine_scores = util.cos_sim(embeddings1, embeddings2)

    print(cosine_scores[0][0])