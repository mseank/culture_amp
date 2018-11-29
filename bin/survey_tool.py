"""Culture Amp Developer Coding Test - Survey Tool"""
import argparse
import pandas as pd
from pandas.errors import EmptyDataError


def process_survey(survey_location, results_location):
    """
    Evaluates user-inputted survey and result CSVs to print out participation metrics and averages for rating questions
    :param survey_location: Filepath to the survey CSV
    :param results_location: Filepath to the results CSV
    :return:
    """
    # Read in the files to Pandas dataframes for easy access
    # Column names for survey are taken from the CSV. Needs 'type' and 'text' at a minimum
    try:
        survey_df = pd.read_csv(survey_location)
        if 'type' not in survey_df.columns or 'text' not in survey_df.columns:
            print('Invalid format for survey file. Requires both "text" and "type" fields.')
            return False

        # Specifying header to None will enumerate the columns, since the results csv has no headers
        # Column names are ints from 0-n, n being number of questions + 2
        results_df = pd.read_csv(results_location, header=None)
    # Catch empty files
    except EmptyDataError as e:
        print('One or both files were empty')
        return False
    # Catch nonexistent files
    except FileNotFoundError:
        print('One or both of the files do not exist')
        return False

    total_employees, participating_employees = _get_participation(results_df)

    question_averages_dictionary = _get_averages(survey_df, results_df)

    print('Participation Percentage: {}%'.format((participating_employees / total_employees) * 100))
    print('Total Employees Who Submitted a Result: {}'.format(participating_employees))

    if participating_employees == 0:
        print('No rating responses were returned.')

    # Blank dictionaries resolve to False
    elif not question_averages_dictionary:
        print('Responses were returned, but there were no rating questions.')

    else:
        for question, average in question_averages_dictionary.items():
            print('Question: "{}" \n had an average response of {}'.format(question, average))


def _get_participation(results_df):
    # Print out total participation and participation percentage
    total_employees = len(results_df.index)
    # Third column is always the timestamp and blank is non-participation, just count the non-null ones (index is 2)
    participating_employees = len(results_df.loc[results_df[2].notnull()])
    return total_employees, participating_employees


def _get_averages(survey_df, results_df):
    # This method makes a dictionary of questions and rating averages

    # Now a simple line to get the mean of all columns that have number values.
    # Remove unsubmitted surveys so we don't count their responses.
    results_df = results_df.loc[results_df[2].notnull()]

    # If there are no submitted surveys, the dataframe will be empty. Return None.
    if results_df.empty:
        return None

    # df.mean returns a series of means for columns i.e. [{column_name, mean}, ...]
    mean_series = results_df.mean(axis=0)

    # Employee ID column may or may not be just numbers. If they are, they'll be in the mean series. We don't want it.
    # Column 1 will always be the employee ID
    if 1 in mean_series:
        mean_series.pop(1)
    # For easier testability, I'll return them in a dictionary instead of just printing them in the for loop
    question_averages_dictionary = {}
    for index, row in survey_df.iterrows():
        if row['type'] == 'ratingquestion':
            # See README for description in section check for mean
            if (3 + index) in mean_series:
                # If any surveys are submitted, there should be an answer for every question,
                # but it can't hurt too much to check
                question_averages_dictionary[row['text']] = mean_series[3 + index]
    return question_averages_dictionary


if __name__ == '__main__':
    # We will parse in the two file values, survey and survey_results
    parser = argparse.ArgumentParser(description='Takes two file values.')

    # We could just not put flags and it's automatically required, but I like flags because it prevents you
    # from needing to remember which argument goes first. All are still required.
    parser.add_argument('-s', '--survey', help='Location of survey file', required=True)
    parser.add_argument('-r', '--results', help='Location of results file', required=True)

    args = parser.parse_args()
    arg_dict = vars(args)

    process_survey(arg_dict['survey'], arg_dict['results'])
