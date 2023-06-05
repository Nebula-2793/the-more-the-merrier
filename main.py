import reqFunctions as reqFn

path = r"data.txt"

list_serials = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
list_obj_questions = []
dict_score = {}
num_max_qs = 0
num_qs = -1
player1 = ""
player2 = ""
num_turns_each_q = 4 #must be even

lines = reqFn.read_file(path)
list_obj_questions = reqFn.read_data(list_obj_questions, lines)
num_max_qs = len(list_obj_questions)

num_qs, player1, player2, list_obj_questions = reqFn.ask_quiz_details(num_qs, 
player1, player2, list_obj_questions, num_max_qs)
dict_score, player1, player2 = reqFn.actual_quiz(dict_score, player1, player2, 
list_obj_questions, list_serials, num_turns_each_q)
reqFn.decide_winner(dict_score, player1, player2)
