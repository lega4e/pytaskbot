# Класс команды

# 
# autor:   lis
# created: 2021.02.12 11:36:12
# 





class CType:
	CNOTICE = 'CNOTICE' # create notice
	RNOTICE = 'RNOTICE' # remove notice
	LNOTICE = 'LNOTICE' # list notice



class Command:
	'''
	Members:
	  type : CType    # Тип команды
	  date : datetime # Аргумент даты
	  text : str      # Текстовый аргумент
	  tags : [ str ]  # Аргумент в виде тегов

	Возможные типы команд:
	  CNOTICE date text [tags]
	  RNOTICE date [tags]
	  #  RNOTICE text [tags]
	  #  RNOTICE date text [tags]
	'''

	def __init__(self, type=None, date=None, text=None, tags=[]):
		self.type = type
		self.date = date
		self.text = text
		self.tags = tags
		return

	def __str__(self):
		return (
			"Тип:   %s\n" + "Дата:  %s\n" +
			"Текст: %s\n" + "Теги:  %s\n"
		) % (
			self.type, 
			self.date.strftime("%d.%m.%Y, %X"),
			self.text, ', '.join(self.tags)
		)





# END
