import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for var in self.domains:
            domain = list(self.domains[var])
            length = var.length
            for word in domain:
                if len(word) != length:
                    self.domains[var].remove(word)
                    continue

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # get the overlap between x and y
        overlap = self.crossword.overlaps[x, y]

        # count the revisions
        revision = 0

        domain = list(self.domains[x])
        for word in domain:
            count = 0  # count how many corresponding value for y
            for cor in self.domains[y]:
                if word[overlap[0]] == cor[overlap[1]]:
                    count += 1

            # if there are no corresponding values, then remove word
            if count == 0:
                self.domains[x].remove(word)
                revision += 1

        if revision == 0:
            return False
        else:
            return True


    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # if arcs is None, then add all arcs in the crossword
        if arcs is None:
            arcs = []
            for var1 in self.crossword.variables:
                for var2 in self.crossword.variables:
                    if var1 == var2:
                        continue
                    if self.crossword.overlaps[var1, var2] is not None:
                        arcs.append((var1, var2))

        # revise each pair in arcs
        for x, y in arcs:
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False    # impossible to solve

                 # make sure all the neighbors and x are also acr-consistent
                for neighbor in self.crossword.neighbors(x):
                    if neighbor != y:
                        arcs.append((x, neighbor))
        return True


    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        if len(assignment) == 0:
            return False

        for var in self.domains:
            if var not in assignment:
                return False
        return True


    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        for var in assignment:
            if assignment[var] is None:
                continue

            for var2 in assignment:
                # check distinct values
                if assignment[var] == assignment[var2] and var != var2:
                    return False

            # check values' length
            if len(assignment[var]) != var.length:
                return False

            # check conflicts
            for neighbor in self.crossword.neighbors(var):
                if neighbor not in assignment:
                    continue
                overlap = self.crossword.overlaps[var, neighbor]
                if assignment[var][overlap[0]] != assignment[neighbor][overlap[1]]:
                    return False

        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        order = list(self.domains[var].copy())
        number = {}   # assign each value to the number of ruled out neighbors
        for value in order:
            num = 0
            for neighbor in self.crossword.neighbors(var):
                overlap = self.crossword.overlaps[var, neighbor]
                match = False   # check if neighbor has at least 1 possible value
                for n_value in self.domains[neighbor]:
                    if value[overlap[0]] == n_value[overlap[1]]:
                        match = True
                if not match:
                    num += 1
            number[value] = num

        # sort the list
        order = sorted(order, key=lambda v: number[v])

        return order

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # get all the unassigned variables
        variables = []
        for var in self.domains:
            if var not in assignment:
                variables.append(var)

        # sort by number of domain values
        variables = sorted(variables, key=lambda variable: len(self.domains[variable]))

        # sort by degree
        if len(variables) >= 2:
            for i in range(len(variables)):
                if i == 0:
                    continue
                if len(self.domains[variables[i]]) != len(self.domains[variables[i-1]]):
                    variables = sorted(variables[0:i],\
                                     key=lambda variable: len(self.crossword.neighbors(variable)),\
                                     reverse = True)
                    break
        return variables[0]


    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment

        # select 1 variable
        var = self.select_unassigned_variable(assignment)

        # get all of its values
        values = self.order_domain_values(var, assignment)

        for value in values:
            assignment2 = assignment.copy()
            assignment2[var] = value

            # If that value makes the assignment consistent, then add it.
            # Otherwise, do not add it.
            if self.consistent(assignment2):
                # make inference by enforcing arc-consistency
                arcs = []
                
                # only consider the arc between var and its neighbors
                for neighbor in self.crossword.neighbors(var):
                    arcs.append((neighbor, var))

                if self.ac3(arcs):
                    for new_var in self.domains:
                        # add any possible inference to the list
                        if len(self.domains[new_var]) == 1:
                            new_values = self.domains[new_var].copy()
                            assignment2[new_var] = new_values.pop()

                        # if that inference makes the list inconsistent, then remove it.
                        if not self.consistent(assignment2):
                            del assignment2[new_var]

                # backtrack
                result = self.backtrack(assignment2)
                if result is not None:
                    return result
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
