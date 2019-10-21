from util import Util
import sys

class UI:

  @staticmethod
  def ask(question):
    ret = input(question+' ')
    if ret == 'exit':
      UI.exit()
    return ret

  @staticmethod
  def ask_integer(question):
    ret = UI.ask(question)

    if not Util.is_int(ret):
      print('Please enter an integer.')
      ret = UI.ask_integer(question)

    return int(ret)

  @staticmethod
  def ask_boolean(question):
    ret = UI.ask(question)
    ret = ret.lower()

    if ret == 'y':
      return True

    if ret == 'n':
      return False

    # if user is still here - they entered an invalid value
    UI.exit()

  @staticmethod
  def ask_limited_choices(question, choices):
    ret = UI.ask(question)
    ret = ret.lower()

    if ret in (choices):
      return ret

    # if user is still here - they entered an invalid value
    print("Please answer with one of the following options: {}".format(choices))
    return UI.ask_limited_choices(question, choices)

  @staticmethod
  def exit(msg=None):
    if msg is not None:
      print(msg)
    sys.exit()