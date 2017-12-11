import unittest

class Column:
    """The column object of dancing link"""

    def __init__(self):
        self.left = None
        self.right = None
        self.up = None
        self.down = None
        self.column = None
        self.size = None
        self.name = None


class Data:
    """The data object of dancing link"""

    def __init__(self):
        self.left = None
        self.right = None
        self.up = None
        self.down = None
        self.column = None
        self.row = None

class Verifier:
    """A verifier to verify existence of solution and correctness of the problem matrix"""

    def verify_if_proper_subset(self, problem_matrix):
        """
        verify if the problem matrix includes proper subsets
        :param problem_matrix: the problem matrix to be solved
        """
        row_size = len(problem_matrix[0])
        for row in problem_matrix:
            if row.count(1) is row_size:
                return False
        return True
    def verify_existence(self, solution_set, problem_matrix):
        """
        Verify if the solution exists
        :param solution_set: the row indices of subsets of the solution
        :param problem_matrix: the problem matrix to be solved
        """
        subset = []
        total_ones = 0
        for row_number in solution_set:
            subset.append(problem_matrix[row_number])
        for row in subset:
            total_ones += row.count(1)
        if total_ones < len(problem_matrix[0]):
            return False
        else:
            return True

class DancingLinkSolver:
    """A implementation of algorithm X using dancing link as the data structure"""

    def __init__(self, header):
        """
        initialize the dancing link solver with the header of dancing link
        :param header: the header of the dancing link
        :type header: Column
        """

        self.header = header

        # initialize a iterator for transversing dancing link in four directions
        self.iterator = DancingLinkIterator()

        # initialize a dictionary to save solution rows
        self.solution_dictionary = {}

    def search(self, k=0):
        """
        A recursive procedure to search the solution that is invoked with k = 0
        :param k: the index of backtracking level
        """

        # terminate and return when all column are covered
        if self.header.right is self.header:
            return
        selected_column = self.choose_column()
        self.cover_column(selected_column)
        for r in self.iterator.down(selected_column):

            # save the solution of current backtracking level to solution dictionary
            self.solution_dictionary[str(k)] = r

            # cover all column that conflicts with the selected column
            for j in self.iterator.right(r):
                self.cover_column(j.column)

            # recursively search solutions
            self.search(k + 1)

            # backtrack
            r = self.solution_dictionary[str(k)]
            selected_column = r.column

            # uncover columns
            for j in self.iterator.left(r):
                self.uncover_column(j.column)
        self.uncover_column(selected_column)
        return

    def choose_column(self):
        """
        minimize the branching factor by choosing the column with the least size

        :return the reference of chosen column object
        """
        return self.find_least_ones_column()

    def find_least_ones_column(self):
        """
        Find the column with the least size
        :return selected_column: the reference of the selected column
        :rtype selected_column: Column
        """
        # set s to infinity
        s = float('inf')
        selected_column = None
        for column in self.iterator.right(self.header):
            if column.size < s:
                selected_column = column
                s = column.size
        return selected_column

    def cover_column(self, selected_column):
        """
        cover a column
        :param selected_column: the reference of the selected column
        """
        self.disconnect_column_object(selected_column)
        self.disconnect_data_object(selected_column)

    def disconnect_column_object(self, selected_column):
        """
        cover the selected column object from the linked list of columns
        :param selected_column: the reference of the selected column
        """
        selected_column.right.left = selected_column.left
        selected_column.left.right = selected_column.right

    def disconnect_data_object(self, selected_column):
        """
        cover the data objects of selected column
        :param selected_column: the reference of the selected column
        """
        for i in self.iterator.down(selected_column):
            for j in self.iterator.right(i):
                j.down.up = j.up
                j.up.down = j.down
                j.column.size -= 1

    def uncover_column(self, selected_column):
        """ uncover the selected column """
        self.connect_data_object(selected_column)
        self.connect_column_object(selected_column)

    def connect_data_object(self, selected_column):
        """ uncover the data objects of the selected column"""
        for i in self.iterator.up(selected_column):
            for j in self.iterator.left(i):
                j.column.size = j.column.size + 1  # why j.column.size and j.size
                j.down.up = j
                j.up.down = j

    def connect_column_object(self, selected_column):
        """ uncover the selected column object"""
        selected_column.right.left = selected_column
        selected_column.left.right = selected_column

    def print_solution(self):
        """ print the solution"""
        for key, data_object in self.solution_dictionary.items():
            print('In the level: ', key, 'the result is:', data_object.row)

    def get_solution(self):
        solution_list = []
        for key, data_object in self.solution_dictionary.items():
            solution_list.append(data_object.row)
        return solution_list

