# Модуль, отвечающий за разбор
# команды, введённой пользователем

# 
# autor:   lis
# created: 2021.02.12 11:36:00
# 

from command import Command, CType
from copy import deepcopy as dpcopy
from pymorphy2 import MorphAnalyzer

from ply import lex, yacc

import datetime as dt
import re
import time





# Settings, global objects
default_time = 9





# Разбирает команду и возвращает объект
# command; в случае неудачи возбуждает
# исключение (какое?)
def parse(text):
	global word_was
	word_was = False
	res = parser.parse(text)
	if res is None:
		return None
	if len(res.text) == 0:
		res.text = ''
	else:
		res.text = text[text.find(res.text[0]):]
	return res





# ====================== IMPLEMENT =====================

# GLOBAL OBJECTS
tokens = [
	#  'COMMAND',      # напомнить, уведомить
	'NUMBER',       # 1, 2...
	'NUMBER_WORD',  # один, два...
	#  'NOT',          # не, нет
	'MONTH_NAME',   # январь, февраль...
	'WEEKDAY',      # понедельник, вторник...
	'TIME_NAME',    # день, неделя, месяц
	'DAYTIME_NAME', # утром, вечером, ночью
	'RELDATE',      # Сегодня, вчера, завтра...
	'IN',           # В
	#  'SINCE',        # От
	#  'DEADLINE',     # Срок, до
	'AFTER',        # Через
	'WORD'          # Все остальные слова
	#  'TAG', 'STRICT_TAG', 'TAG_NAME',
]



