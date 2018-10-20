"""
Identify or correct errors in the "athlete_data.csv" and creat a new file .

"""

__author__ = "Wang xu and 44498012"


from assign1_utilities import get_column, replace_column, truncate_string



def remove_athlete_id(row) :
    """Return a string without athlete id.

    Parameters:
        row (str): String of data with comma separators (CSV format).

    Return:
        str: A string without athlete id

    Preconditions:
        row != None
    """


    #creat a new string without athlete's id
    new_row = ""
    
    #calculate the number of columns in original row
    length = 1
    for word in row:
        if word == "," :
            length += 1
    column_number = 1
    
    #remove data without athlete's id into new string
    while column_number<length:
        y=get_column(row,column_number)
        new_row += y + ','
        column_number += 1  # Add comma between each column
    return new_row[:-1] # Remove extra comma at end of string


def check_number(string, max_characters, corrupt_check) :
    """ check whether string is  whole or floating-point number .

    Parameters:
        string (str): String to be checked.
        max_characters (int): Maximum length of string.
        corrupt_check(bool): Original type of bool of corrupt.

    Returns:
        bool: update the type bool of corrupt

    Preconditions:
        len(string) >= 0
        max_characters >= 0
        corrupt_check is the type bool
    """
    #check the length of string
    if len(string) > max_characters :
        corrupt_check = True

    #check the whole or floating-point number
    if string =="\n":  #string with only "\n" can be correct                                                     
        pass
    else:
        if string:
            try:
                float(string) 
            except ValueError:
                 corrupt_check = True
    return  corrupt_check


def check_name(string, corrupt_check) :
    """ check if characters in the string is satisfied with the format rule.

    Parameters:
        string (str): String to be checked.
        corrupt_check(bool): Original type of bool of corrupt.

    Returns:
        bool: update the type bool of corrupt

    Preconditions:
        len(string) >= 0
        corrupt_check is the type bool
    """
    for character in string:
        if (character == " " or character == "-"
            or character == "'"or character.isdigit()
            or character.isalpha()):
            pass
        else:
            corrupt_check = True
    return corrupt_check

def main() :
    """Main functionality of program."""
    with open("athlete_data.csv", "r") as raw_data_file, \
         open("athlete_data_clean.csv", "w") as clean_data_file :
        for row in raw_data_file :
            corrupt = False
            row = remove_athlete_id(row)
            row_to_process = row #Saves row in original state, minus athlete id.


            #check event name
            event_name = get_column(row_to_process,0)
            if len(event_name) > 30:
                new_event_name = truncate_string(event_name,30)
                row_to_process = replace_column(row_to_process,new_event_name,0)
            elif event_name == "":
                corrupt=True
            event_name = get_column(row_to_process,0)
            corrupt=check_name(event_name,corrupt)

 
            #check if event name is valid
            with open("event_names.csv", "r") as valid_event_names:
                valid_name = False #check if event name in the "event_names.csv"
                for even_name_row in valid_event_names:
                    correct_event_name = get_column(even_name_row, 0)
                    if event_name in correct_event_name:
                        valid_name = True
                        break
            if valid_name == False:
                corrupt = True
            valid_event_names.close()


            #check Athlete’s First Name
            first_name = get_column(row_to_process, 1)
            if len(first_name) > 30:
                new_first_name = truncate_string(first_name,30)
                row_to_process = replace_column(row_to_process,new_first_name,1)
            elif first_name == "" : # Athlete’s First Name cannot be empty
                corrupt = True
            first_name = get_column(row_to_process, 1)
            corrupt=check_name(first_name, corrupt)


            #check Athlete’s Surname
            surname = get_column(row_to_process,2)
            if len(surname) > 30:
                new_surname = truncate_string(surname,30)
                row_to_process=replace_column(row_to_process, new_surname, 2)
            elif surname=="":
                corrupt=True
            surname = get_column(row_to_process,2)
            corrupt=check_name(surname,corrupt)


            #check if athlete’name is valid
            with open("athlete_names.csv", "r") as valid_athlete_names:
                name_valid = False 
                for athlete_name_row in valid_athlete_names:
                    if (first_name in  athlete_name_row
                        and surname in  athlete_name_row):
                        name_valid = True
            if name_valid == False: 
                corrupt =True
            valid_athlete_names.close()


            #check Country Code
            country_code = get_column(row_to_process,3)
            if (len(country_code) > 3
                or  country_code =="" or not country_code.isalpha()):
                corrupt = True

            # turn all country code into uppercase letters
            new_country_code = country_code.upper()
            row_to_process = replace_column(row_to_process, new_country_code, 3)


            #check if country code is valid.
            country_code = get_column(row_to_process,3)
            with open("country_codes.csv","r") as valid_country_code:
                code_valid = False
                for code_row in valid_country_code:
                    if country_code in code_row:
                        code_valid = True
                if code_valid == False:
                    corrupt = True
            valid_country_code.close()


            #check Place
            place = get_column(row_to_process,4)
            if len(place) <= 3 and ( place.isdigit() or place == ''
                 or place == 'DNS' or place == 'DNF' or place == 'PEN'):
                if place.isdigit() and ((get_column(row_to_process,5)==""
                                         and get_column(row_to_process,6)=="")
                    or (get_column(row_to_process,5)
                        and get_column(row_to_process,6))):
                    corrupt=True
                else:
                    pass
            else:
                corrupt = True


            #check score
            score = get_column(row_to_process, 5)
            corrupt = check_number(score, 6, corrupt)


            #check time
            time = get_column(row_to_process, 6)
            corrupt = check_number(time, 8, corrupt)

            
            #check Medal
            medal = get_column(row_to_process, 7)
            
            #change medals into camelcase
            row_to_process=replace_column(row_to_process, medal.title(), 7)

            #check the format rules of medal
            medal = get_column(row_to_process, 7)
            if len(medal)>6 or not (medal =="Gold"
                                    or medal == "Silver"
                                    or medal == "Bronze"
                                    or medal == ''):
                corrupt = True 
            if medal =="":
                pass
            else:
                if ((medal =="Gold" and  place !='1')
                    or (medal =="Silver" and place !='2')
                    or (medal =="Bronze" and place !='3')):
                    corrupt = True 


            #check Olympic Record
            olympic_record = get_column(row_to_process, 8)
            corrupt = check_number(olympic_record, 8, corrupt)


            #check World Record
            world_record = get_column(row_to_process,9)
            corrupt = check_number(world_record,8,corrupt)

            #check if have same values with olympic record.
            if world_record != "" and world_record != olympic_record:
                corrupt = True

                
            #check Track Record
            track_record = get_column(row_to_process,10)
            corrupt = check_number(track_record,8,corrupt)


            if not corrupt :
                clean_data_file.write(row_to_process)
            else :
                row = row[:-1]# Remove new line character at end of row.
                clean_data_file.write(row + ",CORRUPT\n")



