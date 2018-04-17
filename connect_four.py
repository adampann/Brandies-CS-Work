import math
from random import randint

import numpy as np

#global variable of decision tree
global decision_tree
decision_tree = None


def newBoard():
	return np.zeros((7,6)).astype(int)

	# return [[0, 0, 0, 0, 0, 0],
	#         [1, 0, 0, 0, 0, 0],
	#         [0, 0, 0, 0, 0, 0],
	#         [1, 1, 0, 0, 0, 0], #top of colmuns (check horizonal board)
	#         [-1, 1, 0, 0, 0, 0],
	#         [-1, 1, 0, 0, 0, 0],
	#         [-1, 1, 0, 0, 0, 0]]

def LegalMove(position, board):

	if position < 0 and position >= len(board):
		return False

	if board[position, -1] == 0:
		return True

	return False

def placeOnBoard(postition, board, type):
	column = board[postition]
	for y in range(0, len(column)):
		#if type(column[y]) == list:
			#print("this is bad")
		if column[y] == 0:
			board[postition, y] = type
			return board


def randomChoice(options):
	index = randint(0, (len(options) - 1))
	return options[index]


def printBoard(board):
	for y in range(5, -1, -1):
		#print(y + 1, " ", end="")
		for x in range(0, 7):
			if x < 6:
				print(board[x][y], "| ", end="")
			else:
				print(board[x][y], " ", end="")

		print()

	for index in range(0, len(board)):
		print("- - ", end="")
	print()
	for index in range(0, len(board)):
		print(index, "  ", end="")
	print()

def generateMoves(board):
	possible = []
	for x in range(0, len(board)):
		if LegalMove(x, board):
			possible.append(x)
	return possible

def checkplayable(board):

	checker = [0,0]

	winner = checkfull(board)
	if winner:
		return [1,1]

	winner = checkVert(board)
	if winner != 0:
		checker[winner-1] = 1
		return checker

	winner = checkHori(board)
	if winner != 0:
		checker[winner - 1] = 1
		return checker

	winner = checkDiag(board)
	if winner != 0:
		checker[winner - 1] = 1
		return checker

	return [0,0]

def checkfull(board):
	full = True
	for column in board:
		if column[-1] == 0:
			full = False
	return full

def checkVert(board):
	for y in range(0,3):
		for x in range(0,7):
			if board[x][y] != 0 and board[x][y] == board[x][y + 1] == board[x][y + 2] == board[x][y + 3]:
				return board[x][y]
	return 0

def checkHori(board):
	for y in range(0,(len(board[0]))):
		for x in range(0,len(board)-3):
			# print(board[x][y], board[x + 1][y], board[x + 2][y], board[x + 3][y])
			if board[x][y] != 0 and board[x][y] == board[x + 1][y] == board[x + 2][y] == board[x + 3][y]:
				#print("done: ", board[x][y])
				return board[x][y]


	return 0

def checkDiag(board):

	for y in range(0,3):
		for x in range(0,4):
			if board[x][y] != 0 and board[x][y] == board[x + 1][y + 1] == board[x + 2][y + 2] == board[x + 3][y + 3]:
				return board[x][y]

	for y in range(0,3):
		for x in range(6, 2, -1):
			if board[x][y] != 0 and board[x][y] == board[x - 1][y + 1] == board[x - 2][y + 2] == board[x - 3][y + 3]:
				return board[x][y]
	return 0

class human:
	def makeMove(self, board):
		print("legal moves: ", generateMoves(board))
		valid = False
		choice = None
		while valid == False:
			choice = int(input("choice a legal move: "))
			if LegalMove(choice, board) == False:
				print("try again")
			else:
				valid = True
		return placeOnBoard(choice, np.copy(board), self.playerType)

	def __init__(self, type):
		self.playerType = type

