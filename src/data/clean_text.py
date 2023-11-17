import os
import sys
from pathlib import Path
import re
from nltk.tokenize import sent_tokenize, word_tokenize

grandparent_path = Path(__file__).parents[1]
data_path = Path(__file__).parents[2]

raw_data_path = os.path.join(data_path, 'data', 'raw', 'enron_subject_line')
raw_train_path = os.path.join(raw_data_path, 'train')
raw_test_path = os.path.join(raw_data_path, 'test')
raw_dev_path = os.path.join(raw_data_path, 'dev')

interim_train_path = os.path.join(data_path, 'data', 'interim', 'train')
interim_test_path = os.path.join(data_path, 'data', 'interim', 'test')
interim_dev_path = os.path.join(data_path, 'data', 'interim', 'dev')

mymodule_dir = os.path.join(grandparent_path, 'utils')
sys.path.append( mymodule_dir )

from reader import DataReader

greetings = [
    "Dear", 
    "Hello", 
    "Hi", 
    "Good morning", 
    "Good afternoon"
    "Good evening",
    "Hi there",
    "Hello there",
    "Greetings",
    "Hey [Name]",
    "To whom it may concern",
    "Hi folks",
    "Dear Sir/Madam",
    "Ladies and gentlemen",
    "Team",
    "Esteemed [Name]",
    "My dear [Name]",
    "Dear all",
    "Hi everyone",
    "Hello everyone",
    "Good day",
    "Warm greetings",
    "Salutations",
    "Howdy",
    "Hope this email finds you well",
    "I trust this email finds you in good health",
    "I hope you're doing well",
    "I hope you're well",
    "I trust you are well",
    "It's a pleasure to write to you",
    "I'm writing to you",
    "Good to e-meet you",
    "How are you?",
    "Hoping this message sees you in good spirits",
    "How's everything?",
    "Just checking in",
    "Warmest regards",
    "Welcome aboard",
    "Best regards",
    "Sincerely",
    "Yours truly",
    "Kind regards",
    "Warm regards",
    "With gratitude",
    "Take care",
    "With appreciation",
    "In appreciation",
    "Respectfully",
    "Cordially",
    "Thanks",
    "Thanks again",
    "With respect",
    "Cheers",
    "Best wishes",
    "With best regards",
    "With all my best",
    "With warmest regards",
    "With all the best",
    "Yours faithfully",
    "Fondly",
    "With care",
    "With sincere thanks",
    "With warmest regards",
    "In friendship",
    "Best of luck",
    "Wishing you the best",
    "Until next time",
    "Stay well",
    "Take good care",
    "With great respect",
    "Warmly",
    "Regards",
    "Yours in service",
    "Sincerely yours",
    "With kindest regards",
    "With best wishes",
    "In kind regards",
    "Sincerely yours",
    "With high regards",
    "With deep appreciation",
    "Looking forward to see you",
    "Looking forward to seeing you",
    "Looking forward to be with you",
    "Looking forward to being with you"
    ]

for i in range(len(greetings)):
    greetings[i] = greetings[i].lower()

greetings_pattern = r'\b(?:' + '|'.join(re.escape(g) for g in greetings) + r')\b'
greetings_pattern = re.compile(greetings_pattern)

# function to remove salutions and greetings from entire mail body
def remove_salutation(email_body):

    email_body_without_greetings = re.sub(greetings_pattern, 'arkishman', email_body)
    return email_body_without_greetings

def get_difference(original, copy):

    pos_original, pos_copy = 0, 0
    result = ""
    original = word_tokenize(original)
    copy = word_tokenize(copy)

    flag = 0
    while(pos_original < len(original) and pos_copy < len(copy)):
        if (flag == 0):
            if (original[pos_original].lower() == copy[pos_copy]):
                result += original[pos_original] + " "
                pos_copy += 1
            elif (copy[pos_copy] == "arkishman"):
                flag = 1
                pos_copy += 1
            pos_original += 1
        else:
            if (original[pos_original].lower() == copy[pos_copy]):
                flag = 0
                pos_original += 1
                pos_copy += 1
            else:
                pos_original += 1

    while(pos_original < len(original)):
        result += original[pos_original] + " "
        pos_original += 1
    return result

def clean_email_body(raw_path, interim_path):

    f = DataReader(raw_path)
    emails = f.read_file()
    
    for i in range(len(emails)):

        # get rid of everything from @subject
        subject_index = emails[i].find("@subject")
        temp_body = emails[i][ : subject_index]
        email_copy = temp_body
        body_without_greeting = remove_salutation(email_copy.lower())
        new_body = get_difference(temp_body, body_without_greeting)

        email_id = "email_{id}.txt".format(id = i + 1)
        file_path = os.path.join(interim_path, email_id)
        writer = open(file_path, "w")
        writer.write(new_body)
        writer.close()

clean_email_body(raw_train_path, interim_train_path)
clean_email_body(raw_test_path, interim_test_path)
clean_email_body(raw_dev_path, interim_dev_path)
