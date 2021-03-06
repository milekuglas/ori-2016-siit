"""
    @authors:    SW F/2013   Dragutin Marjanovic
                 SW 9/2013   Bojan Blagojevic
    @emails:     dmarjanovic94@gmail.com
                 datiglavaradi@gmail.com
"""

from __future__ import print_function

import copy, random


class State(object):
    """
    Klasa koja opisuje stanje table.
    """

    def __init__(self, board, parent=None):
        """
        :param board: Board (tabla)
        :param parent: roditeljsko stanje
        :return:
        """
        self.board = board  # sahovska tabla koja opisuje trenutno stanje
        self.parent = parent  # roditeljsko stanje
        self.value = 0.  # "vrednost" stanja - racuna ga evaluaciona funkcija calculate_value()

    def generate_next_states(self, max_player):
        """
        Generise moguca sledeca stanja (table) na osnovu svih mogucih poteza (u zavisnosti koji je igrac na potezu).
        :param max_player: bool. Da li je MAX igrac (crni)?
        :return: list. Lista mogucih sledecih stanja.
        """
        next_states = []
        
        check_side = 'b' if max_player else 'w'
        
        for row in range(self.board.rows):
            for col in range(self.board.cols):
                piece = self.board.determine_piece(row, col)  # odredi koja je figura
                if piece is None:
                    continue
                # generisi za crne ako je max igrac na potezu, generisi za bele ako je min igrac na potezu
                if (max_player and piece.side == 'b') or (not max_player and piece.side == 'w'):
                    legal_moves = piece.get_legal_moves()  # svi moguci potezi za figuru
                    for legal_move in legal_moves:
                        new_board = copy.deepcopy(self.board)
                        if(len(legal_move) == 3 ):
                            if(legal_move[2] == -1):
                                new_board.small_rocade_move(piece.side)
                            elif(legal_move[2] == 1):
                                new_board.big_rocade_move(piece.side)
                            elif(legal_move[2] == 0):
                                new_board.en_passant(row, col, legal_move[0], legal_move[1])
                        else:
                            new_board.move_piece(row, col, legal_move[0], legal_move[1])
                        
                        # Ne mozemo dodati u stanje ako je sah na tom stanju.
                        if not new_board.is_check(check_side):
                            next_state = State(new_board, self)
                            next_states.append(next_state)
                        
        # TODO 5: Lista stanja se random mijesa da bi se igrac ponasao drugacije
        random.shuffle(next_states)
        return next_states

    def calculate_value(self):
        """
        Evaluaciona funkcija za stanje.
        :return:
        """
        # TODO 3: Implementirati jednostavnu evaluacionu funkciju (suma vrednosti svih figura na tabli)
        for row in range(self.board.rows):
            for col in range(self.board.cols):
                piece = self.board.determine_piece(row, col)
                if piece is not None:
                    self.value += piece.get_value()
        return self.value