class RandomPlay:
	def makeMove(self, board):
		choice = randomChoice(generateMoves(board))
		#print("Random choice ", choice)
		return placeOnBoard(choice, np.copy(board), self.playerType)

	def __init__(self, type):
		self.playerType = type

class BasicMiniMax:
	def makeMove(self, board):
		choice = minimax(self.playerType, board, self.depth)
		return placeOnBoard(choice, board, self.playerType)

	def __init__(self, type, depth):
		self.playerType = type
		self.depth = depth

class DecisionTree:
	def makeMove(self, board):
		choice = decision_minimax(self.playerType, board, self.depth, self.decision_tree)

		return placeOnBoard(choice, board, self.playerType)

	def __init__(self, type, depth):

		self.decision_tree = create_decision_tree()
		self.playerType = type
		self.depth = depth

def play(p1, p2, board, do_print):
	winnerStatus = [0,0]
	count = 0
	p1_id = p1.playerType
	p2_id = p2.playerType
	while winnerStatus == [0,0]:
		if do_print == True:
			printBoard(board)

		if count == 0:
			if do_print == True:
				print("Player {}'s Turn".format(p1_id))
			board = p1.makeMove(board)
			count += 1
			#print(heuristic(p1.playerType, board))
		else:
			if do_print == True:
				print("Player {}'s Turn".format(p2_id))
			board = p2.makeMove(board)
			count -= 1

		#check for winner / draw
		winnerStatus = checkplayable(board)

	output = 'It\'s a draw'if winnerStatus == [0,0] else 'Player 1 won' if  winnerStatus == [1,0] else 'Player 2 won'
	#print '{0}'.format('It\'s a draw'if winner == [0,0] else 'Player 1 won' if  winner == [1,0] else 'Player 2 won')

	if do_print == True:
		print(output)
		printBoard(board)
	return winnerStatus


def heuristic(Player_symbol, board):

	if Player_symbol == 1:
		score = heuristic_helper(Player_symbol, board)
		others = heuristic_helper(2, board)
		return (score - others)
	else:
		score = heuristic_helper(Player_symbol, board)
		others = heuristic_helper(1, board)
		return  (score - others)

