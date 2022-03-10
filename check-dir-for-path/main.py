from tcs_pythonwhat.signatures import sig_from_params
from tcs_pythonwhat.test_exercise import prep_context

_, ctxt = prep_context()
globals().update(ctxt)
# pre_code - Что не видит студент ------------------------------------------------------------------
'''
from scrapy import Selector

html = """
<html>
  <body>
      <p>Привет Мир!</p>
      <p>Выбирайте DeepSkills!</p>
      <p>Спасибо за просмотр!</p> 
  </body>
</html>
"""

sel = Selector( text = html )

def how_many_elements( xpath ):
  print( len(sel.xpath( xpath )) )
'''

# sample_code - Что видит студент в начале -------------------------------------------------------------
'''
# Создайте строку XPath для направления к дочерним элементам элемента body
xpath = ____

# Выведите количество выбранных элементов
how_many_elements( xpath )
'''

# sol_code - Код который верный --------------------------------------------------------------------
sol_code = r'''
from scrapy import Selector

html = """
<html>
  <body>
      <p>Привет Мир!</p>
      <p>Выбирайте DeepSkills!</p>
      <p>Спасибо за просмотр!</p> 
  </body>
</html>
"""

sel = Selector( text = html )

def how_many_elements( xpath ):
  print( len(sel.xpath( xpath )) )


# solution --------------------------------------------
# Решение
# Создайте строку XPath для направления к дочерним элементам элемента body
xpath = '/html/body/*'

# Выведите количество выбранных элементов
how_many_elements( xpath )
'''

# stu_code - Код который тестиреум -----------------------------------------------------------------
stu_code = '''
from scrapy import Selector

html = """
<html>
  <body>
      <p>Привет Мир!</p>
      <p>Выбирайте DeepSkills!</p>
      <p>Спасибо за просмотр!</p> 
  </body>
</html>
"""

sel = Selector( text = html )

def how_many_elements( xpath ):
  print( len(sel.xpath( xpath )) )


# Создайте строку XPath для направления к дочерним элементам элемента body
xpath = '/html/body/*'

# Выведите количество выбранных элементов
how_many_elements( xpath )
'''

# Tests --------------------------------------------------------------------------------------------
from tcs_pythonwhat.test_exercise import setup_state

setup_state(stu_code=stu_code, sol_code=sol_code)
# expectation -----------------------------------------
Ex().check_object('xpath').has_equal_value()
Ex().check_function('how_many_elements').has_equal_ast()
Ex().check_function('how_many_elements').has_equal_value()  # Не уверен в необходимости

success_msg("""
            Вы смогли обратиться ко всем дочерним элементам элемента body!
            Вам, должно быть, становится удобнее работать с символом подстановки!
            """)