class DancingLinkIterator:
    """ A collection of iterator for dancing link"""

    def down(self, start_object):
        current_object = start_object.down
        while current_object is not start_object:
            yield current_object
            current_object = current_object.down

    def left(self, start_object):
        current_object = start_object.left
        while current_object is not start_object:
            yield current_object
            current_object = current_object.left

    def up(self, start_object):
        current_object = start_object.up
        while current_object is not start_object:
            yield current_object
            current_object = current_object.up

    def right(self, start_object):
        current_object = start_object.right
        while current_object is not start_object:
            yield current_object
            current_object = current_object.right


class DancingLinkConstructor:
    """ Constructing the dancing link"""

    def __init__(self, column_headers, problem_matrix):
        """ initialization
        :param column_headers: the headers of columns
        :param problem_matrix: the subset of column headers represented by a matrix with 1 and 0
        """
        self.verifier = Verifier()
        self.column_headers = column_headers
        self.problem_matrix = problem_matrix
        self.header = Column()

        # a auxiliary dictionary that saves the reference to the last data object of corresponding column
        self.column_tail_objects_dictionary = {}

    def construct(self):
        """
        Construct a dancing link
        :return the header column object of the dancing link
        """
        # raise exception when input problem matrix include non-proper subset
        if self.verifier.verify_if_proper_subset(self.problem_matrix) is not True:
            raise Exception('NOT A PROPER SUBSET')
        self.construct_columns()
        self.construct_column_tail_objects_dictionary()
        self.construct_rows()
        return self.header

    def construct_columns(self):
        """ Construct columns objects of the dancing link from left to right"""

        # the reference to the previous column object
        previous_column_object = None

        # # the reference to the last column object
        tail_column_object = None

        def connect_first_column_object_to_header():
            """ Connect the first column object when the right of header is None"""
            nonlocal previous_column_object
            current_column_object = Column()
            current_column_object.name = column_name
            current_column_object.left = self.header
            current_column_object.column = current_column_object
            self.header.right = current_column_object

            # update the reference to previous column object
            previous_column_object = current_column_object

        def connect_new_column_object():
            """ add a new column object"""
            nonlocal previous_column_object
            nonlocal tail_column_object
            current_column_object = Column()
            current_column_object.name = column_name
            current_column_object.column = current_column_object
            previous_column_object.right = current_column_object
            current_column_object.left = previous_column_object

            # update the references to the previous column object, and the last column object at rightmost
            previous_column_object = current_column_object
            tail_column_object = current_column_object

        def connect_column_head_tail():
            """connect the last column object to the header column object so that forming a circular linked list"""
            tail_column_object.right = self.header
            self.header.left = tail_column_object

        for column_name in self.column_headers:
            if self.header.right is None:
                connect_first_column_object_to_header()
            else:
                connect_new_column_object()
        connect_column_head_tail()

    def construct_rows(self):
        """construct data objects row by row"""

        # initialize a list save the size of each column
        column_sizes = [0] * len(self.column_headers)
        row_index = 0

        def set_up_new_data_object():
            nonlocal data_object
            # create a data object
            data_object = Data()

            # track column size
            # column_size: contain how many data object in each column
            #: A List
            column_sizes[column_index] += 1

            # set row number
            data_object.row = row_index

            column_tail_object = self.column_tail_objects_dictionary[str(column_index)]

            # set column field
            data_object.column = column_tail_object.column

            # create up-down connection to the last data object of the selected column
            self.connect_up_down(data_object, column_tail_object)

            # update the reference to last data object of current column
            self.column_tail_objects_dictionary[str(column_index)] = data_object

        def track_first_data_object():
            nonlocal first_in_row
            if first_in_row is None:
                first_in_row = data_object

        def track_last_data_object():
            nonlocal tail_in_row
            tail_in_row = data_object

        def connect_previous_left_data_object():
            """ connect the connection between current data object and the left data object"""
            nonlocal previous_left_object
            if previous_left_object is None:
                previous_left_object = data_object
            else:
                self.connect_left_right(previous_left_object, data_object)
                previous_left_object = data_object

        for row in self.problem_matrix:
            column_index = 0
            first_in_row = None
            tail_in_row = None
            previous_left_object = None
            data_object = None

            for data in row:
                if data is 1:
                    set_up_new_data_object()
                    track_first_data_object()
                    track_last_data_object()
                    connect_previous_left_data_object()
                column_index += 1
            row_index += 1
            self.connect_left_right(tail_in_row, first_in_row)

        # update column sizes after all data objects were created
        self.update_column_sizes(column_sizes)

        # connect the last data object to its corresponding column object forming a circular linked list
        self.connect_column_tail_head()

    def update_column_sizes(self, column_sizes):
        """
        updates column sizes
        :param column_sizes: List contains the sizes of columns
        """
        for index, size in enumerate(column_sizes):
            self.column_tail_objects_dictionary[str(index)].column.size = size

    def connect_column_tail_head(self):
        """ connect the tail data object to its corresponding column object"""
        for key, data_object in self.column_tail_objects_dictionary.items():
            data_object.down = data_object.column
            data_object.column.up = data_object

    def connect_up_down(self, down_object, up_object):
        """
        create double connection between up and down
        :param down_object: The down object
        :param up_object: The up object
        """
        down_object.up = up_object
        up_object.down = down_object

    def connect_left_right(self, left_object, right_object):
        """
        create double connection between left and right
        :param: left_object: The left object
        :param: right_object: The right object
        """
        left_object.right = right_object
        right_object.left = left_object

    def construct_column_tail_objects_dictionary(self):
        """Construct a dictionary that records the reference of the tail object of the corresponding column. """
        current_column = self.header.right
        current_column_index = 0
        while current_column is not self.header:
            self.column_tail_objects_dictionary[str(current_column_index)] = current_column
            current_column_index += 1
            current_column = current_column.right


