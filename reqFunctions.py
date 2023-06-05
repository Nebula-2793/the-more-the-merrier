import random
import os
from colorama import Fore, Style

#defining colours
c_reset = Style.RESET_ALL
c_cyan = c_reset + Fore.CYAN
c_red = c_reset + Fore.RED 
c_green = c_reset + Fore.GREEN
c_magenta = Fore.MAGENTA

#when clear() is called, it clears the whole terminal
clear = lambda : os.system('cls')

#while debugging, clearing the terminal causes problems -> so mock function
'''def clear():
    print("CLEAR")'''

def strike(text):
    result = ''
    for chr in text:
        result = result + chr + '\u0336'
        result = c_red + result
    return result

class class_question:
    def __init__(self, question, list_options, dict_options_value, list_values, list_sorted_options, mode, unit):
        self.question = question
        self.list_options = list_options
        self.dict_options_value = dict_options_value
        self.list_sorted_values = list_values
        self.list_sorted_options = list_sorted_options
        self.mode = mode
        self.unit = unit

def read_file(path):
    f = open(path, "r")
    lines = f.readlines()
    f.close()
    return lines

def read_data(list_obj_questions, lines):
    question = ""
    list_options = []
    list_values = []
    dict_options_value = {}
    list_sorted_options = []
    unit = ""
    mode = "values provided"

    new_question = True
    for line in lines:
        if (line == "THE END"):
            break
        elif (new_question):
            question_line_split = line.split("#")
            question = question_line_split[0].rstrip("\n").rstrip(" ")
        if (len(question_line_split) != 1):
            unit = question_line_split[1].lstrip(" ").rstrip("\n")
            new_question = False
        elif (line == "NO VALUES: ASCENDING ORDER\n"):
            #print(f"{c_green} DEBUGGING ASCENDING MODE {c_reset}")
            mode = "ascending order"
        elif (line == "NO VALUES: DESCENDING ORDER\n"):
            #print(f"{c_green} DEBUGGING DESCENDING MODE {c_reset}")
            mode = "descending order"
        elif (line != "\n"):
            try:
                line_split = line.split(",", 1) #maxLimit = 1
                option = line_split[0].rstrip("\n")
                #print(f"DEBUGGING option {option}")
                list_options.append(option)
                if (mode == "values provided"):
                    value = (line_split[1].rstrip("\n")).lstrip(" ")
                    try:
                        value = int(value)
                    except:
                        #if the value is a float, not an integer
                        value = float(value)
                    #print(f"DEBUGGING, value: {value}")

                elif (mode == "ascending order"):
                    value = lines.index(line) #lines read later will have a higher number, cuz higher index -> ascending
                
                elif (mode == "descending order"):
                    value = -1*lines.index(line) #just like ascending but opposite cuz -ve -> descending
                
                #if it's already in values, then two options with same values exist -> so they'll have the same points (so just once in the list)
                if value not in list_values:
                    list_values.append(value)

                dict_options_value[option] = value
                list_values.sort()
                #inserts the option in the optionsList at the index at WHICH the value is in the valuesList
                #this list was needed to print the answer key
                list_sorted_options.insert(list_values.index(value), option)
                #print("DEBUGGING", list_nested_sorted_option_value)

            except:
                try:
                    #since there is an error in processing the line, it needs to be removed from the list
                    list_options = list_options.remove(option)
                except:
                    #just in case it's not in the list
                    pass
                clear()
                line = line.rstrip("\n")
                print(f"{c_red}error reading a data line \nthe line: \"{line}\"\n of the question \"{question}\" {c_reset}")
                abc = input(f"\n{c_red}No worries! Your experience will not be compromised:) \nPress enter to continue{c_reset}") #just so that the user presses the enter key

        else: #(line == "\n")
            #question_set finished
            #print("DEBUGGING, question set ended")

            '''print(question)
            print(list_options)
            print(dict_options_value)
            print(list_values)'''

            random.shuffle(list_options)

            list_obj_questions.append(class_question(question, list_options, 
            dict_options_value, list_values, list_sorted_options, mode, unit))
            new_question = True

            list_options = []
            list_values = []
            dict_options_value = {}
            list_sorted_options = [] 
            mode = "values provided" 
            unit = ""

            random.shuffle(list_obj_questions)
            return list_obj_questions
        
