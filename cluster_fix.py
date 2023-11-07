import json

with open('clusters/nuforc.json') as json_file:
    clusters = json.load(json_file)

fixed_clusters = {}
for clust in clusters:
    fixed_clusters[clust] = {}
    fixed_clusters[clust]["sentences"] = {}
    fixed_clusters[clust]["length"] = len(clusters[clust])
    for item in clusters[clust]:
        clean_item = item.lower().strip(".")
        if clean_item in fixed_clusters[clust]["sentences"]:
            fixed_clusters[clust]["sentences"][clean_item] += 1
        else:
            fixed_clusters[clust]["sentences"][clean_item] = 1

with open('clusters/nuforc2.json', 'w') as outfile:
    json.dump(fixed_clusters, outfile)
        
