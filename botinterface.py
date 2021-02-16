# Модуль, который осуществляет взаимодействие
# с пользователем (получение команд, отсылка
# сообщений)

# 
# autor:   lis
# created: 2021.02.12 09:50:42
# 





# Отправляет сообщение в беседу
def send(text):
	print(text)



# Возвращает команду, если есть; если
# нет, то возвращает None
def get_command():
	try:
		s = ''
		while s == '':
			s = input()
		#  print('input:', s)
		return s
	except EOFError:
		return None





# END