marks = [
	#  { 'type' : 'COMMAND', 'value' : 'push', 'words' : [ 'записать', 'написать', ] },
	#  {
		#  'type' : 'COMMAND',
		#  'value' : 'erase',
		#  'words' : [
			#  'удалить', 'выбросить', 'выкинуть',
			#  'удали', 'выброси', 'выбрось', 'выкини', 'выкинь'
		#  ]
	#  },
	#  {
		#  'type' : 'COMMAND',
		#  'value' : 'append',
		#  'words' : [ 'добавить', 'прибавить', 'дополнить' ]
	#  },
	#  {
		#  'type' : 'COMMAND',
		#  'value' : 'rewrite',
		#  'words' : [ 'переписать' ]
	#  },
	#  {
		#  'type' : 'COMMAND',
		#  'value' : 'print',
		#  'words' : [ 'показать', 'напечатать', 'распечатать' ]
	#  },
	#  { 'type' : 'COMMAND', 'value' : 'notice', 'words' : [ 'напомнить', 'напоминать' ] },

	#  { 'type' : 'TAG',        'value' : 'tag',      'words' : [ 'по'         ] },
	#  { 'type' : 'STRICT_TAG', 'value' : 'stag',     'words' : [ 'тег'        ] },
	{ 'type' : 'DEADLINE',   'value' : 'deadline', 'words' : [ 'срок', 'до' ] },
	{ 'type' : 'NOT',        'value' : 'not',      'words' : [ 'не', 'нет'  ] },
	{ 'type' : 'AFTER',      'value' : 'after',    'words' : [ 'через'      ] },
	{ 'type' : 'IN',         'value' : 'in',       'words' : [ 'в'          ] },
	{ 'type' : 'SINCE',      'value' : 'since',    'words' : [ 'от'         ] },

	{ 'type' : 'NUMBER_WORD', 'value' : 1, 'words' : [ 'один'               ] },
	{ 'type' : 'NUMBER_WORD', 'value' : 2, 'words' : [ 'два',    'двое'     ] },
	{ 'type' : 'NUMBER_WORD', 'value' : 3, 'words' : [ 'три',    'трое'     ] },
	{ 'type' : 'NUMBER_WORD', 'value' : 4, 'words' : [ 'четыре', 'четверо'  ] },
	{ 'type' : 'NUMBER_WORD', 'value' : 5, 'words' : [ 'пять',   'пятеро'   ] },
	{ 'type' : 'NUMBER_WORD', 'value' : 6, 'words' : [ 'шесть',  'шестеро'  ] },
	{ 'type' : 'NUMBER_WORD', 'value' : 7, 'words' : [ 'семь',   'семеро'   ] },
	{ 'type' : 'NUMBER_WORD', 'value' : 8, 'words' : [ 'восемь', 'восьмеро' ] },
	{ 'type' : 'NUMBER_WORD', 'value' : 9, 'words' : [ 'девять', 'девятеро' ] },

	{ 'type' : 'NUMBER_WORD', 'value' : 10, 'words' : [ 'десять',       'десятый'       ] },
	{ 'type' : 'NUMBER_WORD', 'value' : 11, 'words' : [ 'одиннадцать',  'одиннадцатый'  ] },
	{ 'type' : 'NUMBER_WORD', 'value' : 12, 'words' : [ 'двенадцать',   'двенадцатый'   ] },
	{ 'type' : 'NUMBER_WORD', 'value' : 13, 'words' : [ 'тринадцать',   'тринадцатый'   ] },
	{ 'type' : 'NUMBER_WORD', 'value' : 14, 'words' : [ 'четырнадцать', 'четырнадцатый' ] },
	{ 'type' : 'NUMBER_WORD', 'value' : 15, 'words' : [ 'пятнадцать',   'пятнадцатый'   ] },
	{ 'type' : 'NUMBER_WORD', 'value' : 16, 'words' : [ 'шестнадцать',  'шестнадцатый'  ] },
	{ 'type' : 'NUMBER_WORD', 'value' : 17, 'words' : [ 'семнадцать',   'семнадцатый'   ] },
	{ 'type' : 'NUMBER_WORD', 'value' : 18, 'words' : [ 'восемнадцать', 'восемнадцатый' ] },
	{ 'type' : 'NUMBER_WORD', 'value' : 19, 'words' : [ 'девятнадцать', 'девятнадцатый' ] },

	{ 'type' : 'NUMBER_WORD', 'value' : 20, 'words' : [ 'двадцать',     'двадцатый'     ] },
	{ 'type' : 'NUMBER_WORD', 'value' : 30, 'words' : [ 'тридцать',     'тридцатый'     ] },
	{ 'type' : 'NUMBER_WORD', 'value' : 40, 'words' : [ 'сорок',        'сороковой'     ] },
	{ 'type' : 'NUMBER_WORD', 'value' : 50, 'words' : [ 'пятьдесят',    'пятьдесятый'   ] },
	{ 'type' : 'NUMBER_WORD', 'value' : 60, 'words' : [ 'шестьдесят',   'шестьдесятый'  ] },
	{ 'type' : 'NUMBER_WORD', 'value' : 70, 'words' : [ 'семьдесят',    'семьдесятый'   ] },
	{ 'type' : 'NUMBER_WORD', 'value' : 80, 'words' : [ 'восемьдесят',  'восемьдесятый' ] },
	{ 'type' : 'NUMBER_WORD', 'value' : 90, 'words' : [ 'девяносто',    'девяностый'    ] },

	{ 'type' : 'NUMBER_WORD', 'value' : 100, 'words' : [ 'сто', 'сотня', 'сотка' ] },
	{ 'type' : 'NUMBER_WORD', 'value' : 200, 'words' : [ 'двести'                ] },
	{ 'type' : 'NUMBER_WORD', 'value' : 300, 'words' : [ 'триста'                ] },
	{ 'type' : 'NUMBER_WORD', 'value' : 400, 'words' : [ 'четыреста'             ] },
	{ 'type' : 'NUMBER_WORD', 'value' : 500, 'words' : [ 'пятьсот'               ] },
	{ 'type' : 'NUMBER_WORD', 'value' : 600, 'words' : [ 'шестьсот'              ] },
	{ 'type' : 'NUMBER_WORD', 'value' : 700, 'words' : [ 'семьсот'               ] },
	{ 'type' : 'NUMBER_WORD', 'value' : 800, 'words' : [ 'восемьсот'             ] },
	{ 'type' : 'NUMBER_WORD', 'value' : 900, 'words' : [ 'девятьсот'             ] },

	{ 'type' : 'NUMBER_WORD', 'value' : 1000,          'words' : [ 'тысяча'   ] },
	{ 'type' : 'NUMBER_WORD', 'value' : 1000000,       'words' : [ 'миллион'  ] },
	{ 'type' : 'NUMBER_WORD', 'value' : 1000000000,    'words' : [ 'миллиард' ] },
	{ 'type' : 'NUMBER_WORD', 'value' : 1000000000000, 'words' : [ 'триллион' ] },

	{ 'type' : 'MONTH_NAME', 'value' : 1,  'words' : [ 'январь'   ] },
	{ 'type' : 'MONTH_NAME', 'value' : 2,  'words' : [ 'февраль'  ] },
	{ 'type' : 'MONTH_NAME', 'value' : 3,  'words' : [ 'март'     ] },
	{ 'type' : 'MONTH_NAME', 'value' : 4,  'words' : [ 'апрель'   ] },
	{ 'type' : 'MONTH_NAME', 'value' : 5,  'words' : [ 'май'      ] },
	{ 'type' : 'MONTH_NAME', 'value' : 6,  'words' : [ 'июнь'     ] },
	{ 'type' : 'MONTH_NAME', 'value' : 7,  'words' : [ 'июль'     ] },
	{ 'type' : 'MONTH_NAME', 'value' : 8,  'words' : [ 'август'   ] },
	{ 'type' : 'MONTH_NAME', 'value' : 9,  'words' : [ 'сентябрь' ] },
	{ 'type' : 'MONTH_NAME', 'value' : 10, 'words' : [ 'октябрь'  ] },
	{ 'type' : 'MONTH_NAME', 'value' : 11, 'words' : [ 'ноябрь'   ] },
	{ 'type' : 'MONTH_NAME', 'value' : 12, 'words' : [ 'декабрь'  ] },

	{ 'type' : 'WEEKDAY', 'value' : 0, 'words' : [ 'понедельник' ] },
	{ 'type' : 'WEEKDAY', 'value' : 1, 'words' : [ 'вторник'     ] },
	{ 'type' : 'WEEKDAY', 'value' : 2, 'words' : [ 'среда'       ] },
	{ 'type' : 'WEEKDAY', 'value' : 3, 'words' : [ 'четверг'     ] },
	{ 'type' : 'WEEKDAY', 'value' : 4, 'words' : [ 'пятница'     ] },
	{ 'type' : 'WEEKDAY', 'value' : 5, 'words' : [ 'суббота'     ] },
	{ 'type' : 'WEEKDAY', 'value' : 6, 'words' : [ 'воскресение' ] },

	{ 'type' : 'TIME_NAME', 'value' : 'sec',   'words' : [ 'секунда', 'секунды'        ] },
	{ 'type' : 'TIME_NAME', 'value' : 'min',   'words' : [ 'минута',  'минуты'         ] },
	{ 'type' : 'TIME_NAME', 'value' : 'hour',  'words' : [ 'час',     'часы'           ] },
	{ 'type' : 'TIME_NAME', 'value' : 'day',   'words' : [ 'день',    'дни',   'сутки' ] },
	{ 'type' : 'TIME_NAME', 'value' : 'week',  'words' : [ 'неделя',  'недели'         ] },
	{ 'type' : 'TIME_NAME', 'value' : 'month', 'words' : [ 'месяц',   'месяцы'         ] },

	{ 'type' : 'DAYTIME_NAME', 'value' : 'morning',   'words' : [ 'утро', 'утром'    ] },
	{ 'type' : 'DAYTIME_NAME', 'value' : 'afternoon', 'words' : [ 'полдень'          ] },
	{ 'type' : 'DAYTIME_NAME', 'value' : 'evening',   'words' : [ 'вечер', 'вечером' ] },
	{ 'type' : 'DAYTIME_NAME', 'value' : 'night',     'words' : [ 'ночь', 'ночью'    ] },

	{ 'type' : 'RELDATE', 'value' : 0,  'words' : [ 'сегодня'     ] },
	{ 'type' : 'RELDATE', 'value' : 1,  'words' : [ 'завтра'      ] },
	{ 'type' : 'RELDATE', 'value' : -1, 'words' : [ 'вчера'       ] },
	{ 'type' : 'RELDATE', 'value' : 2,  'words' : [ 'послезавтра' ] },
	{ 'type' : 'RELDATE', 'value' : -2, 'words' : [ 'позавчера'   ] }
]

