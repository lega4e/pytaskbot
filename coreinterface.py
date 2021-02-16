# Модуль, отвечающий за взаимодействие с
# ядром приложения: разбор команд, хранение
# заметок и напоминаний и т.д.

# 
# autor:   lis
# created: 2021.02.12 10:00:53
# 

import storage
import parser

from botinterface import *
from command import Command, CType
from notice import Notice





# objects
last_notice = None




# Выполняет команду; команда представляет собой
# непосредственно тот текст, который ввёл пользователь;
# при неудаче возбуждает исключение (какое?)
def execute(text):
	try:
		com = parser.parse(text)
		if com is None:
			raise Exception("com is None")
	except Exception:
		print("Error")
		return

	if com.type == CType.CNOTICE:
		storage.push(Notice(date=com.date, text=com.text, tags=com.tags))
		#  send(
			#  'Успешно создано напоминание на %s с текстом "%s"' %
			#  ( com.date.strftime('%d.%M.%Y %X'), com.text )
		#  )
		send('%s — %s' % ( com.date.strftime('%d.%m.%Y %X'), com.text ))
		#  send('')

	elif com.type == CType.RNOTICE:
		torm = []
		for notice in storage.iter():
			if notice.date == com.date:
				torm.append(notice)
			elif notice.date > com.date:
				break
		if len(torm) == 0:
			print("Can't find notice to remove")
		elif len(torm) > 1:
			print("Date is ambigous")
		else:
			storage.remove(torm[0])

	elif com.type == CType.LNOTICE:
		for notice in storage.iter():
			print(notice, end='\n\n')

	else:
		raise Exception("Error: unknown command type")



# Возвращает и удаляет из очереди напоминание,
# если есть; иначе возвращает None
def get_notice():
	if len(storage.storage) == 0:
		return None
	global last_notice
	last_notice = storage.storage.pop(0)
	return last_notice



# Возвращает только что удалённое
# из очереди напоминание обратно;
# если такового нет, то возбуждается
# исключение
def unget_notice():
	if last_notice is None:
		raise Exception('Last notice is None')
	storage.push(last_notice)





# END
