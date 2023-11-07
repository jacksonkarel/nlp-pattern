import json

with open('clusters/nuforc.json') as json_file:
    clusters = json.load(json_file)

for clust in clusters:
    clusters[clust]["size"] = clusters[clust].pop("length")
    clusters[clust]["texts"] = clusters[clust].pop("sentences")

with open('clusters/nuforc2.json', 'w') as outfile:
    json.dump(clusters, outfile)