prenorm_marks = [
	{ 'value' : 'январь',   'words' : [ 'янв'         ] },
	{ 'value' : 'февраль',  'words' : [ 'фев'         ] },
	{ 'value' : 'март',     'words' : [ 'мар'         ] },
	{ 'value' : 'апрель',   'words' : [ 'апр'         ] },
	{ 'value' : 'май',      'words' : [ 'май'         ] },
	{ 'value' : 'июнь',     'words' : [ 'июн'         ] },
	{ 'value' : 'июль',     'words' : [ 'июл'         ] },
	{ 'value' : 'август',   'words' : [ 'авг'         ] },
	{ 'value' : 'сентябрь', 'words' : [ 'сен', 'сент' ] },
	{ 'value' : 'октябрь',  'words' : [ 'окт'         ] },
	{ 'value' : 'ноябрь',   'words' : [ 'ноя'         ] },
	{ 'value' : 'декабрь',  'words' : [ 'дек'         ] },

	{ 'value' : 'понедельник', 'words' : [ 'пон', 'пн', 'пнд' ] },
	{ 'value' : 'вторник',     'words' : [ 'вт', 'втор'       ] },
	{ 'value' : 'среда',       'words' : [ 'ср', 'срд'        ] },
	{ 'value' : 'четверг',     'words' : [ 'чт', 'чтв'        ] },
	{ 'value' : 'пятница',     'words' : [ 'пт', 'пят'        ] },
	{ 'value' : 'суббота',     'words' : [ 'сб', 'суб', 'сбт' ] },
	{ 'value' : 'воскресение', 'words' : [ 'вс', 'вос', 'вск' ] },

	{ 'value' : 'секунда', 'words' : [ 'сек', 'с' ] },
	{ 'value' : 'минута',  'words' : [ 'мин', 'м' ] },
	{ 'value' : 'час',     'words' : [ 'чс',  'ч' ] }
]

