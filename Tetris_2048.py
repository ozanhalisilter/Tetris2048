import stddraw # the stddraw module is used as a basic graphics library
import random # used for creating tetrominoes with random types/shapes
from game_grid import GameGrid # class for modeling the game grid
from tetromino import Tetromino # class for modeling the tetrominoes
from picture import Picture # used representing images to display
import os # used for file and directory operations
from color import Color # used for coloring the game menu

# MAIN FUNCTION OF THE PROGRAM
#-------------------------------------------------------------------------------
# Main function where this program starts execution
def canvas():
   # set the dimensions of the game grid
   global grid_h, grid_w
   grid_h, grid_w = 18, 12
   # set the size of the drawing canvas
   canvas_h, canvas_w = 40 * grid_h, 60 * grid_w
   stddraw.setCanvasSize(canvas_w, canvas_h)
   # set the scale of the coordinate system
   stddraw.setXscale(-0.5, grid_w + 4.5)
   stddraw.setYscale(-0.5, grid_h - 0.5)

   # display a simple menu before opening the game
   display_game_menu(grid_h, grid_w+5)

def start():

   global grid
   # create the game grid
   grid = GameGrid(grid_h, grid_w)
   # create the first tetromino to enter the game grid 
   # by using the create_tetromino function defined below
   current_tetromino = create_tetromino(grid_h, grid_w)
   # print("next tetromino:")
   next_tetromino = create_tetromino(grid_h, grid_w)

   grid.current_tetromino = current_tetromino
   grid.next_tetromino = next_tetromino
   stddraw.clearKeysTyped()
   pause = False
   # main game loop (keyboard interaction for moving the tetromino) 
   while True:

      if not pause:
         mx, my = stddraw.getPosition()
         tileX = grid.current_tetromino.bottom_left_corner.x
         ax = int(mx / 42.35) - 1
         # print(ax, tileX)

         if ax > tileX:
            for i in range(ax - tileX):
               grid.current_tetromino.move("right", grid)
         elif ax < tileX:
            for i in range(tileX - ax):
               grid.current_tetromino.move("left", grid)

      # check user interactions via the keyboard
      if stddraw.hasNextKeyTyped():
         key_typed = stddraw.nextKeyTyped()

         # Pause
         if key_typed=='p':
            print("Pause")
            if pause:
               pause = False
            else:
               pause = True

         elif not pause:



            # if the left arrow key has been pressed
            if key_typed == "left":
               # move the tetromino left by one
               # print("Left Typed")
               current_tetromino.move(key_typed, grid)
            # if the right arrow key has been pressed
            elif key_typed == "right":
               # print("Right Typed")
               # move the tetromino right by one
               current_tetromino.move(key_typed, grid)
            # if the down arrow key has been pressed
            elif key_typed == "down":

               # move the tetromino down by one
               # (causes the tetromino to fall down faster)
               current_tetromino.move(key_typed, grid)
            # piece drop
            elif key_typed =='space':
               for i in range(grid_h):
                  current_tetromino.move('down',grid)
            # Speed Increase
            elif key_typed=='w':
               if grid.delta_time > 50:
                  grid.delta_time -= 40
            # Speed Decrease
            elif key_typed=='s':
               if grid.delta_time < 500:
                  grid.delta_time += 40

            elif key_typed == 'e':
               current_tetromino.rotate(grid)

            elif key_typed=='q':
               current_tetromino.rotate_ccw(grid)

         if key_typed=='r':
            print("restart")
            start()


         # clear the queue that stores all the keys pressed/typed
         stddraw.clearKeysTyped()


      # move (drop) the tetromino down by 1 at each iteration
      if not pause:
         success = current_tetromino.move("down", grid)


      # place the tetromino on the game grid when it cannot go down anymore
      if not success and not pause:
         # get the tile matrix of the tetromino
         tiles_to_place = current_tetromino.tile_matrix
         # update the game grid by adding the tiles of the tetromino
         game_over = grid.update_grid(tiles_to_place)
         # end the main game loop if the game is over
         if game_over:
            if display_game_over(grid_h,grid_w+5):
               pause = True
               start()


         # create the next tetromino to enter the game grid
         # by using the create_tetromino function defined below
         current_tetromino = next_tetromino
         grid.current_tetromino = current_tetromino
         print("next tetromino:")
         next_tetromino = create_tetromino(grid_h, grid_w)
         grid.next_tetromino = next_tetromino
         next_tetromino.draw_dummy()

      # display the game grid and as well the current tetromino      
      grid.display(pause)

   print("Game over")

