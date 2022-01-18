import numpy as np
import pandas as pd
import sklearn
from sklearn.decomposition import PCA

if __name__ == '__main__':
    n_comp = 1
    df = pd.read_excel('../Datasets/PCA_inputs_jan18.xlsx')
    pca = PCA(n_components=n_comp)

    df.drop(
        [
            'SJR_median',
            'journal_h_index_median',
            'author_count_median',
            'median_citations_per_doc',
            'chw_author_position_median',
            'author_weight_median',
            'median_citations_per_doc',
            'chw_author_position_median',
            'author_weight_median'
        ],
        axis=1,
        inplace=True
    )

    pca.fit(df.drop(['Auid', 'affil'], axis=1))

    explained_var = pca.explained_variance_ratio_
    eigenvectors = pca.components_

    scores = pca.fit_transform(df.drop(['Auid', 'affil'], axis=1))
    df['PC1'] = scores

    print(df)