def heuristic_helper(Player_symbol, board):
	count2 = 0
	count3 = 0
	count4 = 0
	#vertical check
	for column in board:
		lowest_index = 0
		while lowest_index < len(column):
			lowest_element = column[lowest_index]
			#if element is 0, nothing is above it so break for current column
			if lowest_element == 0 or lowest_element == "b":
				break
			#if current element isn't the one we are looking skip it
			if lowest_element != Player_symbol:
				lowest_index +=1
				continue

			continuous_length = 1 # length of how many elements are in a row
			#loops while next element is same
			while lowest_index + continuous_length < len(column) and column[lowest_index + continuous_length] == Player_symbol:
				continuous_length += 1

			if continuous_length == 4:
				count4 += 1
			elif continuous_length == 3 and (lowest_index + continuous_length -1) < len(column) and column[lowest_index + continuous_length -1]:
				count3 += 1
			elif continuous_length == 2 and (lowest_index + continuous_length -1) < len(column)-2 and column[lowest_index+2] == 0 and column[lowest_index + 3] == 0:
				count2 += 1

			lowest_index += continuous_length

	#horizontal check
	for row_index in range(0, len(board[0])):
		row = board[:,row_index] #gets the row
		trailing_empty = 0 #keep track of empty squares behind current location
		current_index =0
		while current_index < len(row):
			if row[current_index] == 0: # if the current element is empty keep track it
				trailing_empty += 1
				current_index += 1 #move index forwar
				continue #end checking on this element
			if row[current_index] != Player_symbol: #if its the other player
				trailing_empty = 0 #reset trailing_empty as there is no more empty elemnt behind next element
				current_index += 1
				continue

			continuous_length = 1
			while current_index + continuous_length < len(row) and row[current_index + continuous_length] == Player_symbol:
				continuous_length += 1

			if continuous_length == 4:
				count4 += 1
			elif continuous_length == 3:
				if trailing_empty > 0: #if there is room behind to grow from
					count3 += 1
				#if there is room infront to grow from
				if (current_index + continuous_length) < len(row) and row[current_index + continuous_length] == 0:
					count3 += 1
			elif continuous_length == 2:
				if trailing_empty >= 2: #there is room for the 2 to become a 4 in the back
					count2 += 1
				#if there is one space behind and one space in front for it to grow into a 4
				if trailing_empty >= 1 and current_index + continuous_length < len(row) and row[current_index + continuous_length] == 0:
					count2 += 1
				if current_index + continuous_length + 1 < len(row) and row[current_index + continuous_length] == 0 and (row[current_index + continuous_length + 1] == 0 or row[current_index + continuous_length + 1] == Player_symbol):
					count2 += 1

			current_index += continuous_length
			trailing_empty = 0

	#check diag
	diags = [board[::-1, :].diagonal(i) for i in range(-board.shape[0] + 1, board.shape[1])]
	diags.extend(board.diagonal(i) for i in range(board.shape[1] - 1, -board.shape[0], -1))

	#filters out diags that are less than 4 bc they can never become a winning move
	filtered_diags = []
	for x in range(0, len(diags)):
		if len(diags[x]) >= 4:
			filtered_diags.append(diags[x])

	for diag in filtered_diags:
		trailing_empty = 0
		current_index = 0
		while current_index < len(diag):
			if diag[current_index] == 0:  # if the current element is empty keep track it
				trailing_empty += 1
				current_index += 1  # move index forwar
				continue  # end checking on this element
			if diag[current_index] != Player_symbol:  # if its the other player
				trailing_empty = 0  # reset trailing_empty as there is no more empty elemnt behind next element
				current_index += 1
				continue

			continuous_length = 1
			while current_index + continuous_length < len(diag) and diag[current_index + continuous_length] == Player_symbol:
				continuous_length += 1

			if continuous_length == 4:
				count4 += 1
			elif continuous_length == 3:
				if trailing_empty > 0:
					count3 += 1
				if (current_index + continuous_length) < len(diag) and diag[current_index + continuous_length] == 0:
					count3 += 1
			elif continuous_length == 2:
				if trailing_empty > 1: #there is room for the 2 to become a 4 in the back
					count2 += 1
				if trailing_empty >= 1 and current_index + continuous_length < len(diag) and diag[current_index + continuous_length] == 0:
					count2 += 1
				if current_index + continuous_length + 1 < len(diag) and diag[current_index + continuous_length] == 0 and (diag[current_index + continuous_length + 1] == 0 or diag[current_index + continuous_length + 1] == Player_symbol):
					count2 += 1

			current_index += continuous_length
			trailing_empty = 0

	#return [count2,count3,count4, (2*count2 + 100*count3 + 10000*count4)]
	return (1 * count2 + 10000 * count3 + 500000 * count4)

def decision_minimax(id, board, depth, tree):
	best = ["loss", -float("inf")]
	best_move = None
	for move in generateMoves(board):
		# res is a pair of game end type (win, loss, draw) & the probability of that
		res = min_decision_player(id, placeOnBoard(move, board.copy(), id), (depth - 1), tree)
		if res[0] == "win":
			if best[0] == "win":
				if res[1] > best[1]:
					best = res
					best_move = move
			else:
				best = res
				best_move = move
		elif res[0] == "draw":
			if best[0] == "draw":
				if res[1] > best[1]:
					best = res
					best_move = move
			elif best[0] == "loss":
				best = res
				best_move = move
		elif res[0] == "loss" and best[0] == "loss":
			if res[1] < best[1]:
				best = res
				best_move = move
	return best_move

