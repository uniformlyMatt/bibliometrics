import requests
import json

logfile = None


# 17 June 2021 - logging disabled for now until I figure out a better way to do it

def logging(logfile=logfile):
    """ Add func calls to the logfile 
    
        args:
        -----
        func: Python function
        logfile: filepath for logging
        
        returns:
        --------
        func - with logging
    """

    def Inner(func):
        def wrapper(*args, **kwargs):
            import datetime

            # Get the current time and date
            now = datetime.datetime.now()

            # log the event that func was called
            with open(logfile, 'a+') as file:
                file.write('{0} - INFO - {1} called\n'.format(now, func.__name__))

            # call func
            return func(*args, **kwargs)

        return wrapper

    return Inner


def build_query(first, last):
    """ Accept two columns and join them in a single query """

    return 'AUTHFIRST({0}) and AUTHLASTNAME({1})'.format(first, last)


# @logging(logfile = logfile)
def get_metadata(entry):
    """ Helper function for extracting 
        
        - first/last name 
        - author id
        - affiliation name
        - main subject area
        
        from JSON response text 
    """

    pref = 'preferred-name'
    str_id = 'dc:identifier'
    aff = 'affiliation-current'
    aff_name = 'affiliation-name'

    last = entry.get(pref).get('surname')
    first = entry.get(pref).get('given-name')
    auid = entry.get(str_id)
    docs = entry.get('document-count')

    # some authors have no affiliation
    try:
        affil = entry.get(aff).get(aff_name)
    except AttributeError:
        affil = None

    # some authors only publish in one area
    try:
        subj = entry.get('subject-area')[0].get('$')
    except KeyError:
        subj = entry.get('subject-area').get('$')
    except TypeError:
        subj = None

    name = ', '.join([last, first])

    return name, auid, docs, affil, subj


def show_results(entries, num_results):
    """ Show the authors in search entries
    
        args:
        -----
        text: dict
    """

    print('{} results found\n'.format(num_results))

    # build a formatted string of all results
    head = 'Row - Name - Auid - Doc Count - Institution - Area\n'
    disp_results = ['{} - {} - {} - {} - {} - {}\n'.format(i, *get_metadata(item)) for i, item in enumerate(entries)]

    return head + ''.join(disp_results)


# @logging(logfile = logfile)
def get_auid(query: str, headers=None) -> str:
    """ Accepts a query string and returns the Scopus author ID 
    
        args:
        -----
        query: str - scopus url query 
        
        returns:
        --------
        str - dc:identifier from Scopus search results
    
    """

    def get_response(query: str, headers=headers) -> dict:
        """ Accepts a scopus url query and JSON headers returns the JSON response in dict format """

        return requests.get(query, headers=headers).json()

    txt = get_response(query, headers=headers)

    search_key = 'search-results'

    try:
        num_results = int(txt.get(search_key).get('opensearch:totalResults'))
    except:
        return None

    # 29 June 2021 - temporary change for validating findings
    #     if num_results == 1:
    #         return txt.get(search_key).get('entry')[0].get('dc:identifier')

    if num_results == 0:
        print('No matches found for search {}'.format(query))
        return None

    # what to do if there's more than one match but less than 25 matches
    elif num_results == 1:  # change back to > 1 after validating
        print(show_results(txt.get(search_key).get('entry'), num_results))
        print('\n{}'.format(query))

        # 29 June 2021 - temporary change for validating findings

    #         while True:
    #             try:
    #                 choice = int(input('Which author would you like to choose: \n0-{}\n'.format(num_results-1)))

    #                 if choice in list(range(num_results)):
    #                     return txt.get(search_key).get('entry')[choice].get('dc:identifier')
    #                 elif choice == 9999:
    #                     print('No suitable match found...moving on')
    #                     return None
    #                 elif choice == 'break':
    #                     print('Breaking out...')
    #                     break

    #                 else:
    #                     raise ValueError

    #             except KeyboardInterrupt:
    #                 print('Breaking out...')
    #                 break

    #             except ValueError:
    #                 print('Unknown command...try again...')
    #                 continue

    # TODO allow navigation for over 25 matches
    else:
        print('Over 25 matches found')
        return None


def api_search(df, letters=None, headers=None):
    """ Perform search of Scopus on a subset of letters """

    if letters:
        for key in letters:
            frame = df[key]

            frame['auid'] = None

            for row in frame.index:
                frame['auid'].loc[row] = get_auid(frame['request'].loc[row], headers=headers)
    else:

        df['auid'] = None

        for row in df.index:
            df['auid'].loc[row] = get_auid(df['request'].loc[row], headers=headers)
