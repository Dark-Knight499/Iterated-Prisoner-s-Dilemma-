i = 0
initial_move = "c"
def strategy(opponent_move):
    global i
    i=i+1
    return "c" if i%2==0 else "d"