"""
Sample solution to assignment 1 for CSSE1001/7030 in semester 1 of 2018.
This application processes a file that contains results data from
sporting events. The processing checks for the validity of the data
and corrects the data's format where possible.
"""

__author__ = "Richard Thomas"
__copyright__ = "The University of Queensland, 2018"


from assign1_utilities import get_column, replace_column, truncate_string


EVENT_NAME_COLUMN = 0
ATHLETE_FIRST_NAME_COLUMN = 1
ATHLETE_SURNAME_COLUMN = 2
COUNTRY_CODE_COLUMN = 3
PLACE_COLUMN = 4
SCORE_COLUMN = 5
TIME_COLUMN = 6
MEDAL_COLUMN = 7
OLYMPIC_RECORD_COLUMN = 8
WORLD_RECORD_COLUMN = 9
TRACK_RECORD_COLUMN = 10

MAX_NAME_LENGTH = 30
VALID_NAME_CHARS = ("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
                    + "1234567890-' ")
COUNTRY_CODE_LENGTH = 3
MAX_PLACE_LENGTH = 3
MAX_SCORE_LENGTH = 6
MAX_TIME_LENGTH = 8
MAX_RECORD_LENGTH = 8



def is_float(test_value) :
    """Determines if test_value represents a floating point value.

    Parameter:
        test_value: Value to be checked to see if it is a floating point value
                    Assumed to be a string, but any type will work

    Return:
        bool: True if test_value's contents are a floating point value
              False if test_value's contents are not a floating point value
    """
    try :
        float(test_value)
        valid_float = True
    except ValueError :         # Unable to convert test_value to a float
        valid_float = False
    except TypeError :          # Not a valid parameter type (e.g. None)
        valid_float = False
        
    return valid_float



def is_empty_string(test_string) :
    """Determines if test_string is an empty string.

    Parameter:
        test_string (str): String to be tested

    Return:
       (bool) Returns True iff the string is empty.
    """
    return len(test_string) == 0



def is_valid_string(string, valid_chars) :
    """Determines if all the characters in string are within the valid_chars set.

        Parameters:
            string (str): String to check
            valid_chars (str): All the valid characters

        Return:
            (bool) Returns true if string is only made up of valid characters.
    """
    for character in string :
        if character not in valid_chars :
            return False
        
    return True


def remove_athlete_id(row) :
    """Remove the athlete id column (first column) from a row.

    Assumes that every row contains an athlete id column.
    This is a safe assumption for the assignment.

    Parameters:
        row (str): Comma separated row of athlete data.

    Return:
        str: String containing all data after the first column in this row.
    """
    i = 0
    while row[i] != ',' :
        i += 1
    return row[i+1:]



def process_name(row, name_position) :
    """Process a name to check if it meets the specified format rules.

    Parameters:
        row (str): Comma separated row of athlete data.
        name_position (int): Column number to be processed

    Returns:
        bool: True if the name to be checked is corrupt;
              False if it is not corrupt.
        str : Row with name truncated if it was too long.
    """
    corrupt = False
    name = get_column(row, name_position)
    
    if is_empty_string(name) or not is_valid_string(name, VALID_NAME_CHARS) :
        corrupt = True
    else :
        name = truncate_string(name, MAX_NAME_LENGTH)
        row = replace_column(row, name, name_position)

    return corrupt, row    



def process_country_code(row, code_position) :
    """Process the country code to check if it meets the specified format rules.

    Parameters:
        row (str): Comma separated row of athlete data.
        code_position (int): Column number of the country code to be processed.

    Returns:
        bool: True if the code to be checked is corrupt;
              False if it is not corrupt.
        str : Row with country code made uppercase if it was not already.
    """
    corrupt = False
    country_code = get_column(row, code_position)
    
    if not country_code.isalpha() or len(country_code) != COUNTRY_CODE_LENGTH :
        corrupt = True
    else :
        row = replace_column(row, country_code.upper(), code_position)

    return corrupt, row    



def is_valid_place(place) :
    """Check that 'place' meets the format rules for the place.

    Parameters:
        place (str): Data to be checked

    Returns:
        bool: True if 'place' is at most MAX_PLACE_LENGTH characters long,
              and is a whole number or 'DNS', 'DNF' or 'PEN';
              False otherwise.
    """
    return (len(place) <= MAX_PLACE_LENGTH
            and (place.isdigit() or place == ''
                 or place == 'DNS' or place == 'DNF' or place == 'PEN'))



def process_placing(row, place_position, medal_position) :
    """Process the place and medal to check if they meet the specified format rules.

    Parameters:
        row (str): Comma separated row of athlete data.
        place_position (int): Column number of the place to be processed.
        medal_position (int): Column number of the corresponding medal.

    Returns:
        bool: True if the place or medal to be checked are corrupt;
              False if they are not corrupt.
        str : Row with medal in title case if it was not already.
    """
    corrupt = False
    place = get_column(row, place_position)
    medal = get_column(row, medal_position).capitalize()

    if not is_valid_place(place) :
        corrupt = True
    elif not (medal == ""
              or medal == "Gold" or medal == "Silver" or medal == "Bronze") :
        corrupt = True
    # Check that place corresponds to appropriate medal.
    elif place == "1" and medal != "Gold" :
        corrupt = True
    elif place == "2" and medal != "Silver" :
        corrupt = True
    elif place == "3" and medal != "Bronze" :
        corrupt = True
    # Check that medal corresponds to appropriate place.
    elif medal == "Gold" and place != "1" :
        corrupt = True
    elif medal == "Silver" and place != "2" :
        corrupt = True
    elif medal == "Bronze" and place != "3" :
        corrupt = True
    else :
        row = replace_column(row, medal, medal_position)

    return corrupt, row    



