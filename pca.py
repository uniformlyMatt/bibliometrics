import numpy as np
import pandas as pd
import sklearn
from datetime import datetime
from sklearn.decomposition import PCA

if __name__ == '__main__':
    n_comp = 1

    # load the data
    df = pd.read_excel('../Datasets/PCA_inputs_jan18.xlsx')

    # get the current date
    today = datetime.today().strftime("%d-%h-%Y")

    # create pca model
    pca = PCA(n_components=n_comp)

    # log transform the right-skewed columns
    df['mean_citations_per_year'] = df['mean_citations_per_year'].apply(lambda x: np.log(1 + x))
    df['citation_count'] = df['citation_count'].apply(lambda x: np.log(1 + x))
    df['cited_by_count'] = df['cited_by_count'].apply(lambda x: np.log(1 + x))
    df['document_count'] = df['cited_by_count'].apply(lambda x: np.log(1 + x))
    df['Article_sum'] = df['Article_sum'].apply(lambda x: np.log(1 + x))
    df['journal_h_index_mean'] = df['journal_h_index_mean'].apply(lambda x: np.log(1 + x))
    df['growth_rate'] = df['growth_rate'].apply(lambda x: np.log(1 + x))

    # won't be using these columns
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

    # define the columns to use for the PCA - fit the PCA
    df_pca = df.drop(['Auid', 'affil', 'publication_duration', 'coauthor_count'], axis=1)
    pca.fit(df_pca)

    print(df_pca.columns)

    explained_var = pca.explained_variance_ratio_
    eigenvectors = pca.components_
    loadings = pca.components_.T * np.sqrt(pca.explained_variance_)

    pd.DataFrame(
        {
            'Variable': df_pca.columns,
            'PC1': loadings.flatten(),
            'log_transformed': [1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0]
        }
    ).to_csv('../Datasets/pca_loadings_{}.csv'.format(today), index=False)

    scores = pca.fit_transform(df.drop(['Auid', 'affil', 'publication_duration', 'coauthor_count'], axis=1))
    df['PC1'] = scores

    print(pca.explained_variance_ratio_)

    df.to_csv('../Datasets/authors_with_pca_scores_{}.csv'.format(today), index=False)
