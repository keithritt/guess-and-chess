from ui import UI
from util import Util
import math
import sys
import statistics

class Guesser():
  def __init__(self, test_mode=False):
    print('''
    Welcome to the guessing game!

    To start the game, please enter any integer n to establish the upper limit of the range of numbers I will guess from.
    After I make a guess please reply with one of the following options:
      'h' for too high
      'l' for too low
      'c' for a correct guess
    ''')
    self.test_mode = test_mode
    if self.test_mode:
      self.n = 100
    else:
      self.n = UI.ask_integer("Please enter a number n:")
    self.max_guesses = math.floor(math.log(self.n,2)) + 1
    self.game_count = 0
    self.total_guess_count = 0
    if self.test_mode:
      self.test_number =0
    self.start_new_game()

  def start_new_game(self):
    self.upper_limit = self.n
    self.lower_limit = 1
    self.game_count+=1
    self.current_guess_count = 0
    self.is_solved = False
    if self.test_mode:
      self.test_number+=1
      print('Test Number: {}'.format(self.test_number))
    while not self.is_solved:
      self.guess_number()

  def guess_number(self):
    if self.test_mode:
      print('ok - i will guess a number between {} and {}'.format(self.lower_limit, self.upper_limit))
    self.current_guess_count+=1
    self.total_guess_count+=1
    # guess the median value of the upper and lower limits
    self.current_guess = math.floor(statistics.mean([self.upper_limit, self.lower_limit]))
    if self.test_mode:
      print('{}?'.format(self.current_guess))
      resp = self.test_guess()
      print(resp)
    else:
      resp = UI.ask_limited_choices('{}?'.format(self.current_guess), ('h', 'l', 'c'))
    self.process_guess_response(resp)

  def test_guess(self):
    if self.current_guess > self.test_number:
      return 'h'
    elif self.current_guess < self.test_number:
      return 'l'
    else:
      return 'c'

  def process_guess_response(self, resp):
    if resp == 'h': # guess was too high
      #check to see if there is only 1 other solution
      if self.current_guess - self.lower_limit  == 1:
        return self.show_solution(self.lower_limit)
      self.upper_limit = self.current_guess - 1
    if resp == 'l': #guess was too low
      if self.upper_limit - self.current_guess == 1:
        #print('upper limit = {}'.format(self.upper_limit))
        return self.show_solution(self.upper_limit)
      self.lower_limit = self.current_guess + 1
    if resp == 'c' :# or self.lower_limit == self.upper_limit:
      self.show_solution(self.current_guess)

  def show_solution(self, solution):
    print('Your number is {}.'.format(solution))
    # check to see if the solution is correct
    if self.test_mode and solution != self.test_number:
      UI.exit('I solved incorrectly. I thought it was {} but it is actually {}'.format(solution, self.test_number))

    self.is_solved = True
    self.print_stats()
    self.offer_rematch()

  def print_stats(self):
    #check to see if the script solved it under the threshold
    if self.current_guess_count > self.max_guesses:
      UI.exit('Max guesses exceeded. I was supposed to guess your number in {} guesses and it took me {}'.format(self.max_guesses, self.current_guess_count))
    guess_text = Util.pluralize(self.current_guess_count, 'guess', 'guesses')
    print('It took me {} {}.'.format(self.current_guess_count, guess_text))
    avg_guesses = round(self.total_guess_count / self.game_count, 2)
    guess_text = Util.pluralize(self.total_guess_count, 'guess', 'guesses')
    game_text = Util.pluralize(self.game_count, 'game')
    print('I averaged {} {} per game for {} {}.'.format(avg_guesses, guess_text, self.game_count, game_text))

  def offer_rematch(self):
    if self.test_mode:
      if self.game_count < self.n:
        self.start_new_game()
      else:
        UI.exit('Thanks for playing!')
    else:
      if UI.ask_boolean('Play again? (y/n)'):
        self.start_new_game()
      else:
        print('Thanks for playing!')

if len(sys.argv) > 1 and sys.argv[1] == 'test':
  test_mode = True
else:
  test_mode = False
guesser = Guesser(test_mode)
