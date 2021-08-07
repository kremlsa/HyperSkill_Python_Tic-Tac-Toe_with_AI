# write your code here
import copy
import random

# user_field = list("         ")
player = "X"


def print_field():
    print("---------")
    print("|" , user_field[0] , user_field[1] , user_field[2] , "|")
    print("|" , user_field[3] , user_field[4] , user_field[5] , "|")
    print("|" , user_field[6] , user_field[7] , user_field[8] , "|")
    print("---------")


def is_player_win(user_field_ , letter_):
    if user_field_[0] == letter_ and user_field_[1] == letter_ and user_field_[2] == letter_:
        return True
    if user_field_[3] == letter_ and user_field_[4] == letter_ and user_field_[5] == letter_:
        return True
    if user_field_[6] == letter_ and user_field_[7] == letter_ and user_field_[8] == letter_:
        return True
    if user_field_[0] == letter_ and user_field_[3] == letter_ and user_field_[6] == letter_:
        return True
    if user_field_[1] == letter_ and user_field_[4] == letter_ and user_field_[7] == letter_:
        return True
    if user_field_[2] == letter_ and user_field_[5] == letter_ and user_field_[8] == letter_:
        return True
    if user_field_[0] == letter_ and user_field_[4] == letter_ and user_field_[8] == letter_:
        return True
    if user_field_[2] == letter_ and user_field_[4] == letter_ and user_field_[6] == letter_:
        return True
    return False


def count_letter(letter , user_field_):
    return len([i for i in user_field_ if i == letter])


def is_impossible(user_field_):
    if count_letter("X" , user_field_) > count_letter("O" , user_field_) + 1:
        return True
    if count_letter("O" , user_field_) > count_letter("X" , user_field_) + 1:
        return True
    if is_player_win("X" , user_field_) and is_player_win("O" , user_field_):
        return True


def is_draw(user_field_):
    if count_letter(" " , user_field_) == 0:
        return True


def convert_xy(x , y):
    return int((x - 1) * 3 + y) - 1


def make_move(letter_):
    global user_field
    while True:
        print("Enter the coordinates: ")
        option = input()
        if any([x.isalpha() for x in option.split()]):
            print("You should enter numbers!")
            continue
        x , y = option.split()
        if int(x) < 0 or int(x) > 3 or int(y) < 0 or int(y) > 3:
            print("Coordinates should be from 1 to 3!")
        elif user_field[convert_xy(int(x) , int(y))] != " ":
            print("This cell is occupied! Choose another one!")
            continue
        else:
            user_field[convert_xy(int(x) , int(y))] = letter_
            break


def computer_easy_move(letter_):
    global user_field
    available_moves_ = []
    for index_ in range(len(user_field)):
        if user_field[index_] == ' ':
            available_moves_.append(index_)
    user_field[random.choice(available_moves_)] = letter_


def computer_medium_move(letter_):
    global user_field
    available_moves_ = []
    for index_ in range(len(user_field)):
        if user_field[index_] == ' ':
            available_moves_.append(index_)
    for move_ in available_moves_:
        temp_field = copy.copy(user_field)
        temp_field[move_] = "O" if letter_ == "X" else "X"
        if is_player_win(temp_field , "O" if letter_ == "X" else "X"):
            user_field[move_] = letter_
            return
        temp_field = copy.copy(user_field)
        temp_field[move_] = letter_
        if is_player_win(temp_field , letter_):
            user_field[move_] = letter_
            return
    user_field[random.choice(available_moves_)] = letter_


def minimax(depth_ , letter_ , field_):
    best_score = -10000 if letter_ == computer_letter else 10000
    available_moves_ = []
    for index_ in range(len(field_)):
        if field_[index_] == ' ':
            available_moves_.append(index_)
    best_move = -1
    if len(available_moves_) == 0 or depth_ == 0:
        best_score = evaluate(field_)
        pass
    else:
        for move_ in available_moves_:
            field_[move_] = letter_
            if letter_ == computer_letter:
                current_score = minimax(depth_ - 1 , player_letter , field_)[0]
                if current_score > best_score:
                    best_score = current_score
                    best_move = move_
            else:
                current_score = minimax(depth_ - 1 , computer_letter , field_)[0]
                if current_score < best_score:
                    best_score = current_score
                    best_move = move_
            field_[move_] = " "
    return [best_score , best_move]


def evaluate(field_):
    score_ = 0
    score_ += evaluate_line(0 , 1 , 2 , field_)
    score_ += evaluate_line(3 , 4 , 5 , field_)
    score_ += evaluate_line(6 , 7 , 8 , field_)
    score_ += evaluate_line(0 , 3 , 6 , field_)
    score_ += evaluate_line(1 , 4 , 7 , field_)
    score_ += evaluate_line(2 , 5 , 8 , field_)
    score_ += evaluate_line(0 , 4 , 8 , field_)
    score_ += evaluate_line(2 , 4 , 6 , field_)
    return score_


def evaluate_line(index_1 , index_2 , index_3 , field_):
    score_ = 0
    # First cell
    if field_[index_1] == computer_letter:
        score_ = 1
    elif field_[index_1] == player_letter:
        score_ = -1

    # Second cell
    if field_[index_2] == computer_letter:
        if score_ == 1:
            score_ = 10
        elif score_ == -1:
            return 0
        else:
            score_ = 1
    elif field_[index_2] == player_letter:
        if score_ == -1:
            score_ = -10
        elif score_ == 1:
            return 0
        else:
            score_ = -1

    # Third cell
    if field_[index_3] == computer_letter:
        if score_ > 0:
            score_ *= 10
        elif score_ < 0:
            return 0
        else:
            score_ = 1
    elif field_[index_3] == player_letter:
        if score_ < 0:
            score_ *= 10
        elif score_ > 1:
            return 0
        else:
            score_ = -1

    return score_


def computer_hard_move(letter_):
    move_ = minimax(2 , letter_ , copy.copy(user_field))
    user_field[move_[1]] = letter_


def computer_move(mode_ , letter_):
    if mode_ == "easy":
        computer_easy_move(letter_)
        print('Making move level "easy"')
        return
    if mode_ == "medium":
        computer_medium_move(letter_)
        print('Making move level "medium"')
        return
    if mode_ == "hard":
        computer_hard_move(letter_)
        print('Making move level "hard"')
        return


computer_letter , player_letter = "" , ""
modes = ["user" , "easy" , "medium" , "hard"]
while True:
    user_field = list("         ")
    print("Input command:")
    mode = input()
    if mode == "exit":
        break
    elif mode.split()[0] != "start":
        print("Bad parameters!")
        continue
    elif len(mode.split()) != 3:
        print("Bad parameters!")
        continue
    elif mode.split()[1] not in modes or mode.split()[2] not in modes:
        print("Bad parameters!")
        continue
    x_mode = mode.split()[1]
    o_mode = mode.split()[2]
    if mode.split()[1] == "user":
        computer_letter , player_letter = "O" , "X"
    else:
        computer_letter , player_letter = "X" , "O"
    print_field()
    while True:
        if x_mode == "user" and player == "X":
            make_move(player)
            print_field()
        elif x_mode != "user" and player == "X":
            computer_move(x_mode , player)
            print_field()
        elif o_mode == "user" and player == "O":
            make_move(player)
            print_field()
        elif o_mode != "user" and player == "O":
            computer_move(o_mode , player)
            print_field()
        if is_player_win(user_field , player):
            print(player , "wins")
            break
        if is_draw(user_field):
            print("Draw")
            break
        player = "O" if player == "X" else "X"