# Function for creating random shaped tetrominoes to enter the game grid
def create_tetromino(grid_height, grid_width):
   # type (shape) of the tetromino is determined randomly
   # test with O's
   #tetromino_types = ['S']
   tetromino_types = [ "S", "T","J",'L','O','Z','I']
   random_index = random.randint(0, len(tetromino_types) - 1)
   random_type = tetromino_types[random_index]
   # create and return the tetromino
   tetromino = Tetromino(random_type, grid_height, grid_width)
   return tetromino

# Function for displaying a simple menu before starting the game
def display_game_menu(grid_height, grid_width):
   # colors used for the menu
   background_color = Color(42, 69, 99)
   button_color = Color(25, 255, 228)
   text_color = Color(31, 160, 239)
   # clear the background canvas to background_color
   stddraw.clear(background_color)

   # get the directory in which this python code file is placed
   current_dir = os.path.dirname(os.path.realpath(__file__))
   # path of the image file
   img_file = current_dir + "/menu_image.png"
   # center coordinates to display the image
   img_center_x, img_center_y = (grid_width - 1) / 2, grid_height - 7
   # image is represented using the Picture class
   image_to_display = Picture(img_file)
   # display the image
   stddraw.picture(image_to_display, img_center_x, img_center_y)
   # dimensions of the start game button
   button_w, button_h = grid_width - 1.5, 2
   # coordinates of the bottom left corner of the start game button 
   button_blc_x, button_blc_y = img_center_x - button_w / 2, 4
   # display the start game button as a filled rectangle
   stddraw.setPenColor(button_color)
   stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)
   # display the text on the start game button
   stddraw.setFontFamily("Arial")
   stddraw.setFontSize(25)
   stddraw.setPenColor(text_color)
   text_to_display = "Click Here to Start the Game"
   stddraw.text(img_center_x, 5, text_to_display)
   # menu interaction loop
   while True:
      # display the menu and wait for a short time (50 ms)
      stddraw.show(50)
      # check if the mouse has been left-clicked
      if stddraw.mousePressed():
         # get the x and y coordinates of the location at which the mouse has 
         # most recently been left-clicked  
         mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
         if mouse_x >= button_blc_x and mouse_x <= button_blc_x + button_w:
            if mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h: 
               break # break the loop to end the method and start the game

def display_game_over(grid_height, grid_width):
   background_color = Color(42, 69, 99)
   button_color = Color(25, 255, 228)
   text_color = Color(31, 160, 239)
   # clear the background canvas to background_color
   stddraw.clear(background_color)

   # get the directory in which this python code file is placed
   current_dir = os.path.dirname(os.path.realpath(__file__))
   # path of the image file
   img_file = current_dir + "/menu_image.png"
   # center coordinates to display the image
   img_center_x, img_center_y = (grid_width - 1) / 2, grid_height - 7
   # image is represented using the Picture class
   image_to_display = Picture(img_file)
   # display the image
   stddraw.picture(image_to_display, img_center_x, img_center_y)
   # dimensions of the start game button
   button_w, button_h = grid_width - 1.5, 2
   # coordinates of the bottom left corner of the start game button
   button_blc_x, button_blc_y = img_center_x - button_w / 2, 4
   # display the start game button as a filled rectangle
   stddraw.setPenColor(button_color)
   stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)
   # display the text on the start game button
   stddraw.setFontFamily("Arial")
   stddraw.setFontSize(25)
   stddraw.setPenColor(text_color)
   text_to_display = "Game Over"
   stddraw.text(img_center_x, 5.5, text_to_display)
   stddraw.text(img_center_x,4.5, "Score : "+ str(grid.total_score))
   # menu interaction loop
   while True:
      # display the menu and wait for a short time (50 ms)
      stddraw.show(50)
      # check if the mouse has been left-clicked
      if stddraw.mousePressed():
         # get the x and y coordinates of the location at which the mouse has
         # most recently been left-clicked
         mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
         if mouse_x >= button_blc_x and mouse_x <= button_blc_x + button_w:
            if mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h:
               return True
                 # break the loop to end the method and start the game


# start() function is specified as the entry point (main function) from which 
# the program starts execution
if __name__== '__main__':
   canvas()
   start()
