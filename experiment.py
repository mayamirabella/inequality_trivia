import numpy as np
from psychopy import visual, event
from time import time
import random

from utils.ui import (
    fixation_cross,
    present_text,
    wait_for_keypress,
    determine_start,
    present_start_points,
    determine_end,
    choose_difficulty,
    present_question,
    check_answer,
    present_feedback,
    present_end_points
)

from utils.write import (
    CSVWriter_trial,
	CSVWriter_block,
	CSVWriter_subj
) 

#from utils.triggerer import Triggerer

#### initialize some things

# parport triggers
#parport = Triggerer(0)
#parport.set_trigger_labels(['MVC_start', 'MVC_end',
#			     'baseline_start', 'baseline_end',
#			     'choose_difficulty', 'answer_question',
#				   'start_feedback', 'end_feedback', 
# 					'initial_points', 'final_points'])

# data handling
subj_num = input("Enter subject number: ")
subj_num = int(subj_num)
trial_log = CSVWriter_trial(subj_num)
#block_log = CSVWriter_block(subj_num)
subj_log = CSVWriter_subj(subj_num)
subj_cond = input("Enter subject condition: ")
subj_cond = str(subj_cond)
subj_log.write(subj_num, subj_cond)
np.random.seed(subj_num)

# starting points
points_self, points_conf1, points_conf2 = determine_start(subj_cond)
total_points_self = points_self
trial_num = 1


# make question and answer lists

easy_qs = \
	['What is the fastest land animal on the planet?',
  'What is the largest mammal on the planet?',
  'What is the capital of China?',
  'How many continents are there?',
  'What is the largest country in the world?',
  'Which country has the largest population in the world?',
  'What is the most widely spoken language in Brazil?',
  'What does the B in FBI stand for?',
  'Who plays the Hulk in the Avengers movies?',
  'Which movie won the Oscar for Best Picture/Movie in 2020?',
  'Which TV series features the characters Cersei, Jon, Jamie, and Daenerys?',
  'Which Korean song was the first to have one billion views on Youtube?',
  'Which song has the most views on YouTube?',
  'Which famous band consisted of the members John, Paul, Ringo, and George?',
  'Who is the president of China?',
  'Who is the prime minister of Canada?',
  'Which Olympian has earned the most medals in history?',
  'Which Dutch painter cut of part of his/her ear?',
  'What is the style in which Andy Warhol painted?']
easy_answers = \
	[['Cheetah'],
  ['whale', 'blue whale'],
  ['Beijing'],
  ['7'],
  ['Russia'],
  ['China'],
  ['Portuguese'],
  ['Bureau'],
  ['Mark Ruffalo', 'Ruffalo'],
  ['Parasite'],
  ['Game of Thrones'],
  ['Gangnam Style'],
  ['Despacito'],
  ['The Beatles', 'beatles'],
  ['Xi Jinping'],
  ['Trudeau', 'Justin Trudeau'],
  ['Michael Phelps', 'Phelps'],
  ['Van Gogh', 'Vincent Van Gogh'],
  ['Pop art', 'modern art', 'modern']]
medium_qs = \
    ['What is the slowest mammal in the world?',
     'Which animal kills most humans?',
	 'What does the scoville heat unit measure?',
	 'What is the largest organ in the human body?',
	 'What is the capital of Canada?',
	 'What is the capital of Australia?',
	 'What is the name of the world\'s longest river?',
	 'Which country is also known as the Democratic Republic of Korea?',
	 'What is the smallest country in the world?',
	 'What is the most widely spoken native language in the world?',
	 'Which language is spoken in Hong Kong? (Chinese is not the name of the language)',
	 'Which actor plays the joker in the latest The Joker movie?',
	 'Which iconic TV featured the main characters, Samantha, Carrie, Cynthia and Charlotte?',
	 'What is the most sold music album worldwide in history?',
	 'What is Bob Dylan\'s real name? ',
	 'Which band has sold the most records in history?',
	 'Who is the head of state of Canada?',
	 'How many countries were there in the EU in 2018?',
	 'How many players (including goal keeper) are there on the field during a soccer game?',
	 'Which active NBA player holds the record for most points?',
	 'How many paintings did van Gogh sell during is life?',
	 'Who painted The Scream?',
	 'Which pop art painter\'s paintings resemble comics and cartoons?',
	 'Which country produces most coffee in the world?',
	 'Which book inspired the name of the store Starbucks?']
medium_answers = \
	[['Sloth'],
  ['Mosquito'],
  ['spicy', 'spiciness', 'hotness', 'heat', 'spice level', 'heat level', 'spicy heat of a chili pepper'],
  ['Skin', 'the skin'],
  ['Ottawa'],
  ['Canberra'],
  ['The Nile', 'nile'],
  ['North Korea'],
  ['Vatican', 'the vatican', 'vatican city'],
  ['Mandarin'],
  ['Cantonese'],
  ['Joaquin Phoenix', 'Pheonix'],
  ['Sex and the City'],
  ['Thriller', 'Michael Jackson Thriller', 'Thriller Michael Jackson', 'Michael Jackson\'s Thriller', 'Thriller by Michael Jackson'],
  ['Robert Zimmerman'],
  ['the Beatles', 'beatles'],
  ['King Charles the third', 'King Charles III', 'King Charles 3', 'King Charles', 'Charles', 'Charles the third', 'Charles III', 'Charles 3'],
  ['28'],
  ['22'],
  ['LeBron James', 'LeBron'],
  ['1'],
  ['Edvard Munch', 'Munch'],
  ['Roy Liechtenstein', 'Liechtenstein'],
  ['Brazil'],
  ['Moby Dick']]
