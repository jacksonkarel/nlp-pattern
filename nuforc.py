import os

from segmenting.nuforc import segment_nuforc
from clustering.fast_cluster import fast_cluster

def cluster_nuforc():
    segment_nuforc()
    os.makedirs("clusters", exist_ok=True)
    fast_cluster("sentences/nuforc.txt", "clusters/nuforc.json")