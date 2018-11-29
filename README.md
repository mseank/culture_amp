# SURVEY TOOL
This tool is for the Culture Amp Developer Coding Test.
## What it Does
The tool takes in two separate files: a survey file and a results file for that survey.

### How to use
It is read in via command line arguments, --survey and --results respectively. 
Starts at main on bottom of survey_tool.py

Example:

python bin/survey_tool.py --survey example-data/survey-1.csv --results example-data/survey-1-responses.csv

### Input (For completeness sake)
##### Survey File
Each row represents a question in that survey with headers defining what question data is in each column. The two
required columns for this program are "type" and "text," text being the question text.

##### Results File
Response columns are always in the following order:
* Email
* Employee Id
* Submitted At Timestamp (if there is no submitted at timestamp, you can assume the user did not submit a survey) 
* Each column from the fourth onwards are responses to survey questions.
* Answers to Rating Questions are always an integer between (and including) 1 and 5. 
* Blank answers represent not answered. 
* Answers to Single Select Questions can be any string.

### Output
The file prints two initial lines:
#### Participation
1) Participation Number - Total employees who submitted surveys
2) Participation Percentage - Percentage of employees who submitted

#### Averages
Following that, it goes through a dictionary of "ratingquestion" type questions and prints out
each question and then the average response for that question.

#### Other Cases
1)  In the case of no submitted surveys, the output will be "No rating responses were returned"
2)  In the case of a returned survey but with no rating questions, the output will be "Responses were returned, 
but there were no rating questions."
3)  In the case of one or two of the input files being blank, the output will be "One or both files were empty"
4)  The columns 'text' and 'type' are required for the survey CSV. If they are not present, the output will be
 "Invalid format for survey file. Requires both "text" and "type" fields."
 
### Design Decisions
1) I implemented pandas dataframes for evaluating the CSVs for speed and simplicity
2) I put _get_participation and _get_averages as their own methods to simplify testing

#### Check for Mean
The columns for the results dataframe are always numbers starting at 0. The first three are always
Email, Employee ID, and Submitted (Timestamp) - 0, 1, and 2 respectively. Therefore we know that column 3 will always be the first 
question. The survey dataframe has each question as a row. Therefore we iterate through each question and index,
starting at index=0. The mean_series has the means mapped by the column number, starting at 3. These map
directly back to the questions, starting at 0. Therefore we can connect result column 3 to survey index 0, 
result column 4 to survey index 1, etc.

#### Tests
The tests were run using pytest - install using pip and then simply run pytest from the parent directory

See: https://docs.pytest.org/en/latest/getting-started.html#install-pytest