hard_qs = \
	['Which bone are babies born without?',
  'Who discovered penicilin?',
  'What name is used to refer to a group of frogs?',
  'What is the hardest substance in the human body?',
  'What is the worldst tallest grass?',
  'What is the capital of Malawi?',
  'Which country has the highest population density in the world?',
  'Which american state has the smallest population?',
  'What is someone who suffers oneirophobia afraid of?',
  'What are the three main spoken languages in Switzerland?',
  'Which American President did not speak English as his first language?',
  'Who is the director of The Grand Budapest Hotel?',
  'What African country served as the setting for Tatooine in Star Wars?',
  'Who wrote the Opera Madame Butterfly?',
  'Who was the first female singer to be introduced to the rock \'n roll hall of fame?',
  'Who is the president of Germany?',
  'What degree does Angela Merkel have?',
  'Which female athlete has won the most Olympic medals in history?',
  'Which famous painter lived in Tahiti?',
  'Who said \"in the future everybody will be famous for 15 minutes\"?']
hard_answers = \
	[['Knee cap'],
  ['Alexander Fleming', 'Fleming'],
  ['An army', 'army'],
  ['Tooth enamel', 'teeth', 'enamel', 'tooth', 'teeth enamel'],
  ['Bamboo'],
  ['Lilongwe'],
  ['Monaco'],
  ['Wyoming'],
  ['Dreams'],
  ['German, French, Italian', 'German, Italian, French', 'French, German, Italian', 'French, Italian, German', 'Italian, French, German', 'Italian, German, French'],
  ['Martin van Buren', 'van Buren'],
  ['Wes Anderson'],
  ['Tunisia'],
  ['Puccini', 'Giacomo Puccini'],
  ['Aretha Franklin'],
  ['Steinmeier', 'Frank-Walter Steinmeier'],
  ['PhD', 'PhD in chemistry', 'chemistry PhD', 'quantum chemistry phd', 'chemistry', 'quantum chemistry', 'PhD in quantum chemistry'],
  ['Larisa Latynina', 'Latynina'],
  ['Gauguin', 'Paul Gauguin'],
  ['Andy Warhol', 'Warhol']]


# psychopy viz
win = visual.Window(
	size = (800, 600),
	color = (0, 0, 0),
	colorSpace = 'rgb255',
	screen = -1,
	units = "norm",
	fullscr = False,
	pos = (0, 0),
	allowGUI = False
	)


BASELINE_TIME = 3 # 5 minutes (300s)
DIFFICULTY_WAIT_TIME = 30 # 30s to choose difficulty
ROUND_TIME = 30 # 30s to answer question
N_ROUNDS = 2 # 8 rounds total
START_DISPLAY_TIME = 3
END_DISPLAY_TIME = 3


########################
# Baseline Physio
########################

# Instructions
txt = '''
Now we are going to collect a 5-minute baseline measurement for the ECG. 
Sit comfortably, relax and breathe normally. \n
Press the spacebar when you're ready to begin.
'''
wait_for_keypress(win, txt)

# Get Baseline Physio
#parport.send_trigger('baseline_start')
present_text(win, 'Relax', BASELINE_TIME)
#parport.send_trigger('baseline_end')

########################
# Trivia Task
########################

t1 = time()

# Instructions
txt = '''
Task Instructions here. \n
Press the spacebar to continue.
'''
wait_for_keypress(win, txt)

# Run Trivia Task

# present starting state
#parport.send_trigger('initial_points')
present_start_points(win, points_self, points_conf1, points_conf2, START_DISPLAY_TIME)

# cycle through rounds
for round in range(N_ROUNDS):
    # choose difficulty
	#parport.send_trigger('choose_difficulty')
	difficulty = choose_difficulty(win, DIFFICULTY_WAIT_TIME)
    # present question and get response
	if difficulty == 'easy':
		question = easy_qs[round]
		#parport.send_trigger('answer_question')
		response = present_question(win, question, ROUND_TIME)
		answer = easy_answers[round]
	elif difficulty == 'medium':
		question = medium_qs[round]
		#parport.send_trigger('answer_question')
		response = present_question(win, question, ROUND_TIME)
		answer = medium_answers[round]
	elif difficulty == 'hard':
		question = hard_qs[round]
		#parport.send_trigger('answer_question')
		response = present_question(win, question, ROUND_TIME)
		answer = hard_answers[round]
	else:
		present_text(win, 'No difficulty level chosen.', 'white', ROUND_TIME)
	# check answer
	accuracy = check_answer(response, answer)
	#  display points earned
	#parport.send_trigger('start_feedback')
	points_self = present_feedback(win, difficulty, accuracy)
	#parport.send_trigger('end_feedback')
	# fixation
	fixation_cross(win)

	# save data
	trial_log.write(
		trial_num,
		difficulty,
		question,
		answer[0],
		str.rstrip(response), 
		accuracy,
		points_self
	)
	trial_num += 1
	total_points_self += points_self
	# trial end

# end state
points_conf1, points_conf2 = determine_end(subj_cond, total_points_self)
#parport.send_trigger('final_points')
present_end_points(win, total_points_self, points_conf1, points_conf2, END_DISPLAY_TIME)

t2 = time()
print('Task Complete.')
print('The task took %d minutes.'%((t2 - t1)/60))
print('Participant earned %d points for themselves.'%(total_points_self))
#print('Participant earned %d points for the next participant.'%(points_other))

##########################
# and we're done!
##########################
txt = '''
That's all! You can press the spacebar to end the experiment.
If the experimenter doesn't come get you immediately, let them
know you're done using the button on your desk.
'''
wait_for_keypress(win, txt)
