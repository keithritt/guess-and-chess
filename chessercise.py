import sys
from chesser import Chesser

if len(sys.argv) > 4:
  piece = sys.argv[2]
  position = sys.argv[4]
  chesser = Chesser(piece, position)

  if chesser.validate_arguments():
    print(chesser.get_available_moves())
  else:
    print(chesser.invalid_message)

else:
  Chesser.test_all()