class TestDancingLinkSolver(unittest.TestCase):
    """Test dancing link solver"""

    def setUp(self):
        """
                matrix=
                (0, 1, 0, 0, 0, 0),
                (1, 0, 0, 1, 0, 0),
                (0, 0, 1, 0, 0, 0),
                (0, 0, 0, 0, 1, 1),
                (1, 1, 0, 0, 0, 0)]

                The solution shall be 0, 1, 2, 3
        """
        self.column_headers = ['a', 'b', 'c', 'd', 'e', 'f']
        self.problem_matrix = [(0, 1, 0, 0, 0, 0), (1, 0, 0, 1, 0, 0), (0, 0, 1, 0, 0, 0), (0, 0, 0, 0, 1, 1),
                               (1, 1, 0, 0, 0, 0)]
        self.dl = DancingLinkConstructor(self.column_headers, self.problem_matrix)
        self.dl.header = self.dl.construct()
        self.solver = DancingLinkSolver(self.dl.header)
        self.verifier = Verifier()

    def setUp1(self):

        """
                matrix=
                (1, 1, 0, 1, 0, 0, 1),
                (1, 0, 1, 1, 0, 0, 0),
                (0, 0, 1, 0, 0, 1, 0),
                (0, 1, 0, 0, 1, 1, 0),
                (0, 0, 0, 0, 1, 0, 1)]
                The solution doesn't exist. The program only print the search record.
        """
        self.column_headers = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
        self.problem_matrix = [(1, 1, 0, 1, 0, 0, 1), (1, 0, 1, 1, 0, 0, 0), (0, 0, 1, 0, 0, 1, 0),
                               (0, 1, 0, 0, 1, 1, 0), (0, 0, 0, 0, 1, 0, 1)]
        self.dl = DancingLinkConstructor(self.column_headers, self.problem_matrix)
        self.dl.header = self.dl.construct()
        self.solver = DancingLinkSolver(self.dl.header)

    def setUp2(self):

        """
                matrix=
                (0, 0, 0, 0, 0, 0, 1),
                (1, 0, 1, 1, 0, 0, 0),
                (0, 0, 1, 0, 0, 1, 0),
                (0, 1, 0, 0, 1, 1, 0),
                (0, 0, 0, 0, 1, 0, 1)]
                The solution shall be 0, 1, 3
        """
        self.column_headers = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
        self.problem_matrix = [(0, 0, 0, 0, 0, 0, 1), (1, 0, 1, 1, 0, 0, 0), (0, 0, 1, 0, 0, 1, 0),
                               (0, 1, 0, 0, 1, 1, 0), (0, 0, 0, 0, 1, 0, 1)]
        self.dl = DancingLinkConstructor(self.column_headers, self.problem_matrix)
        self.dl.header = self.dl.construct()
        self.solver = DancingLinkSolver(self.dl.header)

    def test_search_set_up(self):
        print('---------------------')
        self.setUp()
        self.solver.search()
        data_objects = []
        for key, data_object in self.solver.solution_dictionary.items():
            data_objects.append(data_object)
        self.assertEqual(2, data_objects[0].row)
        self.assertEqual(1, data_objects[1].row)
        self.assertEqual(0, data_objects[2].row)
        self.assertEqual(3, data_objects[3].row)
        self.solver.print_solution()
        if self.verifier.verify_existence(self.solver.get_solution(),self.problem_matrix):
            print('Solution exists')
        else:
            print('No solution')
        self.assertEqual(self.solver.get_solution(), [2, 1, 0,3])

    def test_search_set_up1(self):
        print('---------------------')
        self.setUp1()
        self.solver.search()
        data_objects = []
        for key, data_object in self.solver.solution_dictionary.items():
            data_objects.append(data_object)
        self.assertEqual(1, data_objects[0].row)
        self.assertEqual(3, data_objects[1].row)
        self.solver.print_solution()
        if self.verifier.verify_existence(self.solver.get_solution(), self.problem_matrix):
            print('Solution exists')
        else:
            print('No solution')

        self.assertEqual(self.solver.get_solution(), [1, 3])

    def test_search_set_up2(self):
        print('---------------------')
        self.setUp2()
        self.solver.search()
        data_objects = []
        for key, data_object in self.solver.solution_dictionary.items():
            data_objects.append(data_object)

        self.solver.print_solution()
        self.assertEqual(1, data_objects[0].row)
        self.assertEqual(3, data_objects[1].row)
        self.assertEqual(0, data_objects[2].row)
        if self.verifier.verify_existence(self.solver.get_solution(), self.problem_matrix):
            print('Solution exists')
        else:
            print('No solution')

        self.assertEqual(self.solver.get_solution(),[1, 3, 0])

    def test_row_up_iterator(self):
        """
        Test Iterator_up function
        Make sure each column connect up to down,
        and the head connect to tail
        """
        Iterator = DancingLinkIterator()
        column_a = Column()
        column_b = Column()
        column_c = Column()
        column_d = Column()

        column_a.up = column_b
        column_b.up = column_c
        column_c.up = column_d
        column_d.up = column_a
        column_a.name = 'a'
        column_b.name = 'b'
        column_c.name = 'c'
        column_d.name = 'd'

        up_columns = []
        for i in Iterator.up(column_a):
            up_columns.append(i)
        self.assertEqual(up_columns[0].name, 'b')
        self.assertEqual(up_columns[1].name, 'c')
        self.assertEqual(up_columns[2].name, 'd')

    def test_column_down_Iterator(self):
        """
        Test Iterator_down function
        Make sure each column connect up to down,
        and the head connect to tail
        """
        Iterator = DancingLinkIterator()
        column_a = Column()
        column_b = Column()
        column_c = Column()
        column_d = Column()

        column_a.down = column_b
        column_b.down = column_c
        column_c.down = column_d
        column_d.down = column_a
        column_a.name = 'a'
        column_b.name = 'b'
        column_c.name = 'c'
        column_d.name = 'd'

        down_columns = []
        for i in Iterator.down(column_a):
            down_columns.append(i)
        self.assertEqual(down_columns[0].name, 'b')
        self.assertEqual(down_columns[1].name, 'c')
        self.assertEqual(down_columns[2].name, 'd')

    def test_row_left_Iterator(self):
        """
        Test Iterator_left function
        Make sure each column connect up to down,
        and the head connect to tail
        """
        Iterator = DancingLinkIterator()
        column_a = Column()
        column_b = Column()
        column_c = Column()
        column_d = Column()

        column_a.left = column_b
        column_b.left = column_c
        column_c.left = column_d
        column_d.left = column_a
        column_a.name = 'a'
        column_b.name = 'b'
        column_c.name = 'c'
        column_d.name = 'd'

        left_columns = []
        for i in Iterator.left(column_a):
            left_columns.append(i)
        self.assertEqual(left_columns[0].name, 'b')
        self.assertEqual(left_columns[1].name, 'c')
        self.assertEqual(left_columns[2].name, 'd')

    def test_row_right_Iterator(self):
        """
        Test Iterator_right function
        Make sure each column connect up to down,
        and the head connect to tail
        """
        Iterator = DancingLinkIterator()
        column_a = Column()
        column_b = Column()
        column_c = Column()
        column_d = Column()

        column_a.right = column_b
        column_b.right = column_c
        column_c.right = column_d
        column_d.right = column_a
        column_a.name = 'a'
        column_b.name = 'b'
        column_c.name = 'c'
        column_d.name = 'd'

        right_columns = []
        for i in Iterator.right(column_a):
            right_columns.append(i)
        self.assertEqual(right_columns[0].name, 'b')
        self.assertEqual(right_columns[1].name, 'c')
        self.assertEqual(right_columns[2].name, 'd')

    def test_choose_a_column(self):
        """Test choose_a_column function"""
        self.setUp()
        columns = []
        for column in self.solver.iterator.right(self.solver.header):
            columns.append(column)
        self.assertEqual(self.solver.find_least_ones_column(), columns[2])

        columns1 = []
        self.setUp1()
        for column in self.solver.iterator.right(self.solver.header):
            columns1.append(column)
        self.assertEqual(self.solver.find_least_ones_column(), columns1[0])

        columns2 = []
        self.setUp2()
        for column in self.solver.iterator.right(self.solver.header):
            columns2.append(column)
        self.assertEqual(self.solver.find_least_ones_column(), columns2[0])

    def test_find_least_ones_column(self):
        self.setUp()
        columns = []
        for column in self.solver.iterator.right(self.solver.header):
            columns.append(column)
        self.assertEqual(self.solver.find_least_ones_column(), columns[2])