def min_decision_player(id, board, depth, tree):
	if depth == 0 or checkplayable(board) != [0,0]:
		return decision_tree_heuristic(id, board, tree)

	best = ["win",float("inf")]
	for move in generateMoves(board):
		res = max_decision_player(id, placeOnBoard(move, board.copy(), 1 if id == 2 else 2), (depth - 1), tree)
		#print("res", res)
		if res[0] == "loss":
			if best[0] == "loss":
				if res[1] > best[1]:
					best = res
			else:
				best = res
		elif res[0] == "draw":
			if best[0] == "draw":
				if res[1] > best[1]:
					best = res
			elif best[0] == "win":
				best = res
		elif res[0] == "win" and best[0] == "win":
			if res[1] < best[1]:
				best = res
	return best

def max_decision_player(id, board, depth, tree):
	if depth == 0 or checkplayable(board) != [0,0]:
		return decision_tree_heuristic(id, board, tree)


	best = ["loss", -float("inf")]
	for move in generateMoves(board):
		res = min_decision_player(id, placeOnBoard(move, board.copy(), id), (depth - 1), tree)
		#print("res",res)
		if res[0] == "win":
			if best[0] == "win":
				if res[1] > best[1]:
					best = res
			else:
				best = res
		elif res[0] == "draw":
			if best[0] == "draw":
				if res[1] > best[1]:
					best = res
			elif best[0] == "loss":
				best = res
		elif res[0] == "loss" and best[0] == "loss":
			if res[1] < best[1]:
				best = res
	return best

def decision_tree_heuristic(id, board, tree):
	board_as_features = make_in_feature(board, id)

	return compare_with_tree(tree, board_as_features)

def compare_with_tree(tree, board_as_features):
	#print("tree", tree)
	# some base case:
	#need to be able to see if node has a label
	if tree.keys().__contains__("label"):
		#print("tree label", [tree["label"][0], tree["label"][1]])
		return tree["label"]

	current_feature = tree["feature"]
	if board_as_features[current_feature]:
		return compare_with_tree(tree["true"], board_as_features)
	else:
		return compare_with_tree(tree["false"], board_as_features)

# def minimax(id, board, depth):
# 	#move = minimax_helper(id, board, depth, False)
# 	move = minimax_helper(id, board, depth)
# 	return move

def minimax(id, board, depth):
	best = -float("inf")
	best_move = None
	for move in generateMoves(board):
		res = min_player(id, placeOnBoard(move, board.copy(), id),(depth- 1))
		if res > best:
			best  = res
			best_move = move
	return best_move

def min_player(id, board, depth):
	if depth == 0 or checkplayable(board) != [0,0]:
		return heuristic(id, board)

	best = float("inf")
	for move in generateMoves(board):
		res = max_player(id, placeOnBoard(move, board.copy(), 1 if id == 2 else 2), (depth - 1))
		if res < best:
			best = res

	return best

def max_player(id, board, depth):
	if depth == 0 or checkplayable(board) != [0,0]:
		return heuristic(id, board)

	best = -float("inf")
	for move in generateMoves(board):
		res = min_player(id, placeOnBoard(move, board.copy(), id), (depth - 1))
		if res > best:
			best = res
	return best

def tournament(p1, p2, board):
	print("tournament started")
	p1_count = 0
	p2_count = 0
	draw_count = 0
	#player one goes first
	for position in range(0, len(board)):
		#print("game {} started".format(p1_count + p2_count + draw_count+1))
		win_status = play(p2, p1, placeOnBoard(position, newBoard(), p1.playerType), False)
		#print("end game")
		if win_status == [0,1]:
			p2_count += 1
		elif win_status == [1,0]:
			p1_count += 1
		elif win_status == [1,1]:
			draw_count += 1

	#player two goes first.
	for position in range(0, len(board)):
		#print("game {} started".format(p1_count + p2_count + draw_count+1))

		win_status = play(p1, p2, placeOnBoard(position, newBoard(), p2.playerType), False)
		#print("end game")
		if win_status == [0,1]:
			p2_count += 1
		elif win_status == [1,0]:
			p1_count += 1
		elif win_status == [1, 1]:
			draw_count += 1

	print("[{},{},{}]Player 1 wins {}, Player 2 wins {}, there were {} draws".format(p1_count, p2_count, draw_count,p1_count, p2_count, draw_count))