daytime_values = {
	'morning'   : 6,
	'afternoon' : 12,
	'evening'   : 18,
	'night'     : 23
};

daytime_mapping = { 
	'morning' : [
		{ 'condition' : '0 <= %s <= 2',   'mapping': '( (%s + 12) %% 24 )'  },
		{ 'condition' : '3 <= %s < 24',   'mapping': '( %s )'               }
	],
	'afternoon' : [
		{ 'condition' : '0 <= %s <= 7',   'mapping' : '( (%s + 12) %% 24 )' },
		{ 'condition' : '8 <= %s <= 24',  'mapping' : '( %s )'              }
	],
	'evening' : [
		{ 'condition' : '0 <= %s <= 2',   'mapping' : '( %s )'              },
		{ 'condition' : '3 <= %s <= 12',  'mapping' : '( (%s + 12) %% 24 )' },
		{ 'condition' : '13 <= %s <= 24', 'mapping' : '( %s )'              }
	],
	'night' : [
		{ 'condition' : '0 <= %s <= 6',   'mapping' : '( %s )'              },
		{ 'condition' : '7 <= %s <= 12',  'mapping' : '( (%s + 12) %% 24 )' },
		{ 'condition' : '13 <= %s <= 24', 'mapping' : '( %s )'              }
	]
}



morph = MorphAnalyzer()





