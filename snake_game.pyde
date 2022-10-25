import os
import random
import time

path = os.getcwd()

# CONSTANTS AND COLORS' LISTS USED IN THE GAME
NROWS = 20
NCOLS = 20
RESOLUTION = 600
VELOCITY = 1
TILE_WIDTH = RESOLUTION/ NCOLS
TILE_HEIGHT = RESOLUTION/ NROWS
ELEMENT_RADIUS = 15
TEXTSIZE = 15
GAMEOVER_TEXTSIZE = 30
FIRST_ELEMENTS_COLOR = (80, 153, 32)
APPLE_COLOR = (173, 48, 32)
BANANA_COLOR = (251, 226, 76)


# Food class that determines the random positioning of the fruit and displaying it. 
class Food:
    def __init__(self, game):
        self.game = game         
        self.positioning()
    
    # Method that randomly places fruit on the board and loads the image(s) of apple or banana from the 'images' folder. 
    def positioning(self):
        if random.randint(0,1) == 0:
            self.name = "apple"
        else: 
            self.name = "banana"
        self.img = loadImage(path + '/images/' + self.name + ".png")         # Depending on the type of fruit generated (random module), self.img is assigned to either apple or banana. 
        
        # Create an empty list where all the possible positions of tiles on the board
        empty_set = set()
        for x in range(NCOLS):
            for y in range(NROWS):
                empty_set.add((x,y))
            
        # Find the possible coordinates where the food can be placed, i.e., from empty_set remove all the coordinates where the elements of the body are present. 
        possible_coordinates = empty_set - set(self.game.snake.body.coordinates) # Changing list of body coordinates to set for subtracting/ removing body-coordinates
        temp_list = list(possible_coordinates)                                   # Changing set to list again.
        self.point = random.choice(temp_list)                                    # point includes the coordinates of the food obtained such that it never overlaps the coordinates of body elements. 
        
    
    # Display method that displays the fruit on the board. Assign x and y coordinates of food's coordinates to two variables x and y which are used to find the number of pixels. 
    def display(self):
        x = self.point[0]
        y = self.point[1]
        image(self.img, x * TILE_WIDTH, y * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT)                         # Multiply x,y coordinates by Tile's width and height (i.e. to find the actual pixel based position) to correctly place the food on the board. 


