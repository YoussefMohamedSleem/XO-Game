import tkinter as tk
from tkinter import messagebox
import random

root = tk.Tk()
root.title("Tic Tac Toe")
root.geometry("600x700")
root.configure(bg="#2E2E2E")

WHITE = "#FFFFFF"
X_COLOR = "#FF6347"
O_COLOR = "#3CB371"
LINE_COLOR = "#1CAAFF"
BG_COLOR = "#2E2E2E"
BUTTON_COLOR = "#444"
HIGHLIGHT_COLOR = "#00CED1"

board = [""] * 9
current_player = "X"
game_mode = ""
game_running = True
score = {"X": 0, "O": 0}

canvas = tk.Canvas(root, width=600, height=600, bg=BG_COLOR, highlightthickness=0)
canvas.pack()

status_label = tk.Label(root, text="", font=("Arial", 20), bg=BG_COLOR, fg=WHITE)
status_label.pack(pady=5)

selection_frame = tk.Frame(root, bg=BG_COLOR)
selection_frame.place(relx=0.5, rely=0.5, anchor="center")

select_label = tk.Label(selection_frame, text="اختر وضع اللعبة", font=("Arial", 20, "bold"), bg=BG_COLOR, fg=HIGHLIGHT_COLOR)
select_label.pack(pady=10)

mode_var = tk.StringVar(value="pvp")
tk.Radiobutton(selection_frame, text="Player vs Player", variable=mode_var, value="pvp", font=("Arial", 16), bg=BG_COLOR, fg=WHITE, selectcolor=BUTTON_COLOR).pack(pady=5, anchor="w")
tk.Radiobutton(selection_frame, text="Player vs AI", variable=mode_var, value="pvai", font=("Arial", 16), bg=BG_COLOR, fg=WHITE, selectcolor=BUTTON_COLOR).pack(pady=5, anchor="w")
tk.Radiobutton(selection_frame, text="AI vs AI", variable=mode_var, value="aivai", font=("Arial", 16), bg=BG_COLOR, fg=WHITE, selectcolor=BUTTON_COLOR).pack(pady=5, anchor="w")

start_btn = tk.Button(selection_frame, text="ابدأ اللعبة", font=("Arial", 16, "bold"), bg=HIGHLIGHT_COLOR, fg=WHITE, command=lambda: [selection_frame.pack_forget(), selection_frame.place_forget(), start_game()])
start_btn.pack(pady=15)

def draw_board():
    canvas.delete("all")
    for i in range(1, 3):
        canvas.create_line(0, i * 200, 600, i * 200, fill=LINE_COLOR, width=3)
        canvas.create_line(i * 200, 0, i * 200, 600, fill=LINE_COLOR, width=3)
    for i in range(9):
        x = (i % 3) * 200 + 100
        y = (i // 3) * 200 + 100
        if board[i] == "X":
            canvas.create_text(x, y, text="X", font=("Arial", 60), fill=X_COLOR)
        elif board[i] == "O":
            canvas.create_text(x, y, text="O", font=("Arial", 60), fill=O_COLOR)

def make_move(i):
    global current_player, game_running
    if board[i] == "" and game_running:
        board[i] = current_player
        current_player = "O" if current_player == "X" else "X"
        draw_board()
        winner = check_winner()
        if winner:
            end_game(winner)
        elif game_mode == "pvai" and current_player == "O":
            root.after(500, ai_turn)
        elif game_mode == "aivai" and current_player == "O":
            root.after(500, ai_turn)

def check_winner():
    wins = [(0,1,2), (3,4,5), (6,7,8),
            (0,3,6), (1,4,7), (2,5,8),
            (0,4,8), (2,4,6)]
    for a, b, c in wins:
        if board[a] == board[b] == board[c] != "":
            return board[a]
    if "" not in board:
        return "Draw"
    return None

def end_game(winner):
    global game_running
    game_running = False
    if winner == "Draw":
        status_label.config(text="تعادل!")
        messagebox.showinfo("انتهت اللعبة", "تعادل!")
    else:
        score[winner] += 1
        status_label.config(text=f"فاز اللاعب {winner} | X: {score['X']} - O: {score['O']}")
        messagebox.showinfo("انتهت اللعبة", f"اللاعب {winner} فاز!")
    restart_button.pack(pady=10)

def minimax(board, depth, is_maximizing):
    winner = check_winner()
    if winner == "X":
        return -10
    elif winner == "O":
        return 10
    elif winner == "Draw":
        return 0

    if is_maximizing:
        best = -float('inf')
        for i in range(9):
            if board[i] == "":
                board[i] = "O"
                best = max(best, minimax(board, depth + 1, False))
                board[i] = ""
        return best
    else:
        best = float('inf')
        for i in range(9):
            if board[i] == "":
                board[i] = "X"
                best = min(best, minimax(board, depth + 1, True))
                board[i] = ""
        return best

def best_move():
    best_value = -float('inf')
    move = -1
    for i in range(9):
        if board[i] == "":
            board[i] = "O"
            move_value = minimax(board, 0, False)
            board[i] = ""
            if move_value > best_value:
                best_value = move_value
                move = i
    return move

def ai_turn():
    move = best_move()
    make_move(move)

def ai_vs_ai():
    if not game_running:
        return
    ai_turn()
    if game_running:
        root.after(700, ai_turn)
        root.after(1400, ai_turn)

def start_game():
    global game_mode, board, current_player, game_running
    game_mode = mode_var.get()
    board = [""] * 9
    current_player = "X"
    game_running = True
    status_label.config(text="اللاعب X يبدأ")
    restart_button.pack_forget()
    draw_board()
    if game_mode == "aivai":
        ai_vs_ai()

def reset_game():
    start_game()

def on_click(event):
    if not game_running:
        return
    x, y = event.x, event.y
    row, col = y // 200, x // 200
    index = row * 3 + col
    if game_mode == "pvp" or (game_mode == "pvai" and current_player == "X"):
        make_move(index)

canvas.bind("<Button-1>", on_click)

restart_button = tk.Button(root, text="إعادة اللعب", font=("Arial", 14), bg=WHITE, command=reset_game)
restart_button.pack_forget()

root.mainloop()