def ask_quiz_details(num_qs, player1, player2, list_obj_questions, num_max_qs):
    clear()
    print(f"{c_green}Welcome to More The Merrier: A unique multiplayer quiz!{c_reset}")
    player1 = input(f"\n{c_cyan}Please enter name of player1:{c_reset} ")

    while (player1 == ""):
        print(f"{c_red}INVALID: cannot be empty{c_reset}")
        player1 = input(f"\n{c_cyan}Please enter name of player1:{c_reset} ")
        player2 = input(f"{c_cyan}Please enter name of player2:{c_reset} ")

    while (player2 == ""):
        print(f"{c_red}INVALID: cannot be empty{c_reset}")
        player2 = input(f"{c_cyan}Please enter name of player2:{c_reset} ")

    is_input_okay = False
    while (not is_input_okay):
        try:
            num_qs = int(input(f"\n{c_cyan}The number of questions must be a +ve even integer. With the maximum number of questions being {num_max_qs}\nHow many questions would you like to play?{c_reset} "))
            is_input_okay = True
            list_obj_questions = list_obj_questions[:num_qs]
            if (num_qs <= 0):
                is_input_okay = False
                print(f"{c_red}INVALID: number of questions must be more than 0{c_reset}")
            if (num_qs % 2 != 0):
                is_input_okay = False
                print(f"{c_red}INVALID: number of questions must be even{c_reset}")
            if (num_qs > num_max_qs):
                is_input_okay = False
                print(f"{c_red}INVALID: maximum number of questions is {num_max_qs} {c_reset}")
        except: #if it can't be converted into an integer
            print(f"{c_red}INVALID: number of questions must be an integer {c_reset}")
            is_input_okay = False
            num_qs = -1

    return(num_qs, player1, player2, list_obj_questions)

def actual_quiz(dict_score, player1, player2, list_obj_questions, list_serials, num_turns_each_q):
    dict_score[player1] = 0
    dict_score[player2] = 0
    first_player1 = True #is the first turn of player1?
    turn_player1 = True #is the CURRENT turn of player1?

    for q_set_obj in list_obj_questions:
        question = q_set_obj.question
        current_list_options = q_set_obj.list_options
        current_dict_options_value = q_set_obj.dict_options_value
        current_list_sorted_values = q_set_obj.list_sorted_values
        current_list_sorted_options = q_set_obj.list_sorted_options
        current_unit = q_set_obj.unit
        current_mode = q_set_obj.mode

        menu = ""
        list_valid_serials = []

        if(first_player1):
            turn_player1 = True
        else:
            turn_player1 = False
        first_player1 = not first_player1

        list_valid_serials = list_serials[0:len(current_list_options)]

        for player_turn in range(num_turns_each_q):
            clear()
            #print(f"DEBUGGING, listOptions {current_list_options} \nlistValues {current_list_sorted_values}")

            menu = ""
            #making the menu
            for i in range(0, len(current_list_options)):
                current_line = f"{list_serials[i]}. {current_list_options[i]}"
                if (list_serials[i] not in list_valid_serials):
                    current_line = strike(current_line)
                else:
                    current_line = c_green + current_line
                    menu += F"{current_line} \n"

                print(f"\n{c_cyan}{question}\n{menu}")

                if(turn_player1):
                    player_name = player1
                else:
                    player_name = player2

                serial_input = input(f"{c_cyan}{player_name}, {c_magenta}Choose an option by entering its respective letter:{c_reset} ")

                while (serial_input.upper() not in list_valid_serials):
                    serial_input = input(f"{c_red}INVALID INPUT {c_reset}")

                #print("DEBUGGING accepted")
                option_selected = current_list_options[list_serials.index(serial_input.upper())]
                value_of_option_selected = current_dict_options_value[option_selected]
                #print(f"DEBUGGING, {current_list_sorted_values}")
                points = (current_list_sorted_values.index(value_of_option_selected) + 1)*10 #cuz index of first element is 0
                #print(f"DEBUGGING: {current_list_sorted_values}, {value_of_option_selected}, {points}")
                dict_score[player_name] = dict_score[player_name] + points
                turn_player1 = not turn_player1
                list_valid_serials.remove(serial_input.upper())
                
            print_answer_key_score(current_list_sorted_options, current_list_sorted_values, player1, player2, dict_score, current_mode, current_unit)
            return dict_score, player1, player2
        
def print_answer_key_score(current_list_sorted_options, current_list_sorted_values, player1, player2, dict_score, current_mode, current_unit):
    #all player turns over
    clear()

    #printing the answer key
    ans_key = "\nANSWER KEY"
    for i in range(len(current_list_sorted_options)):
        if (current_mode == "values provided"):
            ans_key += f"\n({(i+1)*10}) {current_list_sorted_options[i]} : {current_list_sorted_values[i]} {current_unit}"
        else:
            #doesn't print values
            ans_key += f"\n({(i+1)*10}) {current_list_sorted_options[i]}"
    print(c_cyan + ans_key)

    #printing score after every question
    print(f"\n{c_green}SCORE\n{player1}: {dict_score[player1]}\n{player2}: {dict_score[player2]}")

    #random input statement to wait until user enters something
    abc = input(f"{c_magenta}\nPress enter when you're ready to start the next question{c_reset}")

def decide_winner(dict_score, player1, player2):
    clear()
    print(f"{c_magenta}\nQUIZ OVER\n\n{c_cyan}FINAL SCORE\n{player1}: {dict_score[player1]}\n{player2}: {dict_score[player2]}")
    #all questions over, checking winner

    if (dict_score[player1] == dict_score[player2]):
        clear() 
        print(f"{c_magenta}\nInteresting, it's a tie with both players having a score of {dict_score[player1]} points\n")
    elif (dict_score[player1] > dict_score[player2]):
        print_winner(player1, dict_score[player1])
    else:
        print_winner(player2, dict_score[player2])

def print_winner(winner, points):
    print(f"\n{c_magenta}{winner} wins with {points} points {c_reset}\n")



