from kaggle.api.kaggle_api_extended import KaggleApi

from word_order import word_order

word_order()
kaggle = KaggleApi()
kaggle.authenticate()
kaggle.dataset_create_version("patterns", "Generated from nlp-pattern script", convert_to_csv=False, delete_old_versions=True)