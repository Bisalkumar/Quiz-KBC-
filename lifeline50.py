import random

def ranopt(Question, Options, Correct_Answer, i):
    """
    This function models the 50-50 lifeline. It takes in the current Question, its Options,
    the Correct_Answer, and the question number (i).
    It modifies the options to retain only the correct answer and one randomly chosen wrong answer.
    """
    
    # Create a copy of the options to avoid modifying the original list
    temp_options = Options.copy()

    # Remove the correct answer temporarily
    temp_options.remove(Correct_Answer)

    # Randomly select one wrong answer
    wrong_answer = random.choice(temp_options)

    # Now set Options to only contain the correct answer and one wrong answer
    new_options = [Correct_Answer, wrong_answer]
    random.shuffle(new_options)  # Shuffle so the order isn't predictable

    return new_options

def get_audience_hint(Options, Correct_Answer):
    """
    This function models the 'Ask the Audience' lifeline. 
    It returns two options: the correct answer and one randomly chosen wrong answer.
    """
    
    remaining_options = [option for option in Options if option != Correct_Answer]
    wrong_choice = random.choice(remaining_options)
    
    return (Correct_Answer, wrong_choice)