# CLASSES
class Date:
	year     = None
	month    = None # 1, 2, ..., 12
	day      = None # 1, 2, ..., 31
	weekday  = None # 0 - mon, 1 - tue...
	daytime  = None # morning, afternoon, evening, night
	hours    = None
	minutes  = None
	seconds  = None
	relsec   = None
	relmin   = None
	relhour  = None
	datetype = None # abs, rel, cor

	def __init__(self, datetype):
		self.datetype = datetype
		return

	def __str__(self):
		return (
			( '\ntype:    ' + str(self.datetype)                                    ) +
			( '\nyear:    ' + str(self.year)    if self.year    is not None else '' ) +
			( '\nmonth:   ' + str(self.month)   if self.month   is not None else '' ) +
			( '\nday:     ' + str(self.day)     if self.day     is not None else '' ) +
			( '\nweekday: ' + str(self.weekday) if self.weekday is not None else '' ) +
			( '\ndaytime: ' + str(self.daytime) if self.daytime is not None else '' ) +
			( '\nhours:   ' + str(self.hours)   if self.hours   is not None else '' ) +
			( '\nminutes: ' + str(self.minutes) if self.minutes is not None else '' )
			( '\nseconds: ' + str(self.minutes) if self.minutes is not None else '' )
		).lstrip()

	def pydate(self, future=True, now=dt.datetime.now()) -> dt.datetime:
		'''
		  Функция на основании внутренних данных
		  создаёт объект типа datetime
		'''
		if self.datetype == 'abs':
			year  = self.year  if self.year  is not None else now.year
			month = self.month if self.month is not None else now.month
			day   = self.day   if self.day   is not None else now.day
		else:
			year  = now.year
			month = now.month
			day   = now.day

		if self.daytime is not None:
			if self.hours is not None:
				hours = self._get_hours()
			else:
				hours = daytime_values[self.daytime]
		else:
			if self.hours is None:
				hours = None
			else:
				hours = self.hours+12 if self.hours < 12 else self.hours

		td = None
		minutes = self.minutes if self.minutes is not None else 0
		seconds = self.seconds if self.seconds is not None else 0
		if self.datetype == 'rel' or self.datetype == 'relcor':
			if self.year is not None:
				year += self.year
			if self.month is not None:
				month += self.month
				year += (month - 1) // 12
				month = (month - 1) % 12 + 1
			if hours is None and (
				self.relhour is not None or
				self.relmin  is not None or
				self.relsec  is not None
			):
				hours = now.hour
				minutes = now.minute
				seconds = now.second
			else:
				if hours is None:
					hours = default_time

			td = dt.timedelta(
				days    = self.day     if self.day     is not None else 0,
				hours   = self.relhour if self.relhour is not None else 0,
				minutes = self.relmin  if self.relmin  is not None else 0,
				seconds = self.relsec  if self.relsec  is not None else 0
			)

		if hours is None:
			hours = default_time

		date = dt.datetime(year, month, day, hours, minutes, seconds)
		if td is not None:
			date += td

		if self.weekday is not None:
			exdays = (self.weekday - date.weekday() + 7) % 7
			exdays = 7 if exdays == 0 else exdays
			date += dt.timedelta(days=exdays)

		if future and date < now:
			if self.datetype == 'abs':
				date = dt.datetime(
					date.year+1, date.month, date.day,
					date.hour, date.minute, date.second
				)
			else:
				date += dt.timedelta(days=1)

		return date



	# implementation
	def __getitem__(self, name):
		return eval( 'self.' + str(name) )

	def __setitem__(self, name, value):
		return exec( 'self.' + str(name) + ' = value' )

	@staticmethod
	def _rewrite_items(lhs, rhs, items):
		for item in items:
			if rhs[item] is not None:
				lhs[item] = rhs[item]

	@staticmethod
	def _stack_items(lhs, rhs, items):
		for item in items:
			if lhs[item] is None:
				lhs[item] = rhs[item]
			elif rhs[item] is not None:
				lhs[item] += rhs[item]

	def _get_hours(self):
		#  print(self.daytime, self.hours)
		for item in daytime_mapping[self.daytime]:
			if eval(item['condition'] % self.hours):
				return eval(item['mapping'] % 'self.hours')
		raise Exception('Invalid hours')

	def __or__(self, rhs):
		if self.datetype is None or rhs.datetype is None:
			return None

		lhs = dpcopy(self)

		if lhs.datetype == 'abs':
			if rhs.datetype == 'cor':
				self._rewrite_items( lhs, rhs, [ 'daytime', 'hours', 'minutes', 'seconds' ] )
				return lhs

		if lhs.datetype == 'cor':
			if rhs.datetype == 'abs' or rhs.datetype == 'rel' or rhs.datetype == 'relcor':
				return rhs | lhs

			if rhs.datetype == 'cor':
				lhs._rewrite_items( lhs, rhs, [ 'hours', 'minutes', 'seconds', 'daytime' ] )
				return lhs

		if lhs.datetype == 'rel':
			if rhs.datetype == 'rel' or rhs.datetype == 'relcor':
				self._stack_items(
					lhs, rhs, 
					[ 'year', 'month', 'day', 'relhour', 'relmin', 'relsec' ]
				)
				self._rewrite_items(lhs, rhs, [ 'weekday' ])
				if rhs.datetype == 'relcor':
					self._rewrite_items(lhs, rhs, [ 'hours', 'minutes', 'seconds', 'daytime', 'datetype' ])
				return lhs

			if rhs.datetype == 'cor':
				self._rewrite_items( lhs, rhs, [ 'hours', 'minutes', 'seconds', 'daytime' ] )
				lhs.datetype = 'relcor'
				return lhs

		if lhs.datetype == 'relcor':
			if rhs.datetype == 'rel' or rhs.datetype == 'relcor':
				self._stack_items( lhs, rhs, [ 'year', 'month', 'day', 'relhour', 'relmin', 'relsec' ] )
				self._rewrite_items( lhs, rhs, [ 'weekday' ] )
				if rhs.datetype == 'relcor':
					self._rewrite_items( lhs, rhs, [ 'hours', 'minutes', 'seconds', 'daytime' ] )
				return lhs

			if rhs.datetype == 'cor':
				self._rewrite_items( lhs, rhs, [ 'daytime', 'hours', 'minutes', 'seconds' ] )
				return lhs

		raise Exception(
			"Can't combine %s date and %s date" % (lhs.datetype, rhs.datetype)
		)