def find_feature(board, id):
	Player_symbol = id
	if Player_symbol == None:
		Player_symbol = "x"
	count2 = 0
	count3 = 0
	count4 = 0
	# vertical check
	for column in board:
		lowest_index = 0
		while lowest_index < len(column):
			lowest_element = column[lowest_index]
			# if element is 0, nothing is above it so break for current column
			if lowest_element == 0 or lowest_element == "b":
				break
			# if current element isn't the one we are looking skip it
			if lowest_element != Player_symbol:
				lowest_index += 1
				continue

			continuous_length = 1  # length of how many elements are in a row
			# loops while next element is same
			while lowest_index + continuous_length < len(column) and column[
						lowest_index + continuous_length] == Player_symbol:
				continuous_length += 1

			if continuous_length == 3 and (lowest_index + continuous_length - 1) < len(column) and column[
								lowest_index + continuous_length - 1]:
				count3 += 1
			elif continuous_length == 2 and (lowest_index + continuous_length - 1) < len(column) - 2 and column[
						lowest_index + 2] == 0 and column[lowest_index + 3] == 0:
				count2 += 1

			lowest_index += continuous_length

	# horizontal check
	for row_index in range(0, len(board[0])):
		row = board[:, row_index]  # gets the row
		trailing_empty = 0  # keep track of empty squares behind current location
		current_index = 0
		while current_index < len(row):
			if row[current_index] == 0 or row[current_index] == "b":  # if the current element is empty keep track it
				trailing_empty += 1
				current_index += 1  # move index forwar
				continue  # end checking on this element
			if row[current_index] != Player_symbol:  # if its the other player
				trailing_empty = 0  # reset trailing_empty as there is no more empty elemnt behind next element
				current_index += 1
				continue

			continuous_length = 1
			while current_index + continuous_length < len(row) and row[
						current_index + continuous_length] == Player_symbol:
				continuous_length += 1

			if continuous_length == 3:
				if trailing_empty > 0:  # if there is room behind to grow from
					count3 += 1
				# if there is room infront to grow from
				if (current_index + continuous_length) < len(row) and row[current_index + continuous_length] == 0:
					count3 += 1
			elif continuous_length == 2:
				if trailing_empty >= 2:  # there is room for the 2 to become a 4 in the back
					count2 += 1
				# if there is one space behind and one space in front for it to grow into a 4
				if trailing_empty >= 1 and current_index + continuous_length < len(row) and row[
							current_index + continuous_length] == 0:
					count2 += 1
				if current_index + continuous_length + 1 < len(row) and row[
							current_index + continuous_length] == 0 and (
						row[current_index + continuous_length + 1] == 0 or row[
							current_index + continuous_length + 1] == Player_symbol):
					count2 += 1

			current_index += continuous_length
			trailing_empty = 0

	# check diag
	diags = [board[::-1, :].diagonal(i) for i in range(-board.shape[0] + 1, board.shape[1])]
	diags.extend(board.diagonal(i) for i in range(board.shape[1] - 1, -board.shape[0], -1))

	# filters out diags that are less than 4 bc they can never become a winning move
	filtered_diags = []
	for x in range(0, len(diags)):
		if len(diags[x]) >= 4:
			filtered_diags.append(diags[x])

	for diag in filtered_diags:
		trailing_empty = 0
		current_index = 0
		while current_index < len(diag):
			if diag[current_index] == 0 or diag[current_index] == "b":  # if the current element is empty keep track it
				trailing_empty += 1
				current_index += 1  # move index forwar
				continue  # end checking on this element
			if diag[current_index] != Player_symbol:  # if its the other player
				trailing_empty = 0  # reset trailing_empty as there is no more empty elemnt behind next element
				current_index += 1
				continue

			continuous_length = 1
			while current_index + continuous_length < len(diag) and diag[
						current_index + continuous_length] == Player_symbol:
				continuous_length += 1

			if continuous_length == 3:
				if trailing_empty > 0:
					count3 += 1
				if (current_index + continuous_length) < len(diag) and diag[current_index + continuous_length] == 0:
					count3 += 1
			elif continuous_length == 2:
				if trailing_empty > 1:  # there is room for the 2 to become a 4 in the back
					count2 += 1
				if trailing_empty >= 1 and current_index + continuous_length < len(diag) and diag[
							current_index + continuous_length] == 0:
					count2 += 1
				if current_index + continuous_length + 1 < len(diag) and diag[
							current_index + continuous_length] == 0 and (
						diag[current_index + continuous_length + 1] == 0 or diag[
							current_index + continuous_length + 1] == Player_symbol):
					count2 += 1

			current_index += continuous_length
			trailing_empty = 0



		# print("{}'s heuritic: [2's,{}] [3's,{}] [4's,{}] [score,{}]".format(Player_symbol,count2,count3,count4,(2*count2 + 100*count3 + 10000*count4)))
		return [count2,count3]