class TestColumn(unittest.TestCase):
    """Test initial column function"""

    def test_init_(self):
        collumn = Column()
        self.assertEqual([collumn.left, collumn.right, collumn.up, collumn.down,
                          collumn.column, collumn.size, collumn.name], [None] * 7)


class TestData(unittest.TestCase):
    """Test initial data function"""

    def test_init_(self):
        data = Data()
        self.assertEqual([data.left, data.down, data.left, data.right, data.column
                             , data.row], [None] * 6)


class TestDancingLinkConstructor(unittest.TestCase):
    dl = None

    def init(self):
        """Init function with empty data, test init constructor"""
        column_headers = []
        problem_matrix = []
        self.dl = DancingLinkConstructor(column_headers, problem_matrix)

    def setUp(self):
        """Test construct function"""
        column_headers = ['a', 'b', 'c', 'd', 'e', 'f']
        problem_matrix = [(0, 1, 0, 0, 0, 0), (1, 0, 0, 1, 0, 0), (0, 0, 1, 0, 0, 0), (0, 0, 0, 0, 1, 1)]
        self.dl = DancingLinkConstructor(column_headers, problem_matrix)
        self.dl.header = self.dl.construct()

    def test_construct_exception(self):
        """Test exception when problem matrix including non-proper subset"""
        column_headers = ['a', 'b', 'c', 'd', 'e', 'f']
        problem_matrix = [(1, 1, 1, 1, 1, 1)]
        self.dl = DancingLinkConstructor(column_headers, problem_matrix)
        self.assertRaises(Exception, )
        with self.assertRaises(Exception) as ex:
            self.dl.construct()
        the_exception = ex.exception
        print(the_exception)
        self.assertEqual(str(the_exception),'NOT A PROPER SUBSET')

    def test_init_construct(self):
        """The instance to test init construct function"""
        self.init()
        self.assertEqual(self.dl.header.left, None)
        self.assertEqual(self.dl.header.right, None)
        self.assertEqual(self.dl.header.up, None)
        self.assertEqual(self.dl.header.down, None)
        self.assertEqual(self.dl.column_headers, [])
        self.assertEqual(self.dl.problem_matrix, [])
        self.assertEqual(self.dl.column_tail_objects_dictionary, {})

    def test_construct_columns(self):
        """Test init construct function with data"""
        self.setUp()
        self.assertEqual(self.dl.column_headers, ['a', 'b', 'c', 'd', 'e', 'f'])
        self.assertEqual(self.dl.header.right.name, 'a')
        self.assertEqual(self.dl.header.left.name, 'f')
        self.assertEqual(len(self.dl.column_tail_objects_dictionary), 6)

    def test_construct_column_tail_objects_dictionary(self):
        """Test init column tail dictionary function"""
        self.assertEqual(len(self.dl.column_tail_objects_dictionary), 6)

        self.assertEqual(self.dl.column_tail_objects_dictionary['0'].column.name, 'a')
        self.assertEqual(self.dl.column_tail_objects_dictionary['1'].column.name, 'b')
        self.assertEqual(self.dl.column_tail_objects_dictionary['2'].column.name, 'c')
        self.assertEqual(self.dl.column_tail_objects_dictionary['3'].column.name, 'd')
        self.assertEqual(self.dl.column_tail_objects_dictionary['4'].column.name, 'e')
        self.assertEqual(self.dl.column_tail_objects_dictionary['5'].column.name, 'f')

    def test_construct_rows(self):
        """Test construct rows function"""
        self.setUp()
        self.assertEqual(self.dl.column_tail_objects_dictionary['0'].column.size, 1)
        self.assertEqual(self.dl.column_tail_objects_dictionary['1'].column.size, 1)
        self.assertEqual(self.dl.column_tail_objects_dictionary['2'].column.size, 1)
        self.assertEqual(self.dl.column_tail_objects_dictionary['3'].column.size, 1)
        self.assertEqual(self.dl.column_tail_objects_dictionary['4'].column.size, 1)
        self.assertEqual(self.dl.column_tail_objects_dictionary['5'].column.size, 1)

    def test_update_column_sizes(self):
        column_headers = ['a', 'b', 'c', 'd', 'e', 'f']
        problem_matrix = [(0, 1, 0, 0, 0, 0), (1, 0, 0, 1, 0, 0), (0, 0, 1, 0, 0, 0), (0, 0, 0, 0, 1, 1)]
        danceLink = DancingLinkConstructor(column_headers, problem_matrix)
        danceLink.construct()
        danceLink.update_column_sizes([1, 1, 1, 1, 1, 1])
        self.assertEqual(danceLink.column_tail_objects_dictionary['0'].column.size, 1)
        self.assertEqual(danceLink.column_tail_objects_dictionary['1'].column.size, 1)
        self.assertEqual(danceLink.column_tail_objects_dictionary['2'].column.size, 1)
        self.assertEqual(danceLink.column_tail_objects_dictionary['3'].column.size, 1)
        self.assertEqual(danceLink.column_tail_objects_dictionary['4'].column.size, 1)
        self.assertEqual(danceLink.column_tail_objects_dictionary['5'].column.size, 1)

    def test_connect_column_tail_head(self):
        """Test connect column tail to head function"""
        self.setUp()
        for key, data_object in self.dl.column_tail_objects_dictionary.items():
            self.assertEqual(data_object.column, data_object.down)
            self.assertEqual(data_object, data_object.column.up)

    def test_connect_up_down(self):
        """Test connect up to down function"""
        Data1 = Data()
        Data2 = Data()
        self.init()
        self.dl.connect_up_down(Data1, Data2)
        self.assertEqual(Data2, Data1.up)
        self.assertEqual(Data1, Data2.down)

    def test_connect_left_right(self):
        """Test connect left to right function"""
        Data1 = Data()
        Data2 = Data()
        self.init()
        self.dl.connect_left_right(Data1, Data2)
        self.assertEqual(Data2, Data1.right)
        self.assertEqual(Data1, Data2.left)


