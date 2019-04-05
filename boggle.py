def make_grid(width, height):
    """
    Creates a grid that will hold all dice for a boggle game
    """
    return {(row, col): ' ' for row in range(height)
        for col in range(width)
    }