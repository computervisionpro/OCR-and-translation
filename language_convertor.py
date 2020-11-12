from translate import Translator

class Tr:
   def __init__(self, language):
      self.translator = Translator(from_lang=language, to_lang='en')

   def trans(self, sent):
      try:
         ans = self.translator.translate(sent)
         return ans
      except AttributeError:
         return 'Can\'t translate !'
         
      