class TestVerifier(unittest.TestCase):

    def setUp(self):
        self.problem_matrix_of_wrong_subset = [(0, 0, 0, 0, 0, 0, 1), (1, 1, 1, 1, 1, 1, 1), (0, 0, 1, 0, 0, 1, 0),
                                               (0, 1, 0, 0, 1, 1, 0), (0, 0, 0, 0, 1, 0, 1)]
        self.problem_matrix_of_no_solution = [(0, 0, 0, 0, 0, 0, 1), (1, 0, 1, 1, 0, 0, 0)]
        self.problem_matrix_of_existing_solution = [(0, 1, 0, 0, 0, 0), (1, 0, 0, 1, 0, 0), (0, 0, 1, 0, 0, 0), (0, 0, 0, 0, 1, 1),
                                                    (1, 1, 0, 0, 0, 0)]
        self.verifier = Verifier()

    def test_verify_full_ones_row(self):
        self.assertFalse(self.verifier.verify_if_proper_subset(self.problem_matrix_of_wrong_subset))

    def test_verify_solution_existence_false(self):
        self.assertFalse(self.verifier.verify_existence( [0,1,2],self.problem_matrix_of_existing_solution))

    def test_verify_solution_existence_true(self):
        self.assertTrue(self.verifier.verify_existence([0, 1, 2,3], self.problem_matrix_of_existing_solution))