# FUNCTIONS
def prenormalize(word):
	for mark in prenorm_marks:
		for markword in mark['words']:
			if markword == word:
				return mark['value']
	return word



def normalize(word):
	return morph.normal_forms(word)[0]



def find_mark(word):
	for mark in marks:
		for markword in mark['words']:
			if word == markword:
				return mark
	return None





# RULES FOR LEXER
word_was = False
t_ignore = ' \t\n,.:;!?*@#$%^&()-_+=[]{}|/<>~`'

def t_error(t):
	print("Error: unknown literal: %s" % t.value)
	return

def t_number(t): # integer
	r'\d+'
	global word_was

	if word_was:
		t.type = 'WORD'
		return t

	t.value = int(t.value)
	t.type = 'NUMBER'
	return t

def t_word(t):
	r'\w+'
	global word_was

	if word_was:
		t.type = 'WORD'
		return t

	word = t.value
	word = prenormalize(word.lower())
	word = normalize(word)
	#  print("normalized word: %s" % word)

	mark = find_mark(word)
	if mark is None:
		mark = find_mark(t.value)

	if mark is None:
		t.type = 'WORD'
		word_was = True
		return t

	t.type = mark['type']
	t.value = mark.get('value')
	return t





# RULES FOR PARSER
def p_error(v):
	print("Syntax error on token: %s" % str(v))
	return



