import tkinter as tk
from tkinter import messagebox
from Game import Game
from Errors import *

##### FLOWER BOX #####
'''
# Code to make widget stretchable
top.rowconfigure(0, weight=1)
top.columnconfigure(0, weight=1)
self.rowconfigure(0, weight=1)
self.columnconfigure(0, weight=1)
'''
#####  END BOX   #####

class App(tk.Frame):
    # Constructor
    def __init__(self, master=None):
        # Init game instance
        self.game = Game()
        
        # Init App window
        tk.Frame.__init__(self, master)
        self.grid()
        
        # Init all necesary vars for UI
        self.OUTLINE_CLSOE = 1
        self.OUTLINE_FAR = 601
        self.boardsize_v = tk.StringVar()
        self.gamemode_v = tk.IntVar()
        self.playermode_v = tk.IntVar()
        self.piece_v = tk.StringVar()
        self.p1Score_v = tk.IntVar()
        self.p2Score_v = tk.IntVar()
        self.turn_v = tk.StringVar()
        self.reg = self.register(self.boardsize_callback)
        self.border_id = None
        self.board_v = {}
        self.pieces_v = {}
        
        # Pull default values for UI vars
        self.pull_settings()
        self.pull_scores()
        self.pull_turn()
        
        # Init widgets
        self.create_widgets() 
        
        # Init default board
        self.create_board() 
    
    # Exception handler function
    def excp_handler(self, error):
        try:
            raise error
        except InvalidBoardSizeExcp as ibse:
            self.message("Invalid board size! (3-20)")
        except ValueError as ve:
            self.message("Please enter a board size (3-20)")
        except LogicalExcp as le:
            self.message(le)
        except:
            self.quit()
    
    # Board size entry validator
    def boardsize_callback(self, input):
        if input.isdigit():
            return True
        elif input == '':
            return True
        else:
            return False
    
    # Instantiates all widgets for game UI
    def create_widgets(self):
        
        # Row 0, col 0: Game title
        self.title = tk.Label(self, text='SOS', font=('Arial', -40))
        self.title.grid(row=0, column=0, pady=3)
        
        #region Row 1, col 0: new game settings pane
        self.newgameSettings = tk.Frame(self)
        self.newgameSettings.grid(row=1, column=0)
        
        self.boardSizeText = tk.Label(self.newgameSettings, text='Board size:')
        self.boardSizeText.grid(row=0, column=0)
        self.boardSizeField = tk.Entry(self.newgameSettings, textvariable=self.boardsize_v, width= 5, validate='key', validatecommand=(self.reg, '%P'))
        self.boardSizeField.grid(row=0,column=1)
        
        self.gamemodeLabel = tk.Label(self.newgameSettings, text='Game mode:')
        self.gamemodeLabel.grid(row=1, column=0)
        self.gamemodeSimple = tk.Radiobutton(self.newgameSettings, text='Simple', variable=self.gamemode_v, value=0)
        self.gamemodeGeneral = tk.Radiobutton(self.newgameSettings, text='General', variable=self.gamemode_v, value=1)
        self.gamemodeSimple.grid(row=2, column=0, columnspan=2)
        self.gamemodeGeneral.grid(row=3, column=0, columnspan=2)
        
        self.playermodeLabel = tk.Label(self.newgameSettings, text='Player mode:')
        self.playermodeLabel.grid(row=4, column=0)
        self.playermodePvp = tk.Radiobutton(self.newgameSettings, text='User v User', variable=self.playermode_v, value=0)
        self.playermodePvc = tk.Radiobutton(self.newgameSettings, text='User v COM', variable=self.playermode_v, value=1)
        self.playermodePvp.grid(row=5, column=0, columnspan=2)
        self.playermodePvc.grid(row=6, column=0, columnspan=2)
        #endregion
        
        # Row 2, col 0: Start new game button
        self.startGameBtn = tk.Button(self, text="Start new game", command=self.new_game)
        self.startGameBtn.grid(row=3, column=0, pady=3)
        
        # Row 1, col 1: game window
        self.gameWindow = tk.Canvas(self, height=self.OUTLINE_FAR, width=self.OUTLINE_FAR)
        self.gameWindow.grid(row=1, column=1, padx=1, pady=1)
        
        # Row 0, col 2: player turn
        self.turnFrame = tk.Frame(self)
        self.turnFrame.grid(row=0, column=2)
        self.turnLabel = tk.Label(self.turnFrame, text='Turn: ', font=('Arial', -20))
        self.turnLabel.grid(row=0, column=0)
        self.currentTurn = tk.Label(self.turnFrame, textvariable=self.turn_v, font=('Arial', -20))
        self.currentTurn.grid(row=0, column=1)

        #region Row 1, col 2: current game settings pane
        self.currgameSettings = tk.Frame(self)
        self.currgameSettings.grid(row=1, column=2)
        
        self.piecetypeLabel = tk.Label(self.currgameSettings, text='Piece type:')
        self.piecetypeLabel.grid(row=0, column=0)
        self.pieceS = tk.Radiobutton(self.currgameSettings, text='S', variable=self.piece_v, value='S')
        self.pieceO = tk.Radiobutton(self.currgameSettings, text='O', variable=self.piece_v, value='O')
        self.pieceS.grid(row=1, column=0, columnspan=2)
        self.pieceO.grid(row=2, column=0, columnspan=2)
        
        self.scoreLabel = tk.Label(self.currgameSettings, text='Score:')
        self.scoreLabel.grid(row=3,column=0)
        self.p1Label = tk.Label(self.currgameSettings, text='P1')
        self.p2Label = tk.Label(self.currgameSettings, text='P2')
        self.p1Score = tk.Label(self.currgameSettings, textvariable=self.p1Score_v)
        self.p2Score = tk.Label(self.currgameSettings, textvariable=self.p2Score_v)
        self.p1Label.grid(row=4, column=0)
        self.p1Score.grid(row=4, column=1)
        self.p2Label.grid(row=5, column=0)
        self.p2Score.grid(row=5, column=1)
        #endregion

    #region Puller funcs
    #Pulls settings information from Game class
    def pull_settings(self):
        self.boardsize_v.set(self.game.get_board_size())
        self.gamemode_v.set(self.game.get_gametype())
        self.playermode_v.set(self.game.get_playertype())
        self.piece_v.set(self.game.get_piece())
        
    # Pulls current scores from Game class
    def pull_scores(self):
        self.p1Score_v.set(self.game.get_p1_score())
        self.p2Score_v.set(self.game.get_p2_score())
    
    # Pull current turn into UI var to output to the screen
    def pull_turn(self):
        t = self.game.get_turn()
        match t:
            case 1:
                self.turn_v.set(f'Player {t}')
            case 2:
                self.turn_v.set(f'Player {t}')
    #endregion
    
    #region Sender funcs
    # Send UI piece var to Game var
    def send_piece(self):
        self.game.set_piece(self.piece_v.get())
        return True
    
    # Send UI settings vars to Game vars
    def send_settings(self):
        self.game.set_gametype(self.gamemode_v.get())
        self.game.set_playertype(self.playermode_v.get())
        
        try:
            localint = int(self.boardsize_v.get())
            if localint < 3 or localint > 20:
                raise InvalidBoardSizeExcp
            else:
                self.game.set_board_size(localint)
        except Exception as e:
            self.excp_handler(e)
            return False
        return True
    #endregion
    
    #region Updater funcs
    # Updates anything needed to be updated, used at runtime
    def update_all(self):
        self.update_playerdata()
        self.update_widget(self.p1Score, self.p1Score_v)
        self.update_widget(self.p2Score, self.p2Score_v)
        
    # Update a widget w with a variable var every 100ms
    def update_widget(self, w, var):
        w.config(text=var.get())
        self.after(100, self.update_widget, w, var)
    
    # Updates player data vars every 50ms
    def update_playerdata(self):
        self.pull_scores()
        self.pull_turn()
        self.after(50, self.update_playerdata)
    #endregion
    
    #region Board-related functions
    # Create a game board in canvas
    def create_board(self):
        self.clear_board()
        bs = self.game.get_board_size()
        divisor = (self.OUTLINE_FAR - self.OUTLINE_CLSOE) / bs 
        tlc_x = self.OUTLINE_CLSOE
        brc_x = divisor
        tlc_y = tlc_x
        brc_y = brc_x
        
        #print(divisor)
        
        # Create board rectangles
        for r in range(bs):
            for c in range(bs):
                self.board_v[self.gameWindow.create_rectangle(tlc_x, tlc_y, brc_x, brc_y, tags='clickable')] = (r,c)
                tlc_x += divisor
                brc_x += divisor 
            tlc_x = self.OUTLINE_CLSOE
            brc_x = divisor
            tlc_y = tlc_x + (divisor * (r + 1))
            brc_y = brc_x + (divisor * (r + 1))
        
        
        if self.game.is_active():
            self.gameWindow.bind('<Button-1>', self.clicked)
        else:
            self.piece_v.set('S')
            self.update_board(self.border_id + 4)
            self.piece_v.set('O')
            self.update_board(self.border_id + 5)
            self.piece_v.set('S')
            self.update_board(self.border_id + 6)
        return
    
    # Clears game board canvas and dict and adds a border
    def clear_board(self):
        self.gameWindow.delete('all')
        self.board_v.clear()
        self.pieces_v.clear()
        self.border_id = self.gameWindow.create_rectangle(self.OUTLINE_CLSOE, self.OUTLINE_CLSOE, self.OUTLINE_FAR, self.OUTLINE_FAR)
        
    # Update UI game board and Game board when a valid move occurs
    def update_board(self, item):
        gb = self.game.get_board()
        coordr, coordc = self.board_v[item]
        self.send_piece()
        
        if gb[coordr][coordc] != ' ':
            return
        else:            
            # Prepare to draw appropriate letter to screen
            x1, y1, x2, y2 = self.gameWindow.coords(item)
            size = int((y2 - y1) * 0.8) 
            midx = (x1 + x2) / 2
            midy = (y1 + y2) / 2
            cfont = ('DejaVu Sans', -size)
            if self.game.get_turn() == 1:
                color = 'red'
            else:
                color = 'blue'
            self.pieces_v[(coordr, coordc)] = self.gameWindow.create_text(midx, midy, text=self.piece_v.get(), font=cfont, fill=color)
            
            # Once drawn, update Game class w/ appropriate move
            self.game.move(coordr, coordc)
        return
    
    # TODO: implement function to draw line across item1 and item2
    def draw_line(self, item1, item2):
        return
    #endregion
    
    # Runs when an object is clicked
    def clicked(self, event):        
        clicked_item = self.gameWindow.find_closest(event.x, event.y)[0]

        if clicked_item:
            if 'clickable' not in self.gameWindow.gettags(clicked_item):
                return
            else:
                self.update_board(clicked_item)
        else:
            try:
                raise LogicalExcp("ERROR: Clickable item not found.")
            except Exception as e:
                self.excp_handler(e)
                return
    
    # Ran when new game button is pressed, used for a debug layer currently
    def new_game(self):
        print('In new game UI func')
        
        if not self.send_settings():
            return
        else:
            self.game.new_game()
            
        print('Out of Game new game func')

        self.create_board()
    
    # Shows message box to the user with message m
    def message(self, m):
        messagebox.showinfo(message=m, title="SOS")
        return
        



if __name__ == '__main__':
    app = App()
    app.master.title('SOS')
    app.update_all()
    app.mainloop()