def dominate_middle(board, peice):
	peice_count = 0
	other_count = 0
	for x in range(2,5):
		col = board[x]
		for element in col:
			if element == 0 or element == "b":
				continue
			if element != peice:
				other_count += 1
				continue
			peice_count += 1
	return peice_count > other_count

def dominate_top(board, peice):
	peice_count = 0
	other_count = 0
	for col in board[:,3:]:
		for element in col:
			if element == 0 or element == "b":
				continue
			if element != peice:
				other_count += 1
				continue
			peice_count += 1
	return peice_count > other_count

def more_winning_squares(board, peice):
	peice_winning = 0
	other_winning = 0
	for x in range(0,len(board)-1, 2):
		for y in range(0,len(board[x]), 2):
			peice_count = 0
			other_count = 0
			for x_area in range(0,2):
				for y_area in range(0,2):
					element = board[x+x_area][y+y_area]
					if element == 0 or element == "b":
						continue
					if element != peice:
						other_count += 1
					else:
						peice_count += 1
			if peice_count > other_count:
				peice_winning += 1
			elif other_count > peice_count:
				other_winning += 1
	return peice_winning > other_winning

def column_wins(board, peice):
	peice_col_count = 0
	other_col_count = 0
	for col in board:
		peice_count = 0
		other_count = 0
		for element in col:
			if element == 0 or element == "b":
				break
			if element != peice:
				other_count += 1
			else:
				peice_count += 1
		if peice_count >= other_count:
			peice_col_count += 1
		else:
			other_col_count += 1

	return peice_col_count > other_col_count

def make_in_feature(board, peice):
	feature = {}
	order_count = find_feature(board, peice)
	if type(peice) == int:
		other_count = find_feature(board, (peice%2+1))
	elif peice == 'x':
		other_count = find_feature(board, 'o')
	elif peice == 'o':
		other_count = find_feature(board, 'x')

	if order_count[0] > 0:  # more than zero 2's
		feature["more than zero 2"] = True
	else:
		feature["more than zero 2"] =False
	if order_count[0] > 1:  # more than one 2's
		feature["more than one 2"] = True
	else:
		feature["more than one 2"] = False
	if order_count[0] > 2:  # more than two 2's
		feature["more than two 2"] = True
	else:
		feature["more than two 2"] = False

	if order_count[1] > 0:  # more than zero 3's
		feature["more than zero 3"] = True
	else:
		feature["more than zero 3"] = False
	if order_count[1] > 1:  # more than one 3's
		feature["more than one 3"] = True
	else:
		feature["more than one 3"] = False
	if order_count[1] > 2:  # more than 2 3's
		feature["more than two 3"] = True
	else:
		feature["more than two 3"] = False

	if order_count[0] > other_count[0]:
		feature["winning with 2s"] = True
	else:
		feature["winning with 2s"] = False

	if order_count[1] > other_count[1]:  # more than zero 3's
		feature["winning on 3"] = True
	else:
		feature["winning on 3"] = False


	feature["middle dominate"] = dominate_middle(board, peice)  # do they have middle dominance
	feature["top dominate"] = dominate_top(board, peice)
	feature["more winning squares"] = more_winning_squares(board, peice)
	feature["more column wins"] = column_wins(board, peice)
	return feature

