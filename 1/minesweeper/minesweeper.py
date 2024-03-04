import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True
        '''

        for i, row in enumerate((
            (0, 0, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0),
            (0, 0, 1, 0, 0, 1, 0, 0),
            (0, 0, 0, 0, 0, 1, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 1, 0),
            (0, 1, 0, 0, 1, 0, 1, 0),
            (0, 0, 1, 0, 0, 0, 0, 0),
        )):
            for j, v in enumerate(row):
                self.mines.add((i, j))
                self.board[i][j] = v == 1
        '''

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            return self.cells
        return set()


    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        return set()


    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count-=1


    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)


    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # 1) mark the cell as a move that has been made
        # 2) mark the cell as safe
        self.moves_made.add(cell)
        self.mark_safe(cell)

        # 3) add a new sentence to the AI's knowledge base
        #    based on the value of `cell` and `count`
        # determine neighboring cells, then insert new Sentence
        cells = set()
        #mine_count = 0

        i, j = cell
        for neighbor_cell in (
            (i-1, j-1),
            (i-1, j),
            (i-1, j+1),
            (i, j-1),
            (i, j+1),
            (i+1, j-1),
            (i+1, j),
            (i+1, j+1),
        ):
            neighbor_i, neighbor_j = neighbor_cell
            #print(f'propose {neighbor_i}, {neighbor_j}')
            if (neighbor_i, neighbor_j) in self.mines:
                count-=1
                continue
            if (neighbor_i, neighbor_j) in self.safes:
                continue
            if (neighbor_i, neighbor_j) in self.moves_made:
                continue
            if 0 <= neighbor_i < self.height and 0 <= neighbor_j < self.width:
                cells.add(neighbor_cell)
                '''
                if count == 0:
                    self.mark_safe(neighbor_cell)
                '''
                '''
                '''
        self.knowledge.append(Sentence(cells, count))

        '''
        sentence = Sentence(cells, count - mine_count)
        self.knowledge.append(sentence)
        self.knowledge.append(Sentence(cells, count - mine_count))

        for s in self.knowledge:
            if s.known_mines():
                for c in s.known_mines().copy():
                    self.mark_mine(c)
            if s.known_safes():
                for c in s.known_safes().copy():
                    self.mark_safe(c)

        for s in self.knowledge:
            if sentence.cells.issubset(s.cells):
                self.knowledge.append(Sentence(
                    s.cells.difference(sentence.cells),
                    s.count - sentence.count,
                ))

        self.knowledge.append(sentence)
        '''


        print(f'learned {count} {cells}')
        #print([(_.count, _.cells) for _ in self.knowledge])

        # 4) mark any additional cells as safe or as mines
        #    if it can be concluded based on the AI's knowledge base
        for s in self.knowledge:
            if s.count == 0:
                for c in s.cells.copy():
                    self.mark_safe(c)
            elif s.count == len(s.cells):
                for c in s.cells.copy():
                    self.mark_mine(c)

        # 5) add any new sentences to the AI's knowledge base
        #    if they can be inferred from existing knowledge

        #print(f'***{[(_.count, _.cells) for _ in self.knowledge]}')
        inferred_knowledge = []
        for s, s2 in itertools.product(self.knowledge, self.knowledge):
            if len(s.cells) == 0:
                continue
            if len(s2.cells) == 0:
                continue
            if s2 == s:
                continue
            #print(f'*{s}')
            #print(f'**{cells}={count} {s}')
            #print(f'*{cells} {s.cells}')
            if s2.cells < s.cells:
                if diff_cells := s.cells - s2.cells:
                    diff_count = s.count - s2.count
                    print(f'infer {s.cells} {s.count}, {s2.cells} {s2.count}')
                    print(f'*infer {diff_cells} {diff_count}')
                    inferred_sentence = Sentence(diff_cells, diff_count)
                    if inferred_sentence not in self.knowledge:
                        inferred_knowledge.append(inferred_sentence)
                    if diff_count == 0:
                        for c in diff_cells:
                            self.safes.add(c)
                    elif diff_count == len(diff_cells):
                        for c in diff_cells:
                            self.mines.add(c)
            elif s.cells < s2.cells:
                if diff_cells := s2.cells - s.cells:
                    diff_count = s2.count - s.count
                    print(f'infer2 {s2.cells} {s2.count}, {s.cells} {s.count}')
                    print(f'*infer2 {diff_cells} {diff_count}')
                    inferred_sentence = Sentence(diff_cells, diff_count)
                    if inferred_sentence not in self.knowledge:
                        inferred_knowledge.append(inferred_sentence)
                    if diff_count == 0:
                        for c in diff_cells:
                            self.safes.add(c)
                    elif diff_count == len(diff_cells):
                        for c in diff_cells:
                            self.mines.add(c)

        self.knowledge.extend(inferred_knowledge)

        '''
        for s in self.knowledge:
            if s.count == 0:
                for c in s.cells.copy():
                    s.mark_safe(cell)
                    self.safes.add(c)
            elif s.count == len(s.cells):
                for c in s.cells.copy():
                    s.mark_mine(c)
                    self.mines.add(c)
        '''


        '''
            if count == 0:
                print(f'mark_safe {cells}')
                for c in cells:
                    self.mark_safe(c)
                    #for s in self.knowledge:
                    #    pass
            elif count == len(cells):
                for c in cells:
                    self.mark_mine(c)
                    #for s in self.knowledge:
                    #    pass
            else:
                self.knowledge.append(Sentence(cells, count))
            print([(_.count, _.cells) for _ in self.knowledge])


        '''




        '''
        if count == 0:
            for cell_ in cells:
                self.mark_safe(cell_)
        elif len(cells) == count:
            for cell_ in cells:
                self.mark_mine(cell_)
        for i, j in cells:
        print([(_.count, _.cells) for _ in self.knowledge])
        '''
        print(f'safes {self.safes}')
        print(f'mines {self.mines}')
        '''
        for sentence in self.knowledge:
            if sentence.count == 0:
                for c in sentence.cells:
                    sentence.mark_safe(c)
            elif len(sentence.cells) == sentence.count:
                for c in sentence.cells:
                    sentence.mark_mine(c)
            #print(f'{sentence.count}, {sentence.cells}')
            #print(sentence)
            #print((i, j))
        '''


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """

        for c in self.safes:
            if c not in self.moves_made:
                print(f'safe move {c}')
                return c
        return None


    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        try:
            return random.choice([(i, j) for i in range(self.height) for j in range(self.width) if (i, j) not in self.mines and (i, j) not in self.moves_made])
        except IndexError:
            return None

