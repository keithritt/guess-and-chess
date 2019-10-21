class Chesser():
  all_cols = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
  all_pieces = ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']

  def __init__(self, piece, position):
    self.piece = piece.lower()
    self.position = position.upper()
    self.col, self.row = Chesser.split_position(self.position)

  def validate_arguments(self):
    if self.piece not in self.all_pieces:
      self.invalid_message = 'Unknown piece: {}. Valid option are: {}'.format(self.piece, self.all_pieces)
      return False
    if self.col not in self.all_cols:
      self.invalid_message = 'Row must be between A and H. {} was given'.format(self.col)
      return False

    if self.row not in range(1, 9):
      print(range(0,8))
      self.invalid_message = 'Row must be between 1 and 8. {} was given'.format(self.row)
      return False

    # special cases for pawns - they start in row 2 and turn into a different piece in row 8
    if self.piece == 'pawn' and self.row in [1,8]:
      self.invalid_message = 'A pawn cannot be in row: {}'.format(self.row)
      return False

    return True

  def set_move_limits(self):
    self.max_spaces = 7 # default

    if(self.piece == 'pawn'):
      self.directions = ['n']
      # allow pawns to move 2 spaces on initial move
      self.max_spaces = 2 if self.row == 2 else 1
    if(self.piece == 'rook'):
      self.directions = ['n', 'e', 's', 'w']
    if(self.piece == 'bishop'):
      self.directions = ['ne', 'se', 'sw', 'nw']
    if(self.piece == 'queen'):
      self.directions = ['n', 'ne', 'e',  'se', 's', 'sw', 'w', 'nw']
    if(self.piece == 'king'):
      self.directions = ['n', 'ne', 'e',  'se', 's', 'sw', 'w', 'nw']
      self.max_spaces = 1

  @staticmethod
  def split_position(position):
    return (position[0], int(position[1]))

  @staticmethod
  def combine_position(col, row):
    return col+str(row)

  @staticmethod
  def get_knight_move(position, direction):
    first_direction = direction[0]
    second_direction = direction[1]

    # move first direction twice and second direction once
    tmp_position = Chesser.get_next_position(position, first_direction)
    tmp_position = Chesser.get_next_position(tmp_position, first_direction)
    return Chesser.get_next_position(tmp_position, second_direction)

  def get_available_moves(self):
    ret = []
    if self.piece == 'knight':
      # a knight in the center of the board has exactly 8 moves available - will denote these using 2 direction chars
      # first part indicate the 2 space move, 2nd part is the 1 space move
      # ie 'nw' means 2 spaces north 1 space west 'ws' means twos spaces west 1 space south
      directions = ('nw', 'ne', 'en', 'es', 'se', 'sw', 'ws', 'wn')

      for direction in directions:
        available_move = Chesser.get_knight_move(self.position, direction)
        if available_move is not None:
          ret.append(available_move)
    else:
      self.set_move_limits()
      for direction in self.directions:
        num_moves = 0
        tmp_position = self.position
        while(True):
          num_moves+=1
          next_position = Chesser.get_next_position(tmp_position, direction)

          if next_position is not None:
            ret.append(next_position)
            tmp_position = next_position
          else:
            break

          if num_moves == self.max_spaces:
            break

    return ret

  @staticmethod
  def get_next_position(position, direction):
    # edge case for knights - if the starting position is invalid - so is the next position
    if position is None:
      return None

    col, row = Chesser.split_position(position)

    #check for edges of board
    if 'n' in direction and row == 8:
      return None
    if 's' in direction and row == 1:
      return None
    if 'e' in direction and col == 'H':
      return None
    if 'w' in direction and col == 'A':
      return None

    # adjust col/row
    if 'n' in direction:
      row+=1
    if 's' in direction:
      row-=1
    if 'e' in direction:
      col = Chesser.all_cols[Chesser.all_cols.index(col) + 1]
    if 'w' in direction:
      col = Chesser.all_cols[Chesser.all_cols.index(col) - 1]

    return Chesser.combine_position(col, row)

  @staticmethod
  def test_all():
    #print('test_all()')
    for piece in Chesser.all_pieces:
      #print(piece)
      for col in Chesser.all_cols:
        #print(col)
        for row in range(1,9):
          position = Chesser.combine_position(col, row)
          print('Now testing piece: {} at position: {}'.format(piece, position))
          chesser = Chesser(piece, position)

          if chesser.validate_arguments():
            print(chesser.get_available_moves())
          else:
            print(chesser.invalid_message)




