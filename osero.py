import numpy as np
import sys

white = 1   # ○
black = -1  # ●
blank = 0
tablesize = 8

class Reversi(object):
    
    def __init__(self):
        self.cell = np.zeros((tablesize, tablesize))
        self.cell = self.cell.astype(int)
        self.cell[3][3] = self.cell[4][4] = white
        self.cell[3][4] = self.cell[4][3] = black
        self.current = black
        self.dx = [-1, 0, 1]
        self.dy = [-1, 0, 1]
        self.turn = 1
        
    def _check(self, board, put, flip=False):
        y, x = put
        player = self.current
        if not (0 <= y < tablesize and 0 <= x < tablesize) or board[y][x] != blank:
            return False
        
        found = False
        
        for dy in self.dy:
            for dx in self.dx:
                if dy == 0 and dx == 0:
                    continue
                
                ny, nx = y+dy, x+dx
                flipped = []
                
                while(0 <= ny < tablesize and 0 <= nx < tablesize) and board[ny][nx] == -player:
                    flipped.append((ny, nx))
                    ny += dy
                    nx += dx
                
                if len(flipped) > 0 and (0 <= ny < tablesize and 0 <= nx < tablesize) and board[ny][nx] == player:
                    found = True
                    if flip:
                        board[y][x] = player
                        for fy, fx in flipped:
                            board[fy][fx] = player
        return found
                    
                
    def _display(self):
        print("-" * 30)
        print("   0  1  2  3  4  5  6  7")
        for i in range(tablesize):
            print(f"{i}", end="  ")
            for j in range(tablesize):
                if self.cell[i][j] == 0:
                    print("-", end="  ")
                elif self.cell[i][j] == 1:
                    print("○", end="  ")
                else:
                    print("●", end="  ")
            print()
        print("-" * 30)
    
    def _get_move(self):
        valid = []
        for r in range(tablesize):
            for c in range(tablesize):
                put = (r, c)
                if self._check(self.cell, put, flip=False):
                    valid.append(put)
        return valid
    
    def _fastestB(self):   # 黒が埋まる
        print("(first:black)\n45 → 55 → 54 → 35 → 24 → 13 → 23 → 53 → 32 → 31")
    def _fastestW(self):   # 白が埋まる
        print("(first:black)\n53 → 34 → 23 → 52 → 45 → 54 → 63 → 44 → 41")
    
    def play(self):
        score_count_b = 0
        score_count_w = 0
        draw_count = 0
        pass_count = 0
        
        while True:
            print("\n===== New Game =====")
            self.__init__()
            while True:
                self._display()
                valid = self._get_move()
                current_p = self.current
                
                if np.all(self.cell != blank):
                    print("The board is full")
                    break
                
                if not valid:
                    self.current = -self.current
                    opp_valid = self._get_move()
                    self.current = -self.current
                    if not opp_valid:
                        print("Skipped: Both has no valid moves")
                        break
                    print(f"Skipped: {current_p} has no valid moves")
                    pass_count += 1
                    if pass_count == 2:
                        print("Skipped Both has no valid moves")
                        break
                    self.current = -self.current
                    continue
                
                while True:
                    print(f"\n↓ Waiting for player{"●" if self.current == black else "○"} input... (ex: 3 4)")
                    user_input = input("press \"q\" to quit the game\n(i j): ").strip().lower()
                    if user_input == "q" or user_input == "Q":
                        print("\n===== Quitted the game =====")
                        sys.exit()
                    elif user_input == "full black":
                        self._fastestB()
                    elif user_input == "full white":
                        self._fastestW()
                    try:
                        y, x = map(int, user_input.split())
                        put = (y, x)
                        if put in valid:
                            print(f"\nplayer{"●" if self.current == black else "○"} (i j): {put}")
                            break
                        else:
                            print("\n!!!!! Cannot put this position !!!!!")
                    except:
                        print("\n!!!!! Invalid input: Enter the (i j) ex: 3 4 !!!!!")
                self._check(self.cell, put, flip=True)
                self.current = -self.current
            
            b_score = np.sum(self.cell == black)
            w_score = np.sum(self.cell == white)
            if b_score > w_score:
                print("● Black Win")
                score_count_b += 1
            elif b_score < w_score:
                print("○ White Win")
                score_count_w += 1
            else:
                print("Draw")
                draw_count += 1
            print(f"Score: ●{b_score} - ○{w_score}")
            print(f"Total score: ●win {score_count_b} - ○win {score_count_w} - draw {draw_count}")
            
            again = input("\n Play again? (y/n)").strip().lower()
            if again != "y":
                print("===== ｵﾜﾀ ====")
                break
        
if __name__ == "__main__":
    Reversi().play()


