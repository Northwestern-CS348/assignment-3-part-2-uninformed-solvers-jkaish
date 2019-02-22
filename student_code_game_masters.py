from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here
        ret = [[],[],[]]
        asks = [parse_input('fact: (on ?x peg1)'), parse_input('fact: (on ?x peg2)'), parse_input('fact: (on ?x peg3)')]
        for ii, a in enumerate(asks):
            bindings = self.kb.kb_ask(a)
            if bindings:
                for b in bindings:
                    disk = b.bindings[0].constant.element[-1]
                    ret[ii].append(int(disk))
            ret[ii].sort()

        ret = tuple([tuple(x) for x in ret])
        return ret


    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        terms = movable_statement.terms
        disk = terms[0].term.element
        from_peg = terms[1].term.element
        to_peg = terms[2].term.element

        to_retract = []
        to_retract.append(parse_input('fact: (on {} {}'.format(disk, from_peg)))
        to_retract.append(parse_input('fact: (top {} {}'.format(disk, from_peg)))

        to_assert = []
        to_assert.append(parse_input('fact: (on {} {}'.format(disk, to_peg)))
        to_assert.append(parse_input('fact: (top {} {}'.format(disk, to_peg)))

        to_peg_empty = parse_input('fact: (empty {})'.format(to_peg))
        if self.kb.kb_ask(to_peg_empty):
            to_retract.append(to_peg_empty)
            to_assert.append(parse_input('fact: (bottom {} {}'.format(disk, to_peg)))
        else:
            old_top = parse_input('fact: (top ?x {})'.format(to_peg))
            res = self.kb.kb_ask(old_top)
            c = res[0].bindings[0].constant.element
            to_assert.append(parse_input('fact: (under {} {})'.format(c, disk)))
            to_retract.append(parse_input('fact: (top {} {})'.format(c, to_peg)))

        from_peg_empty = parse_input('fact: (bottom {} {})'.format(disk, from_peg))
        if self.kb.kb_ask(from_peg_empty):
            to_retract.append(from_peg_empty)
            to_assert.append(parse_input('fact: (empty {})'.format(from_peg)))
        else:
            new_top = parse_input('fact: (under ?x {})'.format(disk))
            bindings = self.kb.kb_ask(new_top)
            c = bindings[0].bindings[0].constant.element
            to_assert.append(parse_input('fact: (top {} {})'.format(c, from_peg)))
            to_retract.append(parse_input('fact: (under {} {})'.format(c, disk)))

        for tr in to_retract:
            self.kb.kb_retract(tr)

        for ta in to_assert:
            self.kb.kb_assert(ta)
            

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))


    def createFutureGameState(self, curr_state, movable_statement):
        terms = movable_statement.terms
        disk = int(terms[0].term.element[-1])
        from_peg = int(terms[1].term.element[-1]) - 1
        to_peg = int(terms[2].term.element[-1]) - 1

        temp = [list(x) for x in curr_state]

        temp[from_peg].remove(disk)
        temp[to_peg].append(disk)
        temp[to_peg].sort()

        return tuple([tuple(x) for x in temp])


class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here
        ret = [[], [], []]
        loc_queries = ['fact: (locatedat ?x {} pos1)', 'fact: (locatedat ?x {} pos2', 'fact: (locatedat ?x {} pos3)']
        x_pos = ['pos1', 'pos2', 'pos3']

        for ii, lq in enumerate(loc_queries):
            for x in x_pos:
                temp = lq.format(x)
                q = parse_input(temp)
                resp = self.kb.kb_ask(q)
                tile = resp[0].bindings[0].constant.element
                ret[ii].append(int(tile[-1]) if tile != 'empty' else -1)

        ret = tuple([tuple(x) for x in ret])
        return ret

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        terms = movable_statement.terms
        tile = terms[0]
        old_x = terms[1]
        old_y = terms[2]
        new_x = terms[3]
        new_y = terms[4]

        to_assert = []
        to_assert.append(parse_input('fact: (locatedat {} {} {})'.format(tile, new_x, new_y)))
        to_assert.append(parse_input('fact: (locatedat empty {} {})'.format(old_x, old_y)))

        to_retract = []
        to_retract.append(parse_input('fact: (locatedat {} {} {})'.format(tile, old_x, old_y)))
        to_retract.append(parse_input('fact: (locatedat empty {} {})'.format(new_x, new_y)))

        for tr in to_retract:
            self.kb.kb_retract(tr)

        for ta in to_assert:
            self.kb.kb_assert(ta)
        

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))

    def createFutureGameState(self, curr_state, movable_statement):
        terms = movable_statement.terms
        tile = int(terms[0].term.element[-1])
        old_x = int(terms[1].term.element[-1]) - 1
        old_y = int(terms[2].term.element[-1]) - 1
        new_x = int(terms[3].term.element[-1]) - 1
        new_y = int(terms[4].term.element[-1]) - 1

        temp = [list(x) for x in curr_state]
        temp[new_y][new_x] = tile
        temp[old_y][old_x] = -1

        return tuple([tuple(x) for x in temp])