# Element class that creates first element elements of the snake (including the head), and checks the invalid 
class Element:
    def __init__(self):
        self.coordinates = []                                                    # Empty list where the coordinates of the intial positioning of the snake's elements are appended. 
        for i in range(3):                                                       # Since, we need 3 elements at first (including the head), we use a range of 3.                                      
            self.coordinates.append(((NCOLS // 2) - i, NROWS // 2))              # Placing the first-three elements in the middle of board. First head is placed in the middle, and as we move to the second element, subtracting x co-ordinate from head's x-coordinate and so forth. 
    
    
    # Method to check if the snake's head has touched the borders of the board or not. This method is called in the Game class every time to check if the game_over is True or False.
    def check_invalid(self):
        x, y = self.coordinates[0]                                               # [Tuple unpacking] Assign x and y coordinates of the snake's head to x and y
        if ((0 <= x < NCOLS) and (0 <= y < NROWS) and (x,y) not in self.coordinates[1:]) == False:                  # If the head of the snake hits any of the four borders, the method returns True. 
            return True
        else:                                                                    # As long as the snake's head is within the border, the method will return False. 
            return False

# Snake class where we add first-two elements (at the very beginning of the game); we increase the length of the snake as it collides with the fruit; we handle the key press for movements.            
class Snake:
    def __init__(self, game):
        self.game = game
        self.reset()
    
    # Reset method of the snake class
    def reset(self):
        self.direction = RIGHT                                                   # Initial direction of the snake, i.e., movement from Left to Right
        self.head_horizontal = loadImage(path + "/images/head_left.png")         # Loads the image for the vertical movement of the snake. Later when UP/ DOWN keys are pressed, this attribute is called to display up/ down head iamge. 
        self.head_vertical = loadImage(path + "/images/head_up.png")             # Similarly, for LEFT/ RIGHT movement.
        self.img = self.head_horizontal                                          # Initial direction is RIGHT, so a specific attribute. Later based on key-press, this attribute takes different images.
        self.velocity = VELOCITY
        self.body = Element()                                                    # Element class is instantiated and assigned to self.body attribute. 
        self.body_colors = [0, FIRST_ELEMENTS_COLOR, FIRST_ELEMENTS_COLOR]       # For the first two elements, we use the color assigned to the constant variable at the very beginning. 0 is used as a dummy element for the ease of indexing. 
    
    # Method to move snake when keys are pressed
    def move_one_step(self):        
        for i in range(len(self.body.coordinates) - 1, 0, -1):                   # Take backward indexing of the body coordinates in the self.body.coordinates list
            self.body.coordinates[i] = self.body.coordinates[i - 1]              # Take the coordinate of the second last element and assign it to the last element, and repeat for all the elements in the list of the body-elements' coordinates
        x, y = self.body.coordinates[0]                                          # Assign x and y coordinates to variables x and y ~ (Tuple unpacking)
        
        # If the key pressed is LEFT or RIGHT, increase or decrease the x-coordinate of each and every element in the list. However, if the key pressed is UP or DOWN, else block is executed to increase the y-coordinate. 
        if self.direction in (LEFT, RIGHT):
            self.body.coordinates[0] = (x + self.velocity, y)
        else:
            self.body.coordinates[0] = (x , y + self.velocity)
    
    # Method that handles the keypress for the movement of the snake        
    def key_handler(self, keycode):                                              # Takes keycode argument from the keyPressed() function of the processing
        checker = False                                                          # Checker variable that handles the dynamic assignment of values in the attributes of different classes. If the correct key-press is used, it changes to 'TRUE'
        if keycode == LEFT and self.direction != RIGHT:                          # If the snake is not moving in the right direction, and LEFT key is pressed, the direction of the snake is changed to LEFT
            self.direction = LEFT
            checker = True
        elif keycode == RIGHT and self.direction != LEFT:                        # Similarly, for RIGHT key press in order to avoid the snake eating itself. 
            self.direction = RIGHT
            checker = True
        elif keycode == UP and self.direction != DOWN:                           # Similarly, for UP key press in order to avoid the snake eating itself.
            self.direction = UP
            checker = True
        elif keycode == DOWN and self.direction != UP:                           # Similarly, for DOWN key press in order to avoid the snake eating itself.
            self.direction = DOWN
            checker = True
        
        # When correct combination of key press is used this block gets executed
        if checker == True:
            if keyCode == LEFT or keyCode == UP:                                 # When LEFT or UP key is pressed, the direction of velocity is reversed, i.e., we subtract the x or y coordinates from the previous elements in the list.
                self.velocity = -VELOCITY
            elif keyCode == RIGHT or keyCode == DOWN:                            # When RIGHT or DOWN key is pressed, the direction of velocity is reversed, i.e., we subtract the x or y coordinates from the previous elements in the list.
                self.velocity = VELOCITY

            if keyCode == LEFT or keyCode == RIGHT:                              # For horizontal movement (i.e., when LEFT or RIGHT key is pressed, snake head image with left/ right orientation is assinged to self.img attribute)
                self.img = self.head_horizontal
            else:
                self.img = self.head_vertical                                    # For vertical movement (i.e., when UP or DOWN key is pressed, snake head image with up/ down orientation is assinged to self.img attribute)

    # During collision, an extra element (0, 0) is added to the list. And, using move_one_step() method, the value of the coordinate appended recently is altered based on the coordinates of the previous element in the list.
    def add_element(self):
        self.body.coordinates.append((0, 0))
        self.move_one_step()
    
        
    def display(self):
        x, y = self.body.coordinates[0]                                          # Assign the x, y coordinates of the head element (from the coordinates list) to x, y respectively
        if self.direction == LEFT or self.direction == UP:                       # When the direction of the snake is left or up, we use the loaded image directly and displayed using this display method
            image(self.img, x * TILE_WIDTH, y * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT)
        elif self.direction == RIGHT:                                            # However, when self.direction is RIGHT, we need to crop the image from TOP-RIGHT coordinates to BOTTOM-LEFT coordinates
            image(self.img, x * TILE_WIDTH, y * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT, TILE_WIDTH, 0, 0, TILE_WIDTH)
        elif self.direction == DOWN:                                             # Similarly, when self.direction is DOWN, we need to crop the image from BOTTOM-RIGHT coordinates to TOP-LEFT coordinates
            image(self.img, x * TILE_WIDTH, y * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT, 0, 0) 
        self.img.resize(TILE_WIDTH, TILE_HEIGHT) 
            
        counter = 1                                                              # Temporary variable to access different colors information appended together in the self.body_colors list. Its value is set to 1 because the element in index 0 is a dummy element
        for x, y in self.body.coordinates[1:]:                                   # [Tuple unpacking] Access the first element in the coordinates list (first after the head element) and assign its x, y coordinates to x and y respectively
            fill(self.body_colors[counter][0], self.body_colors[counter][1], self.body_colors[counter][2])   # From the first or second element of the body_color list, access R, G, B combinations of the list using double indexing
            strokeWeight(0)
            circle(x * TILE_WIDTH + TILE_WIDTH/2, y * TILE_HEIGHT + TILE_HEIGHT/2, TILE_WIDTH)               # Using x and y as the center of the circle and multiplying with pixels to correctly place it on the board
            counter += 1                                                         # Increase the value of counter when the the first element of the body-coordinate is created and filled with the color. The loop continues for the rest of the elements
        
        self.move_one_step()                                                     # Move the snake elements by one-step when the diplay method is called


# Game class to handle all the other classes of the game
class Game: 
    def __init__(self):
        self.snake = Snake(self)                                                 # Snake class is called
        self.food = Food(self)                                                   # Food class is called 
        self.reset()                                                             # reset method of Game class is called
        
    def reset(self):
        self.is_game_over = False                                                # Intially, game_over attribute is assigned to False
        self.food.positioning()                                                  # Call the positioning method of the food class to randomly place and load the images of the fruit
        self.snake.reset()                                                       # Call the reset method of the snake class: it loads the image for the head of the snake and determines the direction of the snake
        self.score = 0                                                           # Attribute to keep track of the score of the player: initally, it is set to 0, and later modified
    
    # Call the check_invalid() method of the snake class. If the snake hits the border, this method returns True, else False.
    def check_game_over(self):
        return self.snake.body.check_invalid()
    
    # Method to check if the length of the snake has covered the entire board or not. For which we check if the length of body_cordinates list is equal to the dimension of the board or not
    def check_total_fill(self):
        return len(self.snake.body.coordinates) == NCOLS * NROWS                 # If the snake has covered the entire board, this method will return TRUE.
    
    
    def show(self):
        if self.check_total_fill() == True:                                      # If the snake has covered the entire board, custom message of my choice is displayed using the method written below
            self.show_custom_display()
        elif self.check_game_over() == True:                                     # If game_over method returns true, the game over screen is displayed and self.is_game_over is changed to True (which was False initially)
            self.show_game_over_screen()
            self.is_game_over = True
        
        # However, if the game is not over, i.e, if the snake has not covered the board or has not hit the border, the elements of the snake, food are displayed and eating fruit is validated too.
        else:
            self.snake.display()                                                 # call the display method of the snake class
            self.food.display()                                                  # Call the display method of the food class
            self.check_update()                                                  # Call the collision method of the Game class to check if the snake has eaten the fruit and update it accordingly
        
        # Score displayed after displaying the snake
        self.display_score()                                                     # Attribute to display the score of the player all the time on the upper right corner of the board

    # Method to display the score of the player on the top right corner
    def display_score(self):
        textSize(TEXTSIZE)
        fill(0, 0, 0)
        text("Score: " + str(self.score), RESOLUTION - 90, 25)
    
    # When the snake has covered the entire board, this method is called and a message of my choice (called 'Classic Win') is displayed on the screen instead of 'Game Over!'
    def show_custom_display(self):
        textSize(TEXTSIZE)
        text("Classic Win !", (RESOLUTION - TILE_WIDTH)/2 - 35, (RESOLUTION - TILE_HEIGHT)/2)
    
    # When the snake hits the borders or hits its own element, a message of 'Game Over!' is displayed using this method
    def show_game_over_screen(self):
        textSize(TEXTSIZE)
        text("Game Over!", (RESOLUTION - TILE_WIDTH)/2 - 35, (RESOLUTION - TILE_HEIGHT)/2)
        
        # To display the score in the middle of the screen after the game is over
        textSize(GAMEOVER_TEXTSIZE)
        fill(0, 0, 0)
        text("FINAL SCORE: " + str(self.score), (RESOLUTION - TILE_WIDTH * 8.2)/2, (RESOLUTION + TILE_HEIGHT * 2)/2)

    # Method to check when the snake eats the fruit
    def check_update(self):
        # If the coordinate of the randomly assigned fruit lies in the body_coordinates list, this block is executed. If it's true, another if condition checks if the type of the food, and respective element colors are appened to the body_color list
        if self.food.point in self.snake.body.coordinates:
            if self.food.name == "apple":
                self.snake.body_colors.append(APPLE_COLOR)
            else:
                self.snake.body_colors.append(BANANA_COLOR)
            self.food.positioning()                                                 # This method of the food class generates a new position of the fruit as the old position disappears
            self.score += 1                                                         # The player's score is increased by 1
            self.snake.add_element()                                                # This method of the snake class adds new element to the body_coordinates list so that the length of the snake increases
        
# The main Game() class is instantiated    
game = Game()                                                 

def setup():
    size(RESOLUTION, RESOLUTION)
    # background(255, 255, 255)
    
def draw():
    if frameCount % 12 == 0:
        background(205)
        game.show()

# Processing function to handle the key presses
def keyPressed():
    game.snake.key_handler(keyCode)


# Processing function to restart the game when the user clicks the screen after game over
def mouseClicked():
    if game.is_game_over:
        game.reset()
         