# Call the main() function if this module is executed
if __name__ == "__main__" :
    main()


"""
----------------------------------------------
MARKING:   ##### CSSE7030 #####

Total: 10

Meeting comments:
   Good assignment, just had some questions about doing the extension task

General comments:
   Programming Constructs
       Program is Well Structured & Readable
           Code structure highlights logical blocks and is easy to understand. Code does not employ global variables. Constants clarify code meaning.
       Variable and function names are meaningful
           All variable and function names are clear and informative, increasing readability of the code.
       Algorithmic logic is appropriate
           Algorithm design is not too complex or has minor logical errors. A few control structures are a little convoluted.
       Functions used appropriately
           Could have used additional function decomposition. 
       Well-Designed Functions
           Program is well-designed, splitting the logic into an appropriate number of general functions, where each function performs a single cohesive logical task.
   Functionality
       Column size limits
           All size limit rules are implemented correctly.
       Column format rules
           Most, if not all format rules are implemented correctly.
       Conditional constraints between columns
           At least two of the rules listed under the heading “Extension” are decently implemented.
       Extension
   Documentation
       Clear & Concise Comments
           Comments provide useful information that elaborates on the code. These are useful in understanding the logic and are not too wordy.
       All functions having informative docstring comments
           All docstrings provide a complete, unambiguous, description of how to use the function.
       Appropriate use of inline comments
           Inline comments are used to explain logical blocks of code (e.g. significant loops or conditionals).
   General
       Discuss:
       -additional function decomposition e.g. moving athlete_name check. 
       -some code could be simplified

----------------------------------------------
Tests version: 1.1.1
Version: 2018s1
/------------------------------------------------------------------------------\
|                              Summary of Results                              |
\------------------------------------------------------------------------------/
BasicTests
    +  1. Tests a file with no corruptions
ColumnSizeTests
    +  1. Tests that overlong event and athlete names are appropriately truncated
    +  2. Tests that corrupt size limit violations are correctly marked
ColumnFormatTests
    +  1. Tests the format of event and athlete names
    +  2. Tests the format of the country code column
    +  3. Tests the format of the place column
    +  4. Tests the format of the medal column
    +  5. Tests the format of the score, time, and record columns
ConditionalConstraintTests
    +  1. Tests conditional constraints between place, score and time
    +  2. Tests conditional constraints between place and medal
    +  3. Tests conditional constraints between record columns
MedalTieTests
    -  1. Tests ties with multiple gold medals
    -  2. Tests ties with multiple silver medals
ThreeMedalRuleTests
    -  1. Tests single missing medal
    -  2. Tests multiple missing medals
MasterFileTests
    +  1. Tests event name masterfile
    +  2. Tests athlete name masterfile
    +  3. Tests country code masterfile
    +  4. Tests multiple masterfiles
--------------------------------------------------------------------------------
/------------------------------------------------------------------------------\
|                                 Failed Tests                                 |
\------------------------------------------------------------------------------/
================================================================================
FAIL: MedalTieTests 1. Tests ties with multiple gold medals
--------------------------------------------------------------------------------
    Traceback (most recent call last):
    AssertionError: "Wome[54 chars]ld,,,\n\nWomen's Speedskating 500m,Yara,van Ke[89 chars],,\n" != "Wome[54 chars]ld,,,,CORRUPT\n\nWomen's Speedskating 500m,Yar[113 chars]PT\n"
    - Women's Speedskating 500m,Arianna,Fontana,ITA,1,,42.569,Gold,,,
    + Women's Speedskating 500m,Arianna,Fontana,ITA,1,,42.569,Gold,,,,CORRUPT
    ?                                                                ++++++++
    - Women's Speedskating 500m,Yara,van Kerkhof,NED,1,,42.569,Gold,,,
    + Women's Speedskating 500m,Yara,van Kerkhof,NED,1,,42.569,Gold,,,,CORRUPT
    ?                                                                 ++++++++
    - Women's Speedskating 500m,Kim,Boutin,CAN,2,,43.881,Silver,,,
    + Women's Speedskating 500m,Kim,Boutin,CAN,2,,43.881,Silver,,,,CORRUPT
    ?                                                             ++++++++
    
     : At least one of rows 15-17 should have been marked as corrupt
     These lines test: Invalid tie

================================================================================
FAIL: MedalTieTests 2. Tests ties with multiple silver medals
--------------------------------------------------------------------------------
    Traceback (most recent call last):
    AssertionError: "Wome[41 chars]er,,,\n\nWomen's Half-Pipe,Jiayu,Liu,CHN,2,98.[68 chars],,\n" != "Wome[41 chars]er,,,,CORRUPT\n\nWomen's Half-Pipe,Jiayu,Liu,C[92 chars]PT\n"
    - Women's Half-Pipe,Chloe,Kim,USA,2,98.25,,Silver,,,
    + Women's Half-Pipe,Chloe,Kim,USA,2,98.25,,Silver,,,,CORRUPT
    ?                                                   ++++++++
    - Women's Half-Pipe,Jiayu,Liu,CHN,2,98.25,,Silver,,,
    + Women's Half-Pipe,Jiayu,Liu,CHN,2,98.25,,Silver,,,,CORRUPT
    ?                                                   ++++++++
    - Women's Half-Pipe,Arielle,Gold,USA,3,85.75,,Bronze,,,
    + Women's Half-Pipe,Arielle,Gold,USA,3,85.75,,Bronze,,,,CORRUPT
    ?                                                      ++++++++
    
     : At least one of rows 18-20 should have been marked as corrupt
     These lines test: Invalid tie

================================================================================
FAIL: ThreeMedalRuleTests 1. Tests single missing medal
--------------------------------------------------------------------------------
    Traceback (most recent call last):
    AssertionError: "Wome[38 chars]ld,,,\n\nWomen's Moguls,Jakara,Anthony,AUS,2,9[55 chars],,\n" != "Wome[38 chars]ld,,,,CORRUPT\n\nWomen's Moguls,Jakara,Anthony[79 chars]PT\n"
    - Women's Moguls,Madii,Himbury,AUS,1,100,,Gold,,,
    + Women's Moguls,Madii,Himbury,AUS,1,100,,Gold,,,,CORRUPT
    ?                                                ++++++++
    - Women's Moguls,Jakara,Anthony,AUS,2,99,,Silver,,,
    + Women's Moguls,Jakara,Anthony,AUS,2,99,,Silver,,,,CORRUPT
    ?                                                  ++++++++
    - Women's Moguls,Britteny,Cox,AUS,3,98,,,,,
    + Women's Moguls,Britteny,Cox,AUS,3,98,,,,,,CORRUPT
    ?                                          ++++++++
    
     : At least one of rows 12-14 should have been marked as corrupt
     These lines test: No bronze medal awarded

================================================================================
FAIL: ThreeMedalRuleTests 2. Tests multiple missing medals
--------------------------------------------------------------------------------
    Traceback (most recent call last):
    AssertionError: "Men'[38 chars]ld,,,\n\nMen's Half-Pipe,Kent,Callister,AUS,2,[55 chars],,\n" != "Men'[38 chars]ld,,,,CORRUPT\n\nMen's Half-Pipe,Kent,Calliste[79 chars]PT\n"
    - Men's Half-Pipe,Scotty,James,AUS,1,100,,Gold,,,
    + Men's Half-Pipe,Scotty,James,AUS,1,100,,Gold,,,,CORRUPT
    ?                                                ++++++++
    - Men's Half-Pipe,Kent,Callister,AUS,2,99,,,,,
    + Men's Half-Pipe,Kent,Callister,AUS,2,99,,,,,,CORRUPT
    ?                                             ++++++++
    - Men's Half-Pipe,Nathan,Johnstone,AUS,3,98,,,,,
    + Men's Half-Pipe,Nathan,Johnstone,AUS,3,98,,,,,,CORRUPT
    ?                                               ++++++++
    
     : At least one of rows 18-20 should have been marked as corrupt
     These lines test: No silver or bronze medal awarded

--------------------------------------------------------------------------------
Ran 19 tests in 0.217 seconds with 15 passed/0 skipped/4 failed.


END TESTS
"""