# COMMAND
def p_command(v):
	'''
	command : date
	        | command WORD
	'''
	if isinstance(v[1], Date):
		v[0] = Command(CType.CNOTICE, v[1].pydate(), [])
	elif len(v) == 2:
		v[0] = v[1]
		v[1].text.append(v[2])
	else: 
		v[0] = v[1]
		v[0].text += [ v[2] ]
	return

#  def p_command_word(v):
	#  'command : command WORD'
	#  v[0] = v[1]
	#  return

#  def p_command_pre_word(v):
	#  'command : WORD command'
	#  v[0] = v[2]
	#  return

#  def p_command_prev(v):
	#  'command : command COMMAND'
	#  v[0] = Command(v[2])
	#  v[0].prev = v[1]
	#  return

#  def p_command_tags(v):
	#  'command : command tags'
	#  v[0] = v[1]
	#  v[0].tags = v[2]
	#  return

#  def p_command_deadline(v):
	#  '''
	#  command : command DEADLINE date
	#  command : command DEADLINE DEADLINE date
	#  '''
	#  v[0] = v[1]
	#  v[0].deadline = v[3] if isinstance(v[3], Date) else v[4]
	#  return

#  def p_command_date(v):
	#  'command : command date'
	#  v[0] = v[1]
	#  v[0].date = v[2]
	#  return

#  def p_command_from(v):
	#  'command : command SINCE date'
	#  v[0] = v[1]
	#  v[0].since = v[3]

#  def p_not_command(v):
	#  'command : NOT command'
	#  v[0] = v[2]
	#  v[0].vice = True
	#  return





# tags
#  def p_tags(v):
	#  'tags : TAG_NAME'
	#  v[0] = [ v[1] ]
	#  return

#  def p_tags_tag_list(v):
	#  '''
	#  tags : taglist
		 #  | staglist
	#  '''
	#  v[0] = v[1]
	#  return

#  def p_tag_list(v):
	#  'taglist : TAG'
	#  v[0] = []
	#  return

#  def p_tag_list_tag(v):
	#  'taglist : taglist WORD'
	#  v[0] = v[1]
	#  v[0].append( find_tag(v[2]) )
	#  return

#  def p_strict_tag_list(v):
	#  'staglist : STRICT_TAG'
	#  v[0] = []
	#  return

#  def p_strict_tag_list_tag(v):
	#  'staglist : staglist WORD'
	#  v[0] = v[1]
	#  v[0].append( v[2] )
	#  return





# DATE

# Дата может быть абсолютной, относительной или
# корректировочной
def p_date(v):
	'''
	date : absdate
		 | reldate
	     | cordate
	'''
	v[0] = v[1]
	return



# Абсолютная дата, т.е. когда явно указывается
# день, месяц (год?); к абсолютной дате может
# добавляться корректировочная
def p_absdate(v):
	'''
	absdate : num MONTH_NAME
	        | absdate cordate
	'''
	if isinstance(v[1], list):
		v[0] = Date('abs')
		v[0].day = v[1][0]
		v[0].month = v[2]
	else:
		v[0] = v[1] | v[2]
	return



# Относительная дата, которая может состоять из:
#   - Названия дня недели (пондельник, вторник...)
#   - Ключевое слово 'через', возможно, число и
#     указание единицы измерения времени, например,
#     "через десять минут", "через час"
# К относительное дате может добавляться корректи-
# ровочная: "завтра утром", "через неделю вечером в шесть"
def p_reldate(v):
	'''
	reldate : RELDATE
	        | IN WEEKDAY
			| WEEKDAY
			| AFTER TIME_NAME
			| AFTER num TIME_NAME
			| reldate cordate
			| reldate reldate
			| cordate reldate
	'''
	if isinstance(v[1], int):
		v[0] = Date('rel')
		v[0].day = v[1]
		return

	if v[1] == 'in':
		v[0] = Date('rel')
		v[0].weekday = v[2]
		return

	if len(v) < 3:
		v[0] = Date('rel')
		v[0].weekday = v[1]

	if v[1] == 'after':
		v[0]     = Date('rel')
		timename = v[2]    if isinstance(v[2], str)  else v[3]
		num      = v[2][0] if isinstance(v[2], list) else 1
		if timename == 'sec':
			v[0].relsec = num
		elif timename == 'min':
			v[0].relmin = num
		elif timename == 'hour':
			v[0].relhour = num
		elif timename == 'day':
			v[0].day = num
		elif timename == 'week':
			v[0].day = num*7
		elif timename == 'month':
			v[0].month = num
		else:
			raise Exception('Unknown time name')
		return

	v[0] = v[1] | v[2]

	return



