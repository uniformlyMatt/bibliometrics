import csv
from typing import Tuple

import numpy as np
import pandas as pd
from pybliometrics.scopus import AuthorRetrieval

pd.options.mode.chained_assignment = None  # default='warn'


def get_auids(path: str, site: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """ Accepts a path pointing to an Excel file and creates two pandas DataFrames

        args:
        -----
        :filepath:
            string that points to a Microsoft Excel file
        :new_site:
            name of the site for which you will retrieve author profiles
    """

    chw = pd.read_excel(path)
    chw = chw[chw['Auid'] > 0]

    new_site = chw[chw[site] > 0]

    return chw, new_site


def get_profiles(col: pd.Series) -> dict:
    """ Accepts a column of a pandas DataFrame (as a Series) and uses pybliometrics to
        retrieve the corresponding author profiles.
    """

    profiles: dict = {auid: AuthorRetrieval(auid) for auid in col}
    print('{} profiles retrieved'.format(len(profiles.values())))

    return profiles


def get_publications(profs: dict, destination: str):
    """ Accepts a dictionary of AuthorRetrieval objects and retrieves the
        associated publication records from Scopus.
        :rtype: object
    """

    docs = [author.get_documents() for author in profs.values()]
    total_docs = sum([len(sublist) for sublist in docs])

    print('\nFor {} authors, we have {} documents\n'.format(len(docs), total_docs))

    with open(destination, 'a+') as csvfile:
        writer = csv.writer(
            csvfile,
            delimiter=','
        )

        # loop over authors and their associated documents
        for author, doc_list in zip(profs, docs):
            # loop over each doc in a list of documents
            for doc in doc_list:
                writer.writerow([author] + list(doc[:]))

    return None


def merge_profiles(profile_dict: dict, profile_headings: list, existing_profile_path: str) -> pd.DataFrame:
    """ Accepts dict of AuthorRetrieval objects, a list of attributes, and
        the location of the existing author profiles, and combines the new
        author profiles with the existing.
    """
    # convert author profiles into dictionaries
    pros = {
        auid: {key: profile_dict[auid].__getattribute__(key) for key in profile_headings} for auid in profile_dict
    }

    # convert to df
    df_profiles = pd.DataFrame(pros).T
    df_profiles['Auid'] = df_profiles.index

    # load existing author profiles
    if existing_profile_path is None:
        existing_profile_path = '../Datasets/chw_author_profiles.xlsx'

    chw_profiles = pd.read_excel(existing_profile_path)

    # combine the new profiles with the existing profiles
    merged_profiles = pd.concat([df_profiles, chw_profiles])

    # reset the index
    merged_profiles.index = np.arange(len(merged_profiles))

    return merged_profiles


def main(
        path_to_ids: str,
        new_site_name: str,
        publication_destination: str,
        existing_profiles: str,
        profile_destination: str
):
    """ Accepts filepath pointing to newly disambiguated list of author ids,
        creates a DataFrame for the new author profiles, and merges these
        profiles with the existing author profiles.
    """

    # load the author headings to be used for merging with existing author profiles
    with open('author_headings.txt', 'r') as heading_file:
        reader = csv.reader(heading_file)
        headings = [item for sublist in list(reader) for item in sublist]

    df_chw, df_new_site = get_auids(path_to_ids, site=new_site_name)
    profiles = get_profiles(df_new_site['Auid'])

    # download and save all documents associated with new authors
    get_publications(profiles, destination=publication_destination)

    chw_profiles = merge_profiles(profiles, profile_headings=headings, existing_profile_path=existing_profiles)

    # persist merged profiles
    chw_profiles.to_excel(profile_destination, index=False)

    return 0


if __name__ == '__main__':
    ids_path = '../Datasets/chw_ids.xlsx'
    newsite = 'MCMASTER'
    pub_destination = '../Datasets/chw_publications.csv'
    profiles_path = '../Datasets/chw_author_profiles.xlsx'
    main(ids_path, newsite, pub_destination, profiles_path, profiles_path)
