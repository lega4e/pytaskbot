# Класс уведомления

# 
# autor:   lis
# created: 2021.02.12 11:33:19
# 

import datetime as dt





class Notice:
	'''
	Members:
	  - cdate : datetime # Дата создания
	  - date  : datetime # Дата, когда нужно прислать уведомление
	  - text  : str      # Текст уведомления
	  - tags  : [ str ]  # Теги
	'''


	def __init__(self, date=None, text=None, tags=[], cdate=dt.datetime.today()):
		self.cdate = cdate
		self.date = date
		self.text = text
		self.tags = tags
		return


	def __str__(self):
		s = ', '.join( [ '#' + str(tag) for tag in self.tags ] )
		if len(s) != 0:
			s += '\n'

		if self.cdate is not None:
			s += 'Дата создания: ' + self.cdate.strftime('%d.%m.%Y, %H:%M:%S') + '\n'

		if self.date is not None:
			s += 'Срок:          ' + self.date.strftime('%d.%m.%Y, %H:%M:%S') + '\n'

		if len(s) != 0:
			s += '\n'

		s += self.text
		return s


	def __lt__(lhs, rhs):
		if lhs.date != rhs.date:
			return lhs.date < rhs.date
		return lhs.cdate < rhs.cdate





# END
