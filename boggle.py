from string import ascii_uppercase
from random import choice

def make_grid(width, height):
    """
    Creates a grid that will hold all dice for a boggle game
    """
    # choice() returns an item from a list at random
    return {(row, col): choice(ascii_uppercase)
        for row in range(height)
        for col in range(width)}
        

def neighbours_of_position(coords):
    """
    Get neighbours of given position
    A 3 x 3 grid will have the coordinates of:
    -1,1     -1,0     -1,+1
    0,-1     0,0      0,+1
    +1,-1    +1,0     +1,+1
    """
    row = coords[0]
    col = coords[1]
    
    # Assign each of the neighbours
    # Going from top-left to top-right
    top_left = (row - 1, col - 1)
    top_centre = (row - 1, col)
    top_right = (row - 1, col + 1)
    
    # Left to right
    left = (row, col - 1)
    
    # The (row, col) coordinates passed to this
    # function are situated here
    right = (row, col + 1)

    bottom_left = (row + 1, col - 1)
    bottom_centre = (row + 1, col)
    bottom_right = (row + 1, col + 1)
    
    return [top_left, top_centre, top_right, left, right, bottom_left, bottom_centre, bottom_right]
    
    
def all_grid_neighbours(grid):
    """
    Get all of the possible neighbours for each position in the grid
    """
    neighbours = {}
    for position in grid:
        position_neighbours = neighbours_of_position(position)
        neighbours[position] = [p for p in position_neighbours if p in grid]
        
    return neighbours
    
    
def path_to_word(grid, path):
    """
    Add all of the letters on the path to a string
    """
    return ''.join([grid[p] for p in path])
    

def search(grid, dictionary):
    """
    Search through the paths to locate words by matching
    strings to words in a dictionary
    """
    # First we get the neighbours of every position in the grid...
    neighbours = all_grid_neighbours(grid)
    
    # ...then we get the paths list to capture all paths.
    # Note: the reason we are storing words as paths instead 
    #       strings is because a letter could be repeated
    #       in the grid several times. If we had two letter
    #       A's, how would we know which A it is.
    paths = []
    full_words, stems = dictionary
    
    # Note the nested function. This cannot be called directly
    # outside of the outer function, only by the outer function
    # or by itself recursively to build up paths. The search
    # function starts to search by passing a single position
    # to the do_search. This is a path of one letter. The
    # do_search function converts whatever path it's given
    # into a word and checks if it's in the dictionary. If
    # a path makes a word, it's added to the paths list.
    # Whether the path is a word or not, do_search gets each
    # of the neighbours of the last letter, checks to make sure
    # the neighbouring letter isn't already in the path and then
    # continues searching from that letter.
    # So, do_search calls itself eight times for each starting
    # position and again for each of the various neighbours of
    # each position in the grid and so on. 
    # For each position in the grid, we do a search and convert
    # all the paths and make valid words into words and return
    # them in a list.
    def do_search(path):
        word = path_to_word(grid, path)
        if word in full_words:
            paths.append(path)
        # To speed up the algorithm, we ignore the rest of the string
        # of letters (the path) if our current string (partial string of chars from path)
        # is not in stems. Example:
        #           String/word = 'B', the search continues as it is in the stems dictionary
        #           String/word = 'BA', the search continues as it is in the stems dictionary
        #           String/word = 'BAX', the search stops as it is NOT in the stems dictionary
        if word not in stems:
            return
        for next_pos in neighbours[path[-1]]: # path[-1] returns the last item
            if next_pos not in path:
                do_search(path + [next_pos])
                
    for position in grid:
        do_search([position])
            
    words = []
    for path in paths:
        words.append(path_to_word(grid, path))
        
    return set(words)
    
    
def get_dictionary(dict_file):
    """
    Load dictionary file 
    """
    full_words, stems = set(), set()

    with open(dict_file) as f:
        for word in f:
            word = word.strip().upper()
            full_words.add(word)
            
            for i in range(1, len(word)):
                stems.add(word[:i])
            
    #return [w.strip().upper() for w in f] # This returns a set
    #return {w.strip().upper() for w in f} # This returns a list -- exponentially faster!!
    
    return full_words, stems

def display_words(words):
    for word in words:
        print(word)
    
    print("Found %s words" % len(words))
        
def main():
    """
    This is the function that will run the whole project 
    """
    num_rows = 4
    num_cols = 4
    grid_letters = []
    grid = make_grid(num_cols, num_rows)
    # Display our grid
    for r in range(num_rows):
        for c in range(num_cols):
            grid_letters.append(grid[(r,c)] + ' ')
            #print("(%s,%s): %s" % (r,c,grid[(r,c)]))
            #print('({},{}): {}'.format(r, c, grid[(r,c)])) # Does exactly the same thing as line above
            #print('({0},{1}): {2}'.format(r, c, grid[(r,c)])) # Does exactly the same thing as line above
        grid_letters.append('\n')
    print(''.join(grid_letters))
    
    dictionary = get_dictionary('words.txt')
    words = search(grid, dictionary)

    if len(words) > 0:
        display_words(words)
    else:
        print("No words found. Creating new grid...")
        main()

"""
Running the code like below causes it to automatically get
executed when importing in our test file 

main()

Instead, do this:
"""
if __name__ == "__main__":
    main()

