import numpy as np


def trough(position: int, length: int, b=4) -> float:
    """ This implements the custom author weight function.
        The fundamental assumption is that authors at the
        beginning and end of the author list contribute
        more to a publication than middle authors.

        :position:
            where the author is located in the authorship list
        :length:
            total number of authors in the authorship list
        :b:
            parameter for the slope of the 'trough' in the trough function

        :returns:
            author weight according to the trough function
    """

    def sigmoid(x: float) -> float:
        """ The sigmoid/logistic function. """
        return 1 / (1 + np.exp(-x))

    c = (length - 1) / length

    return 1 - c * (sigmoid(b * (position - 1)) - sigmoid(b * (position - length + 2)))


def convert_eu_to_float(x) -> float:
    """ Convert number of the form 0,xx to 0.xx

        args:
        -----
        :x:
            str or float

        :returns:
            decimal form of x

        :raises: ValueError: if x is not in the form x.xx, 'x.xx', or 'x,xx'
        :raises: AttributeError: if x is not str, int, or float

        Examples:
        ---------
        >>> convert_eu_to_float('7,89')
        7.89
        >>> convert_eu_to_float(4.5)
        4.5
        >>> convert_eu_to_float('9.99')
        9.99
        >>> convert_eu_to_float(4)
        4.0
    """

    if isinstance(x, float) or isinstance(x, int):
        return float(x)

    return float(x.replace(',', '.'))


def count_affils(affils: list) -> int:
    """ Accepts a list of affiliations and returns the length.
        Logic is included for where the list is empty.

        :affils:
            list of affiliations for a given author

        :returns:
            length of the list - 0 if the list if empty

        Examples:
        >>> count_affils([7, 67, 54])
        3
        >>> count_affils(np.nan)
        0
    """

    if isinstance(affils, float):
        return 0
    else:
        return len(affils)


def publication_metrics(profiles: dict) -> dict:
    """ Generate df to hold all publication metrics for each author

        args:
        -----
        :profiles:
            dict of {auid: AuthorRetrieval object}

        :returns:
            dict of the form
                 auid: [
                     indexed_name,
                     affiliation_current,
                     affiliation_history,
                     alias,
                     citation_count,
                     cited_by_count,
                     coauthor_count,
                     classificationgroup,
                     document_count,
                     h_index,
                     orcid,
                     publication_range,
                     subject_areas
                 ]
    """

    return {
        author: [
            profiles[author].indexed_name,
            profiles[author].affiliation_current,
            profiles[author].affiliation_history,
            profiles[author].alias,
            profiles[author].citation_count,
            profiles[author].cited_by_count,
            profiles[author].coauthor_count,
            profiles[author].classificationgroup,
            profiles[author].document_count,
            profiles[author].h_index,
            profiles[author].orcid,
            profiles[author].publication_range,
            profiles[author].subject_areas,
        ] for author in profiles
    }
