import stddraw # the stddraw module is used as a basic graphics library
from color import Color # used for coloring the tile and the number on it
from point import Point # used for representing the position of the tile
import copy as cp # the copy module is used for copying tile positions
from random import randint
import math # math module that provides mathematical functions

# Class used for representing numbered tiles as in 2048
class Tile: 
   # Class attributes shared among all Tile objects
   # ---------------------------------------------------------------------------
   # value used for the thickness of the boxes (boundaries) around the tiles
   boundary_thickness = 0.004
   # font family and size used for displaying the tile number
   font_family, font_size = "Arial", 14

   # Constructor that creates a tile at a given position with 2 as its number 
   def __init__(self, position = Point(0, 0)): # (0, 0) is the default position
      # assign the number on the tile
      self.number = 2**randint(1,3)
      # set the colors of the tile


      self.foreground_color = Color(0, 100, 200) # foreground (number) color
      self.boundary_color = Color(0, 100, 200) # boundary (box) color
      # set the position of the tile as the given position
      self.position = Point(position.x, position.y)
   def __repr__(self):
      return str(self.number)
   # Setter method for the position of the tile
   def set_position(self, position):
      # set the position of the tile as the given position
      self.position = cp.copy(position) 

   # Getter method for the position of the tile
   def get_position(self):
      # return the position of the tile
      return cp.copy(self.position)


   def double(self):
      self.number *= 2

   # Method for moving the tile by dx along the x axis and by dy along the y axis
   def move(self, dx, dy):
      self.position.translate(dx, dy)

   # Method for drawing the tile
   def draw(self):
      # draw the tile as a filled square
      if (self.number == 2):
         self.background_color = Color(238, 228, 218) # background (tile) color
      if (self.number == 4):
         self.background_color = Color(237, 224, 200)  # background (tile) color
      if (self.number == 8):
         self.background_color = Color(242, 177, 121)  # background (tile) color
      if (self.number == 16):
         self.background_color = Color(245, 149, 99)  # background (tile) color
      if (self.number == 32):
         self.background_color = Color(246, 124, 95)  # background (tile) color
      if (self.number == 64):
         self.background_color = Color(246, 94, 59)  # background (tile) color
      if (self.number == 128):
         self.background_color = Color(237, 207, 114)  # background (tile) color
      if (self.number == 256):
         self.background_color = Color(237, 204, 97)  # background (tile) color
      if (self.number == 512):
         self.background_color = Color(237, 200, 80)  # background (tile) color
      if (self.number == 1024):
         self.background_color = Color(237, 197, 63)  # background (tile) color
      if (self.number == 2048):
         self.background_color = Color(237, 194, 46)  # background (tile) color
      #used proper colors until 2048
      #used remainder in order to get a proper color for every number
      #with this the value will never exceed 255 however better solution may be proposed
      if (self.number > 2048):
         self.background_color= Color((self.number%255),(self.number%20),(self.number%255))

      stddraw.setPenColor(self.background_color)
      stddraw.filledSquare(self.position.x, self.position.y, 0.5)
      # draw the bounding box of the tile as a square
      stddraw.setPenColor(self.boundary_color)
      stddraw.setPenRadius(Tile.boundary_thickness)
      stddraw.square(self.position.x, self.position.y, 0.5)
      stddraw.setPenRadius()  # reset the pen radius to its default value
      # draw the number on the tile
      stddraw.setPenColor(self.foreground_color)
      stddraw.setFontFamily(Tile.font_family)
      stddraw.setFontSize(Tile.font_size)
      stddraw.boldText(self.position.x, self.position.y, str(self.number))
