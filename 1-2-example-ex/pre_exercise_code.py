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