def convert_data_to_result_features(database, peice = "x"):
	database_with_feature_list = []
	for data in database:
		result_with_feature = [data[1], make_in_feature(data[0], peice)]
		database_with_feature_list.append(result_with_feature)#add this feature list

	return database_with_feature_list

def take_in_data():
	database = []
	peice = "x"
	with open('connect-4.data') as file:
		for line in file:

			line_seperated = line.split(",")

			board = np.array(line_seperated)[0:-1].reshape((7,6))
			combined = [board, line_seperated[-1].split('\n')[0]] #

			database.append(combined)

		return database

def create_decision_tree():
	global decision_tree
	if decision_tree != None:
		print("decision tree already created")
		return decision_tree
	else:
		print("creating decision tree")
		#returns list of board, outcome pairs
		database = take_in_data()

		#returns list of outcome, dictionary of features pairs
		database_as_result_features = convert_data_to_result_features(database, "x")

		#gets all features used for data
		full_feature_list = list(database_as_result_features[0][1].keys())
		#(full_feature_list)

		#global decision_tree#ID3(database_as_result_features, full_feature_list)
		decision_tree = ID3(database_as_result_features, full_feature_list, "")
		return decision_tree

def check_win_loose_draw(database):
	all_win = True
	all_loss = True
	all_draw = True
	for data in database:
		outcome = data[0]
		if all_win and outcome == 'loss' or outcome == 'draw':
			all_win = False
		if all_loss and outcome == 'win' or outcome == 'draw':
			all_loss = False
		if all_draw and outcome == 'loss' or outcome == 'win':
			all_draw = False
		if not(all_draw or all_loss or all_win):
			return None
	if all_win:
		return["win", 1]
	elif all_loss:
		return ["loss", 1]
	elif all_draw:
		return ["draw", 1]
	return None

def most_common(database): #this needs to be FIXED
	win = 0
	loss = 0
	draw = 0
	for data in database:
		attribute = data[0]
		if attribute == 'win':
			win += 1
		elif attribute == 'loss':
			loss += 1
		elif attribute == 'draw':
			draw += 1
	total = win + loss + draw
	return ["win", (win/total)] if (win > loss and win > draw) else ["loss", (loss/total)] if (loss > win and loss > draw) else ["draw", (draw/total)]

def ID3(database, feature_list, spacing):
	root = {}
	#if all examplesa are of the same type, set nodes label to that
	label = check_win_loose_draw(database)
	if label != None:
		root["label"] = label
		#print("wld {}".format(root["label"]))
		return root
	#if you run out of features to use then just take the most common
	if feature_list == []:
		root["label"] = most_common(database)
		#print("mc {}".format(root["label"]))
		return root

	#determine best feature to use
	best_gain_score = -float("inf")
	best_feature = None
	for feature in feature_list:
		val = Gain(database, feature)
		if val > best_gain_score:
			best_feature = feature
			best_gain_score = val

	#will only use the feature if any info was actually gained from it
	if best_gain_score > 0:
		print("{}{}: {}".format(spacing, best_feature, best_gain_score))

		#set nodes feature to best feature
		root["feature"] = best_feature
		#split data on feature
		database_split = split(database, best_feature) #[[true on feature],[false on feature]]

		#remove best feature from feature list
		copy_feature_list = feature_list.copy()
		copy_feature_list = remove(copy_feature_list, best_feature)

		# create children and set to None
		root["true"] = None
		root["false"] = None

		if len(database_split[0]) == 0:
			root["true"] = {"label" : most_common(database)}
		else:
			root["true"] = ID3(database_split[0], copy_feature_list, spacing + "	")

		if len(database_split[1]) == 0:
			root["false"] = {"label" : most_common(database)}
		else:
			root["false"] = ID3(database_split[1], copy_feature_list, spacing + "	")
	else:
		root["label"] = most_common(database)
	return root

