import telebot
import random
import re
import json

# token.json = {"token":"YourApiToken"}
try:
	with open('token.json') as token_file:
		token = json.load(token_file)
		bot = telebot.TeleBot(token['token'])
except FileNotFoundError:
	print('Create token.json {"token":"YourApiToken"}')

# global variables used to pass dices to the `roll_advantage` function
advantage_check_flag = None
advantage_dice = {}


@bot.message_handler(commands=['start'])
def start(message):
	bot.send_message(message.chat.id, 'Hello :3\nCheck out /help pls')


@bot.message_handler(commands=['help'])
def help_message(message):
	with open(file='./help_message.txt') as file:
		bot.send_message(message.chat.id, str(file.read()))


@bot.message_handler(commands=['roll'])
def roll(message):
	try:
		inputted_dice = telebot.util.extract_arguments(message.text)
		if inputted_dice == '':
			inputted_dice = '1d20+0'
		answer = roll_helper(inputted_dice)
		bot.send_message(message.chat.id, str(answer))
	except ValueError:
		bot.send_message(message.chat.id, "Something is wrong, probably 0-sided dice")
	except (telebot.apihelper.ApiTelegramException, telebot.apihelper.ApiHTTPException):
		bot.send_message(message.chat.id, "Why")


@bot.message_handler(regexp='^\\d*[dDкК]\\d+[+-]?\\d*$')
def roll_shortcut(message):
	try:
		inputted_dice = message.text
		answer = roll_helper(inputted_dice)
		bot.send_message(message.chat.id, str(answer))
	except ValueError:
		bot.send_message(message.chat.id, "Can't work with 0-sided dice")
	except (telebot.apihelper.ApiTelegramException, telebot.apihelper.ApiHTTPException):
		bot.send_message(message.chat.id, "Why")


@bot.message_handler(regexp='[12]')
def adv_dis(message):
	global advantage_check_flag
	if advantage_check_flag:
		global advantage_dice
		advantage_check_flag = False
		multiplier = advantage_dice['multiplier']
		n_of_sides = advantage_dice['n_of_sides']
		modifier = advantage_dice['modifier']
		if re.search('1', message.text):
			sum_answer, answer_list = roll_dice(multiplier, n_of_sides, modifier, mode='advantage')
		else:
			sum_answer, answer_list = roll_dice(multiplier, n_of_sides, modifier, mode='disadvantage')
		bot.send_message(message.chat.id, f"{sum_answer} {tuple(answer_list)}")


@bot.message_handler(func=lambda message: True)
def unhandled(message):
	bot.send_message(message.chat.id, 'Invalid input')


def roll_advantage(num_dice, num_sides, mode=None):
	results = []
	for i in range(num_dice):
		results.append(random.randint(1, num_sides))
	if mode == 'advantage':
		return max(results)
	elif mode == 'disadvantage':
		return min(results)
	else:
		return sum(results)


def roll_helper(inputted_dice):
	if not input_test(inputted_dice):
		return 'Invalid input'
	multiplier, n_of_sides, modifier = splice_tested_input(inputted_dice)
	if multiplier == '2' and n_of_sides == '20':
		global advantage_check_flag
		advantage_check_flag = True
		global advantage_dice
		advantage_dice = {
			'multiplier': multiplier,
			'n_of_sides': n_of_sides,
			'modifier': modifier
		}
		return '1. advantage\n2. disadvantage'
	if int(multiplier) > 255:
		return 'Too many dices'
	sum_answer, answer_list = roll_dice(multiplier, n_of_sides, modifier)
	if len(answer_list) < 2:
		return sum_answer
	return f"{sum_answer} {tuple(answer_list)}"


def input_test(inputted_dice):
	negative_multiplier = re.search('^-', inputted_dice)
	if negative_multiplier:
		return False
	is_dice = re.search("^\\d*[dDкК]\\d+[+-]?\\d*$", inputted_dice)
	if not is_dice:
		return False
	return True


def splice_tested_input(dice):
	try:
		multiplier = re.search('^\\d*', dice).group()
		if not multiplier:
			multiplier = 1
	except AttributeError:
		multiplier = 1
	n_of_sides = re.search('[dDкК](\\d+)', dice).group(1)
	try:
		modifier = re.search('(\\+\\d*)|(-\\d*)', dice).group()
		if not re.search('\\d+', modifier):
			modifier = '+0'
	except AttributeError:
		modifier = '+0'
		if not modifier:
			modifier = 1
	return multiplier, n_of_sides, modifier


def roll_dice(multiplier, n_of_sides, modifier, mode=None) -> tuple:
	answer_list = []
	if n_of_sides == 0:
		return 0, [0]
	for i in range(0, int(multiplier)):
		dice_throw = random.randint(1, int(n_of_sides))
		answer_list.append(dice_throw)
	sum_of_dices = sum(answer_list)
	if not modifier:
		return sum_of_dices, answer_list
	modifier_int = int(re.search('\\d+$', modifier).group())
	if mode == 'advantage':
		sum_of_dices = max(answer_list)
	elif mode == 'disadvantage':
		sum_of_dices = min(answer_list)
	if not re.search('^-', modifier):
		sum_of_dices += modifier_int
	else:
		sum_of_dices -= modifier_int
	return sum_of_dices, answer_list


if __name__ == '__main__':
	try:
		bot.infinity_polling()
	except Exception as e:
		print(str(e))
