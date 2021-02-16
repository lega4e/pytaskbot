# Модуль, отвечающий за хранение записей
# и напоминаний, а также за управление
# этим хранилищем

# 
# autor:   lis
# created: 2021.02.12 10:07:54
# 

from notice import Notice
from sortedcontainers import SortedSet





# objects
storage = SortedSet();





# Добавление нового уведомления
def push(notice):
	global storage
	storage.add(notice)
	return



# Удаление существующего уведомления
def remove(notice):
	global storage
	storage.remove(notice)
	return



# Итерируемый объект по уведомлениям
def iter():
	global storage
	return storage





# END