# Корректировочная дата или, другими совами, определяющая
# время в пределах суток; дата может состоять из:
#   - Названия времени дня (утром, вечером, ночью)
#   - Ключевого слова "в" и числа (в 5, 10)
# К корректировочная дате может прибавляться ещё одна
# корректировочная: утром в 5, вечером в 9
def p_cordate(v):
	'''
	cordate : DAYTIME_NAME
	        | IN DAYTIME_NAME
			| IN num
			| IN num TIME_NAME
			| IN TIME_NAME 
			| IN TIME_NAME num
			| cordate num TIME_NAME
			| cordate cordate
	'''

	if v[1] == 'in':
		v[0] = Date('cor')
		if isinstance(v[2], list):
			if len(v) == 3:
				v[0].hours = v[2][0]
				v[2] += [ None, None ]
				v[0].minutes, v[0].seconds = v[2][1], v[2][2]
			else:
				if v[3] == 'hour':
					v[0].hours = v[2][0]
				elif v[3] == 'min':
					v[0].minutes = v[2][0]
				elif v[3] == 'sec':
					v[0].seconds = v[2][0]
				else:
					raise Exception('Unknown TIME_NAME with on rule IN num TIME_NAME (cordate)')
		elif v[2] == 'hour':
			v[0].hours = 1
			if len(v) == 4:
				v[3] += [ None ]
				v[0].minutes, v[0].seconds = v[3][0], v[3][1]
			return
		else:
			v[0].daytime = v[2]
	elif isinstance(v[1], str):
		v[0] = Date('cor')
		v[0].daytime = v[1]
	else:
		if len(v) == 4:
			v[0] = v[1]
			if v[3] == 'hour':
				v[0].hours = v[2][0]
			elif v[3] == 'min':
				v[0].minutes = v[2][0]
			elif v[3] == 'sec':
				v[0].seconds = v[2][0]
			else:
				raise Exception('Unknown TIME_NAME with on rule IN num TIME_NAME (cordate)')
		else:
			v[0] = v[1] | v[2]

	return



# NUMBERS
def p_num_number(v):
	'num : NUMBER'
	v[0] = [ v[1] ]
	return

def p_num_num_word(v):
	'num : numword'
	v[0] = v[1]
	return

def p_num_num_add(v):
	'''
	num : num NUMBER
	    | num numword
	'''
	v[0] = v[1]
	if isinstance(v[2], list):
		v[0] += v[2]
	else:
		v[0].append(v[2])
	return

def p_num_word(v):
	'numword : NUMBER_WORD'
	v[0] = [ v[1] ]
	return

def p_num_word_overlap(v):
	'numword : numword NUMBER_WORD'

	pval = v[1][-1]
	val = v[2]
	res = None
	if pval % ( 10 ** len(str(val)) ) == 0 and pval != 10: 
		res = pval + val
	elif pval > 1000 and pval // 1000 * 1000 % ( 10 ** len(str(val + pval%1000)) ) == 0:
		res = pval // 1000 * 1000 + val * (pval % 1000)
	elif pval < 1000 and val >= 1000:
		res = pval * val
	else:
		v[0] = v[1]
		v[0].append(v[2])
		return
	v[0] = v[1]
	v[0][-1] = res
	return





# FUNCTIONAL OBJECTS
lexer = lex.lex()
parser = yacc.yacc()





# END
