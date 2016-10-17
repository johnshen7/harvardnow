import puzzle_data

def makeSpecial():
	s = "A student in the Harvard body has been desecrating the building walls with graffiti with nonsense riddles!" 
	s += "As the student detective, you have no clues or leads but to answer the riddles themselves… \n"
	s += "Text ‘puzzle’ and the answer to the riddle to progress to the next one.\n"
	s += "The first riddle: \n"
	s += puzzles[0][0]
    return s

special = makeSpecial()

puzzles = puzzle_data.puzzles
num_puzzles = len(puzzles)

def eval(ans):
	ans = ans.lower()
	for index, puzzle in enumerate(puzzles):
		if ans == puzzle[1].lower():
			if index < num_puzzles - 1:
				return puzzles[index + 1][0]
			else:
				done = "After you follow the trail of riddles, you find that the perp was Michael Gao!\n"
				done += "You discover that he was the puppet master for the entire school! The absolute power was driving him insane!\n"
				done += "You throw him with the mumps victims in quarintine. He plots his revenge..."
				return done 

	return "Incorrect, the scoundrel inches closer to freedom."