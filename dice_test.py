import random
import re


def input_test(inputted_dice):
	negative_multiplier = re.search('^-', inputted_dice)
	if negative_multiplier:
		return False
	is_dice = re.search("^\\d*[dD]\\d+[+-]?\\d*$", inputted_dice)
	if not is_dice:
		return False
	return True


def splice_tested_input(dice):
	if dice == 'abort':
		return 'abort'
	try:
		multiplier = re.search('^\\d*', dice).group()
		if not multiplier:
			multiplier = 1
	except AttributeError:
		multiplier = 1
	n_of_sides = re.search('d(\\d+)', dice).group(1)
	try:
		modifier = re.search('(\\+\\d*)|(-\\d*)', dice).group()
		if not re.search('\\d+', modifier):
			modifier = '+0'
	except AttributeError:
		modifier = '+0'
		if not modifier:
			modifier = 1
	return multiplier, n_of_sides, modifier


def roll_dice(multiplier, n_of_sides, modifier) -> tuple:
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
	if not re.search('^-', modifier):
		sum_of_dices += modifier_int
	else:
		sum_of_dices -= modifier_int
	return sum_of_dices, answer_list


def main():
	inputted_dice = input('ur dice?\n')
	try:
		if not input_test(inputted_dice):
			print('Invalid input')
			return
		multiplier, n_of_sides, modifier = splice_tested_input(inputted_dice)
		sum_answer, answer_list = roll_dice(multiplier, n_of_sides, modifier)
		if len(answer_list) < 2:
			print(sum_answer)
			return
		print(f"{sum_answer} {tuple(answer_list)}")
	except Exception as e:
		print("something went wrong :(")
		print(str(e))


if __name__ == '__main__':
	main()
