class Util:

  @staticmethod
  def is_int(text):
    try:
        int(text)
        return True
    except ValueError:
        return False

  @staticmethod
  def pluralize(number, singular, plural=None):
    if number == 1:
      return singular

    if plural is None:
      plural = singular + 's'

    return plural