def remove(lst, feature):
	updated = []
	for element in lst:
		if element != feature:
			updated.append(element)
	return updated

def Gain(database, attribute):
	gain = Entropy(database)
	values = [True, False]
	total_sum = 0
	for value in values:
		set_with_value = get_subset(database, attribute, value)
		if len(set_with_value) != 0:
			total_sum += ((len(set_with_value)/ len(database)) * Entropy(set_with_value))

	gain -= total_sum
	return  gain

def get_subset(database, attribute, value):
	subset = []
	for data in database:
		data_features = data[1]
		if data_features[attribute] == value:
			subset.append(data)

	return subset

def Entropy(database):
	value = 0
	size = len(database)
	outcomes = ['win', 'loss', 'draw']
	for outcome in outcomes:
		#print("outcome: {}".format(outcome))
		prop = (how_many(outcome, database))/size
		#print("prop: {}".format(prop))
		if prop != 0:
			value += (0 - prop) * math.log(prop,2)
	return value
def how_many(goal_outcome, database): #returns how many of database has given outcome
	count = 0
	for data in database:
		if goal_outcome == data[0]:
			count += 1
	#print(count)
	return count


def split(database, feature):
	split_data = [[],[]]
	for data in database:
		if data[1][feature] == True:
			split_data[0].append(data)
		else:
			split_data[1].append(data)

	return split_data

#NOTE: This does not entirly work, there is a but causing it to fail at the end of the range depths.
# I my testing these depths work when put through the normal code but something seems to break it here.
# sorry :(
def test_different_depths():
	for mini_depth in range(2,5):
		for tree_depth in range(2,4):
			p2 = BasicMiniMax(2, mini_depth)
			p1 = DecisionTree(1, tree_depth)
			tournament(p1, p2, newBoard())
			print("mini depth: {}, tree depth {}".format(mini_depth, tree_depth))

if __name__ == "__main__":
	print("welcome to connect four!")
	playType = 0
	while playType != 3:
		print("Would you like to play(1) or have a tournament(2) or test different ply *READ COMMENTS ON CODE*(3) or exit(4): ")
		playType = int(input())
		if playType == 4:#exit
			break
		elif playType == 1 or playType == 2:
			p1 = None
			p2 = None
			while p1 == None:
				responce = int(input("is player 1 human(1), random(2), minimax(3), or decision tree(4): "))
				if responce == 1:
					p1 = human(1)
				elif responce == 2:
					p1 = RandomPlay(1)
				elif responce == 3:
					p1 = BasicMiniMax(1, 4)
				elif responce == 4:
					p1 = DecisionTree(1, 4)
				else:
					print("that doesn't seem to be an option, try again")
			while p2 == None:
				responce = int(input("is player 2 human(1), random(2), minemax(3), or decision tree(4): "))
				if responce == 1:
					p2 = human(2)
				elif responce == 2:
					p2 = RandomPlay(2)
				elif responce == 3:
					p2 = BasicMiniMax(2, 4)
				elif responce == 4:
					p2 = DecisionTree(2, 4)
				else:
					print("that doesn't seem to be an option, try again")
			if playType == 1:
				print("start play")
				play(p1, p2, newBoard(), True)
			elif playType == 2:
				tournament(p1, p2, newBoard())
		elif playType == 3:
			test_different_depths()
		else:
			print("try again")






