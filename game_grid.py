import stddraw # the stddraw module is used as a basic graphics library
from color import Color # used for coloring the game grid
import numpy as np # fundamental Python module for scientific computing
import time
# Class used for modelling the game grid
class GameGrid:
	# Constructor for creating the game grid based on the given arguments
   def __init__(self, grid_h, grid_w):
      # set the dimensions of the game grid as the given arguments
      self.grid_height = grid_h
      self.grid_width = grid_w
      # create the tile matrix to store the tiles placed on the game grid
      self.tile_matrix = np.full((grid_h, grid_w), None)
      # the tetromino that is currently being moved on the game grid
      self.current_tetromino = None
      self.next_tetromino = None
      # game_over flag shows whether the game is over/completed or not
      self.game_over = False
      self.delta_time = 250
      # set the color used for the empty grid cells

      self.empty_cell_color = Color(205, 192, 180) #CHANGED Color(42, 69, 99)
      # set the colors used for the grid lines and the grid boundaries
      self.line_color = Color(147, 133, 120)
      self.boundary_color = Color(147, 133, 120)
      # thickness values used for the grid lines and the grid boundaries 
      self.line_thickness = 0.002
      self.box_thickness = 8 * self.line_thickness
      #sum score
      self.sum = 0
   # Method used for displaying the game grid
   def display(self):
      # clear the background canvas to empty_cell_color
      stddraw.clear(self.empty_cell_color)

      # SCORE
      stddraw.setFontSize(28)
      stddraw.setPenColor(stddraw.WHITE)
      stddraw.boldText(self.grid_width + 2, self.grid_height - 1, "SCORE")
      stddraw.rectangle(self.grid_width, self.grid_height - 3.5, 4, 2)
      stddraw.boldText(self.grid_width+2,self.grid_height-2.5,str(self.sum))

      # Controls
      stddraw.setFontSize(18)
      stddraw.setPenColor(stddraw.DARK_GRAY)
      stddraw.boldText(self.grid_width + 2, self.grid_height - 6, "Controls")

      stddraw.setFontSize(12)
      stddraw.boldText(self.grid_width + 2, self.grid_height - 7, "← Left Key the tetromino left by on")
      stddraw.boldText(self.grid_width + 2, self.grid_height - 7.5, "→ Right Key the tetro right by on")
      stddraw.boldText(self.grid_width + 2, self.grid_height - 8, "P to Pause")
      stddraw.boldText(self.grid_width + 2, self.grid_height - 8.5, "E to Rotate")
      stddraw.boldText(self.grid_width + 2, self.grid_height - 9, "W to Faster Down")
      stddraw.boldText(self.grid_width + 2, self.grid_height - 9.5, "S to Slower Down")
      stddraw.boldText(self.grid_width + 2, self.grid_height - 10, "R to Restrat ")



      stddraw.setFontSize(24)
      stddraw.setPenColor(stddraw.WHITE)
      stddraw.text(self.grid_width+2, self.grid_height-12 , "next")
      stddraw.rectangle(self.grid_width,self.grid_height-18,4,5)
      # draw the game grid
      self.next_tetromino.draw_dummy()
      self.draw_grid()
      # draw the current (active) tetromino
      if self.current_tetromino != None:
         self.current_tetromino.draw()
      # draw a box around the game grid 
      self.draw_boundaries()
      # show the resulting drawing with a pause duration = 250 ms
      stddraw.show(self.delta_time)
         
   # Method for drawing the cells and the lines of the grid
   def draw_grid(self):
      # draw each cell of the game grid
      for row in range(self.grid_height):
         for col in range(self.grid_width):
            # draw the tile if the grid cell is occupied by a tile
            if self.tile_matrix[row][col] != None:
               self.tile_matrix[row][col].draw() 
      # draw the inner lines of the grid
      stddraw.setPenColor(self.line_color)
      stddraw.setPenRadius(self.line_thickness)
      # x and y ranges for the game grid
      start_x, end_x = -0.5, self.grid_width - 0.5
      start_y, end_y = -0.5, self.grid_height - 0.5
      for x in np.arange(start_x + 1, end_x, 1):  # vertical inner lines
         stddraw.line(x, start_y, x, end_y)
      for y in np.arange(start_y + 1, end_y, 1):  # horizontal inner lines
         stddraw.line(start_x, y, end_x, y)
      stddraw.setPenRadius()  # reset the pen radius to its default value            
      
   # Method for drawing the boundaries around the game grid 
   def draw_boundaries(self):
      # draw a bounding box around the game grid as a rectangle
      stddraw.setPenColor(self.boundary_color)  # using boundary_color
      # set the pen radius as box_thickness (half of this thickness is visible 
      # for the bounding box as its lines lie on the boundaries of the canvas)
      stddraw.setPenRadius(self.box_thickness)
      # coordinates of the bottom left corner of the game grid
      pos_x, pos_y = -0.5, -0.5
      stddraw.rectangle(pos_x, pos_y, self.grid_width, self.grid_height)
      stddraw.setPenRadius()  # reset the pen radius to its default value

   # Method used for checking whether the grid cell with given row and column 
   # indexes is occupied by a tile or empty
   def is_occupied(self, row, col):
      # return False if the cell is out of the grid
      if not self.is_inside(row, col):
         return False
      # the cell is occupied by a tile if it is not None
      return self.tile_matrix[row][col] != None
      
   # Method used for checking whether the cell with given row and column indexes 
   # is inside the game grid or not
   def is_inside(self, row, col):
      if row < 0 or row >= self.grid_height:
         return False
      if col < 0 or col >= self.grid_width:
         return False
      return True

   # Method for updating the game grid by placing the given tiles of a stopped 
   # tetromino and checking if the game is over due to having tiles above the 
   # topmost game grid row. The method returns True when the game is over and
   # False otherwise.
   def update_grid(self, tiles_to_place):
      # place all the tiles of the stopped tetromino onto the game grid

      n_rows, n_cols = len(tiles_to_place), len(tiles_to_place[0])
      for col in range(n_cols):
         for row in range(n_rows):            
            # place each occupied tile onto the game grid
            if tiles_to_place[row][col] != None:
               pos = tiles_to_place[row][col].get_position()
               if self.is_inside(pos.y, pos.x):
                  self.tile_matrix[pos.y][pos.x] = tiles_to_place[row][col]
               # the game is over if any placed tile is out of the game grid
               else:
                  self.game_over = True
      # return the game_over flag

      #check on each iteration
      self.delete_tile()

      self.check_grid()
      self.merge()
      return self.game_over

   def check_grid(self):
      print(self.tile_matrix)
      for row in range(self.grid_width):
         if None not in self.tile_matrix[row]:
            self.delete_row(row)
            self.move_row(row)
            self.check_grid()



   def delete_row(self,row):
      print("----------BEFORE----------")
      print(self.tile_matrix)
      #adding score to every tile
      for i in range(self.grid_width):

         newScore = self.tile_matrix[row][i].number
         print("score:",newScore)
         self.sum += newScore
         print("Sum :",self.sum)



      self.tile_matrix = np.delete(self.tile_matrix,row,axis=0)
      self.tile_matrix = np.append(self.tile_matrix, np.reshape(np.full(self.grid_width,[None]),(-1,self.grid_width)),axis=0)
      print("----------AFTER------------")
      print(self.tile_matrix)
      print("------------------------------")

   def move_row(self,row):
      for row_i in range(row,self.grid_height):
         for col_i in range(self.grid_width):
            if self.tile_matrix[row_i][col_i] != None:
               self.tile_matrix[row_i][col_i].move(0,-1)

   def tile_matrix_print(self,tile_matrix):
      for row in tile_matrix:
         for tile in row:
            if tile == None:
               print(".", end=" ")
            else:
               print(tile, end=" ")
         print()
   def move_column(self,col,row):
      for row_i in range(row,self.grid_height):
         if self.tile_matrix[row_i][col] != None:
            print('-----MOVING-----')
            print('row_i',row_i,col)
            print("number",self.tile_matrix[row_i][col].number)

            print('====BEFORE=====')
            self.tile_matrix_print(self.tile_matrix)

            self.tile_matrix[row_i][col].move(0,-1)

            print('====AFTER====')
            self.tile_matrix_print(self.tile_matrix)
            print('===================')

            self.tile_matrix_print(self.tile_matrix)
      transposed = self.tile_matrix.transpose()
      deleted = np.delete(transposed[col],row)
      transposed[col] = np.append(deleted,[None],axis=0)
      self.tile_matrix = transposed.transpose()

   # FOUR CONNECTED TEST
   def delete_tile(self):
      for row_i in range(1,self.grid_height-1):
         for col_i in range(1,self.grid_width-1):
            if self.tile_matrix[row_i][col_i] != None:

               if self.tile_matrix[row_i + 1][col_i] is None and \
                 self.tile_matrix[row_i - 1][col_i] is None and \
                 self.tile_matrix[row_i][col_i + 1] is None and \
                 self.tile_matrix[row_i][col_i - 1] is None:
                  print('--------4connected-------')
                  self.tile_matrix[row_i][col_i] = None

                  self.delete_tile()

               #TODO Four Connected dependency check

   def merge(self):
      for row_i in range(self.grid_height-1):
         for col_i in range(self.grid_width ):
            if self.tile_matrix[row_i][col_i] != None and self.tile_matrix[row_i+1][col_i] != None:
               if self.tile_matrix[row_i][col_i].number == self.tile_matrix[row_i+1][col_i].number:
                  self.tile_matrix[row_i][col_i].double()
                  self.tile_matrix[row_i+1][col_i] = None
                  self.move_column(col_i,row_i+1)
                  print('------------------------------------')
                  print(row_i,col_i,self.tile_matrix[row_i][col_i].number)
                  self.merge()