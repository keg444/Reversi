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
    
    # 石おけるかチェック
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
                    
                
    def _display(self, valid=None):
        print("-" * 30)
        print("   0  1  2  3  4  5  6  7")
        for i in range(tablesize):
            print(f"{i}", end="  ")
            for j in range(tablesize):
                if self.cell[i][j] == blank:
                    if valid and (i, j) in valid:
                        print("?", end="  ")
                    else:
                        print("-", end="  ")
                elif self.cell[i][j] == white:
                    print("○", end="  ")
                else:
                    print("●", end="  ")
            print()
        print("-" * 30)
    
    # 合法手を返す
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
    
    # def _cpu(self, valid):
    #     if not valid:
            
    def _skip(self, current_player, pass_count):
        pass_count = 0
        self.current = -self.current
        opp_valid = self._get_move()
        # 合法手がない
        if not opp_valid:
            print("Skipped: Both has no valid moves\n")
            return True, pass_count
        print(f"Skipped: {current_player} has no valid moves\n")
        pass_count += 1
        
        if pass_count == 2:
            print("Skipped: Both has no valid moves\n")
            return True, pass_count
        self.current = -self.current
        return True, pass_count
    
    def _score(self, black_score, white_score):
        score_count_b = 0
        score_count_w = 0
        draw_count = 0
        if black_score > white_score:
            print("● Black Win")
            score_count_b += 1
        elif black_score < white_score:
            print("○ White Win")
            score_count_w += 1
        else:
            print("Draw")
            draw_count += 1
        print(f"Score: ●{black_score} - ○{white_score}")
        print(f"Total score: ●win {score_count_b} - ○win {score_count_w} - draw {draw_count}")


        
    
    def play(self):
        while True:
            print("\n===== New Game =====")
            self.__init__()
            while True:
                valid = self._get_move()
                self._display(valid)
                current_p = self.current
                
                # 盤面全埋まり
                if np.all(self.cell != blank):
                    print("The board is full")
                    break
                
                # 合法手がない場合
                if not valid:
                    game_over, pass_count = self._skip(current_p, pass_count)
                    if game_over:
                        break
                    continue
                pass_count = 0
                
                # 入力
                while True:
                    print(f"\nturn count: {self.turn}")
                    print(f"\n↓ Waiting for player{"●" if self.current == black else "○"} input... (ex: 34)")
                    user_input = input("press \"q\" to quit the game\n(i j): ").strip().lower()
                    if user_input == "q" or user_input == "Q":
                        print("\n===== Quitted the game =====")
                        sys.exit()
                    ####### おまけ #########
                    elif user_input == "full black":
                        self._fastestB()
                    elif user_input == "full white":
                        self._fastestW()
                    #################
                    try:
                        # y, x = map(int, user_input.split())
                        # put = (y, x)
                        y = int(user_input[0])
                        x = int(user_input[1])
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
                self.turn += 1
            
            # スコア表示
            self._score(np.sum(self.cell == black), np.sum(self.cell == white))
            
            # 再戦確認
            again = input("\n Play again? (y/n)").strip().lower()
            if again != "y":
                print("===== ｵﾜﾀ ====")
                break
        
if __name__ == "__main__":
    Reversi().play()

# gitに上げられん


