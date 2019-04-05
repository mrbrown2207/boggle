import unittest
import boggle

class TestBoggle(unittest.TestCase):
    """
    Our test suite for boggle solver
    """
    
    def test_can_create_an_empty_grid(self):
        """
        Test to see if we can create an empty grid
        """
        grid = boggle.make_grid(0, 0)
        self.assertEqual(len(grid), 0)
        

    def test_grid_size_is_width_times_height(self):
        """
        Test to ensure that the total size of the grid
        is equal to width * height
        """
        grid = boggle.make_grid(2, 3)
        self.assertEqual(len(grid), 6)
        
    def test_grid_coordinates(self):
        """
        Test to ensure that all of the coordinates inside
        of the grid can be accessed
        """
        num_rows = 2
        num_cols = 2
        grid = boggle.make_grid(num_cols, num_rows)
        for c in range(num_cols):
            for r in range(num_rows):
               self.assertIn((c, r), grid)
               
        self.assertNotIn((num_cols+1, num_rows+1), grid)