def process_result(row, score_position, time_position, place_position) :
    """Process the score or time to check if they meet the specified format rules.

    Parameters:
        row (str): Comma separated row of athlete data.
        score_position (int): Column number of the score result.
        time_position (int) : Column number of the time result.
        place_position (int): Column number of the place.

    Returns:
        bool: True if the score or time to be checked are corrupt
              or if there is data for both score and time
              or place should not have a score or time;
              False if there is only one and it is not corrupt.
    """
    corrupt = False
    score = get_column(row, score_position)
    time = get_column(row, time_position)
    place = get_column(row, place_position)

    if place.isdigit() :
        # If athlete placed in the event they must have either a score or a time.
        if ((len(score) > 0 and len(time) > 0)
            or (len(score) == 0 and len(time) == 0)):
            corrupt = True
        # Check that the score or time are valid.
        elif (len(time) == 0
              and (not is_float(score) or len(score) > MAX_SCORE_LENGTH)) :
            corrupt = True
        elif (len(score) == 0
              and (not is_float(time) or len(time) > MAX_TIME_LENGTH)) :
            corrupt = True
    # Otherwise, athlete did not place in the event,
    # so should not have either a score or a time.
    elif len(score) > 0 or len(time) > 0 :
        corrupt = True

    return corrupt    



def is_valid_record(record) :
    """Check that record meets the format rules for a record.

    Parameters:
        record (str): Data to be checked

    Returns:
        bool: True if record is at most MAX_RECORD_LENGTH characters long
              and is a floating point number, or the record is an empty string;
              False otherwise.
    """
    return (len(record) == 0
            or (len(record) <= MAX_RECORD_LENGTH and is_float(record)))



def process_records(row, olympic_rec_position,
                    world_rec_position, track_rec_position) :
    """Process the records to check if they meet the specified format rules.

    Parameters:
        row (str): Comma separated row of athlete data.
        olympic_rec_position (int): Column number of the olympic record.
        world_rec_position (int)  : Column number of the world record.
        track_rec_position (int)  : Column number of the track record.

    Returns:
        bool: True if the records to be checked are corrupt
              or if world and olympic records do not match;
              False if the records are not corrupt.
    """
    corrupt = False
    olympic_record = get_column(row, olympic_rec_position)
    world_record = get_column(row, world_rec_position)
    track_record = get_column(row, track_rec_position)

    if (not is_valid_record(olympic_record)
        or not is_valid_record(world_record)
        or not is_valid_record(track_record)) :
        corrupt = True
    elif len(world_record) > 0 and world_record != olympic_record :
        corrupt = True

    return corrupt    



def main() :
    """Iterates through each line of the data file processing the data.
       This includes checking that the data is in the correct format, and
       that any dependencies between data elements are enforced.
       Any data formatting errors that can be corrected are corrected.
    """
    with open("athlete_data.csv", "r") as raw_data_file, \
         open("athlete_data_clean.csv", "w") as clean_data_file :
        for row in raw_data_file :
            corrupt = False
            row = row.strip()
            row = remove_athlete_id(row)
            row_to_process = row    # Saves row in original state, minus athlete id.

            # Process names to check if they are corrupt
            # and to truncate names that are too long.
            for name_position in range(EVENT_NAME_COLUMN,
                                       ATHLETE_SURNAME_COLUMN + 1) :
                if not corrupt :
                    corrupt, row_to_process = process_name(row_to_process,
                                                           name_position)

            # Process Country Code to check if it is in the correct format
            # and ensure that it is in all uppercase.
            if not corrupt :
                corrupt, row_to_process = process_country_code(row_to_process,
                                                               COUNTRY_CODE_COLUMN)
                
            # Process place and corresponding medal to check if they are in the 
            # correct format and ensure that medal is in title case.
            if not corrupt :
                corrupt, row_to_process = process_placing(row_to_process,
                                                          PLACE_COLUMN, 
                                                          MEDAL_COLUMN)
                
            # Process score and time to check that they are mutually exclusive, 
            # correspond to a valid place, and are in the correct format.
            if not corrupt :
                corrupt = process_result(row_to_process, SCORE_COLUMN,
                                         TIME_COLUMN, PLACE_COLUMN)
                
            # Process the records to check if they are in the correct format and
            # if a world record is set that it has a corresponding olympic record.
            if not corrupt :
                corrupt = process_records(row_to_process, OLYMPIC_RECORD_COLUMN,
                                          WORLD_RECORD_COLUMN, TRACK_RECORD_COLUMN)

            # Save the row data to the cleaned data file.
            if not corrupt :
                clean_data_file.write(row_to_process + "\n")
            else :
                clean_data_file.write(row + ",CORRUPT\n")    
    


# Call the main() function if this module is executed
if __name__ == "__main__" :
    main()

