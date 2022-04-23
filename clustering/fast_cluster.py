import time

from sentence_transformers import SentenceTransformer, util

from helpers import txt_to_list

def fast_cluster(corpus_fn):
    """
    Modified from https://github.com/UKPLab/sentence-transformers/blob/master/examples/applications/clustering/fast_clustering.py
    You can freely configure the threshold what is considered as similar. A high threshold will
    only find extremely similar sentences, a lower threshold will find more sentence that are less similar.
    A second parameter is 'min_community_size': Only communities with at least a certain number of sentences will be returned.
    The method for finding the communities is extremely fast, for clustering 50k sentences it requires only 5 seconds (plus embedding comuptation).
    """
    # Model for computing sentence embeddings.
    model = SentenceTransformer('all-MiniLM-L6-v2')

    corpus_sentences = txt_to_list(corpus_fn)
    print("Encode the corpus. This might take a while")
    corpus_embeddings = model.encode(corpus_sentences, batch_size=64, show_progress_bar=True, convert_to_tensor=True)


    print("Start clustering")
    start_time = time.time()

    #Two parameters to tune:
    #min_cluster_size: Only consider cluster that have at least 25 elements
    #threshold: Consider sentence pairs with a cosine-similarity larger than threshold as similar
    clusters = util.community_detection(corpus_embeddings, min_community_size=25, threshold=0.75)

    print("Clustering done after {:.2f} sec".format(time.time() - start_time))

    #Print for all clusters the top 3 and bottom 3 elements
    for i, cluster in enumerate(clusters):
        print("\nCluster {}, #{} Elements ".format(i+1, len(cluster)))
        for sentence_id in cluster[0:3]:
            print("\t", corpus_sentences[sentence_id])
        print("\t", "...")
        for sentence_id in cluster[-3:]:
            print("\t", corpus_sentences[sentence_id])
