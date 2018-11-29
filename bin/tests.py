from bin.survey_tool import _get_averages, _get_participation, process_survey
import pandas as pd

# Test value file locations
SURVEY_ONE = r'..\example-data\survey-1.csv'
RESULTS_ONE = r'..\example-data\survey-1-responses.csv'
SURVEY_TWO = r'..\example-data\survey-2.csv'
RESULTS_TWO = r'..\example-data\survey-2-responses.csv'
SURVEY_THREE = r'..\example-data\survey-3.csv'
RESULTS_THREE = r'..\example-data\survey-3-responses.csv'


def test_survey_1():
    survey_df = pd.read_csv(SURVEY_ONE)
    results_df = pd.read_csv(RESULTS_ONE, header=None)

    # Test that the participation is correct
    total_employees, participating_employees = _get_participation(results_df)
    assert(total_employees == 6)
    assert(participating_employees == 5)

    # Test that the means were correct
    question_averages_dictionary = _get_averages(survey_df, results_df)
    print(question_averages_dictionary)
    assert(question_averages_dictionary['I like the kind of work I do.'] == 4.6)
    assert(question_averages_dictionary['In general, I have the resources (e.g., business tools, information, facilities, IT or functional support) I need to be effective.'] == 5)
    assert(question_averages_dictionary['We are working at the right pace to meet our goals.'] == 5)
    assert(question_averages_dictionary['I feel empowered to get the work done for which I am responsible.'] == 3.6)
    assert(question_averages_dictionary['I am appropriately involved in decisions that affect my work.'] == 3.6)


def test_survey_2():
    survey_df = pd.read_csv(SURVEY_TWO)
    results_df = pd.read_csv(RESULTS_TWO, header=None)

    # Test that the participation is correct
    total_employees, participating_employees = _get_participation(results_df)
    assert(total_employees == 5)
    assert(participating_employees == 5)

    # Test that the means were correct
    question_averages_dictionary = _get_averages(survey_df, results_df)
    assert (question_averages_dictionary['I like the kind of work I do.'] == 4.6)
    assert (question_averages_dictionary['In general, I have the resources (e.g., business tools, information, facilities, IT or functional support) I need to be effective.'] == 5)
    assert (question_averages_dictionary['We are working at the right pace to meet our goals.'] == 5)
    assert (question_averages_dictionary['I feel empowered to get the work done for which I am responsible.'] == 3.6)


def test_survey_3():
    survey_df = pd.read_csv(SURVEY_THREE)
    results_df = pd.read_csv(RESULTS_THREE, header=None)

    # Test that the participation is correct
    total_employees, participating_employees = _get_participation(results_df)
    assert (total_employees == 5)
    assert (participating_employees == 0)

    # Test that the means were correct
    question_averages_dictionary = _get_averages(survey_df, results_df)
    assert (question_averages_dictionary is None)


def test_no_text_and_or_type():
    wrong_columns = r'..\example-data\wrong-columns.csv'
    # results shouldn't matter here, testing columns. any file will do.
    assert(process_survey(wrong_columns, RESULTS_ONE) is False)


def test_no_rating_questions():
    # I doubt this will happen, but who knows, customers are unpredictable
    no_ratings_survey = r'..\example-data\no-rating-questions-survey.csv'
    no_ratings_responses = r'..\example-data\no-rating-questions-survey-responses.csv'
    survey_df = pd.read_csv(no_ratings_survey)
    results_df = pd.read_csv(no_ratings_responses, header=None)

    # Test that the participation is correct
    total_employees, participating_employees = _get_participation(results_df)
    assert (total_employees == 3)
    assert (participating_employees == 2)

    # Test that the means were correct
    question_averages_dictionary = _get_averages(survey_df, results_df)
    # Empty dictionaries return as false.
    assert (not question_averages_dictionary)


def test_empty_files():
    empty_file = r'..\example-data\empty-responses.csv'
    assert (process_survey(empty_file, RESULTS_ONE) is False)
    assert (process_survey(SURVEY_ONE, empty_file) is False)
    assert (process_survey(empty_file, empty_file) is False)


def test_nonexistent_files():
    made_up_location = r'..\example-data\not-real.csv'
    assert (process_survey(made_up_location, RESULTS_ONE) is False)
    assert (process_survey(SURVEY_ONE, made_up_location) is False)
    assert (process_survey(made_up_location, made_up_location) is False)
