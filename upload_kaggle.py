from kaggle.api.kaggle_api_extended import KaggleApi

from word_order import word_order

pat_sw = ["it", "in", "around", "this", "after", "/"]
word_order("tokenizations/tokenized.p", "patterns/nuforc/patterns.csv", pat_sw)
kaggle = KaggleApi()
kaggle.authenticate()
kaggle.dataset_create_version("patterns/nuforc", "Generated from nlp-pattern script", convert_to_csv=False, delete_old_versions=True)