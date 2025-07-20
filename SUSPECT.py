"""J'ACCUSE!, by Aditya Verma @youngcoder45
A mystery game of intrigue and a missing cat.
# This code is available at https://nostarch.com/big-book-small-python-programming
Tags: extra-large, game, humor, puzzle"""

# Play the original Flash game at:
# https://homestarrunner.com/videlectrix/wheresanegg.html
# More info at: http://www.hrwiki.org/wiki/Where's_an_Egg%3F

import time, random, sys

# Set up the constants:
SUSPECTS = ['Mr. SIMON', 'ELLISHA BENZ', 'BILL MONOPOLIS', 'SENATOR SCHMEAR', 'MRS. CATHEREINE', 'DR. JEAN RUTHERFORD', 'ADV. DEAN SUZZER', 'ESPRESSA BARRISTOW', 'CECIL EDGAR VANDERTON']
ITEMS = ['FLASHLIGHT', 'CANDLESTICK', 'TRICOLOUR FLAG', 'PRINGLES', 'MARVEL POSTER', 'JAR OF PICKLES', 'NIKE JORDAN', 'ROLEX WATCH', '5 DOLLAR GIFT CARD']
PLACES = ['ZOO', 'JUNKYARD', 'PHOENIX MALL', 'CITY HALL', 'STARBUCKS CAFE', 'BOWLING ALLEY', 'VIDEO GAME CENTER', 'UNIVERSITY LIBRARY', 'THE AIRPORT']
TIME_TO_SOLVE = 350  # 350 seconds (5 minutes 50 Seconds) to solve the game.

# First letters and longest length of places are needed for menu display:
PLACE_FIRST_LETTERS = {}
LONGEST_PLACE_NAME_LENGTH = 0
for place in PLACES:
    PLACE_FIRST_LETTERS[place[0]] = place
    if len(place) > LONGEST_PLACE_NAME_LENGTH:
        LONGEST_PLACE_NAME_LENGTH = len(place)

# Basic sanity checks of the constants:
assert len(SUSPECTS) == 9
assert len(ITEMS) == 9
assert len(PLACES) == 9
# First letters must be unique:
assert len(PLACE_FIRST_LETTERS.keys()) == len(PLACES)


knownSuspectsAndItems = []
# visitedPlaces: Keys=places, values=strings of the suspect & item there.
visitedPlaces = {}
currentLocation = 'TAXI'  # Start the game at the taxi.
accusedSuspects = []  # Accused suspects won't offer clues.
liars = random.sample(SUSPECTS, random.randint(3, 4))
accusationsLeft = 3  # You can accuse up to 3 people.
culprit = random.choice(SUSPECTS)

# Common indexes link these; e.g. SUSPECTS[0] and ITEMS[0] are at PLACES[0].
random.shuffle(SUSPECTS)
random.shuffle(ITEMS)
random.shuffle(PLACES)

# Create data structures for clues the truth-tellers give about each
# item and suspect.
# clues: Keys=suspects being asked for a clue, value="clue dictionary".
clues = {}
for i, interviewee in enumerate(SUSPECTS):
    if interviewee in liars:
        continue  # Skip the liars for now.

    # This "clue dictionary" has keys=items & suspects,
    # value=the clue given.
    clues[interviewee] = {}
    clues[interviewee]['debug_liar'] = False  # Useful for debugging.
    for item in ITEMS:  # Select clue about each item.
        if random.randint(0, 1) == 0:  # Tells where the item is:
            clues[interviewee][item] = PLACES[ITEMS.index(item)]
        else:  # Tells who has the item:
            clues[interviewee][item] = SUSPECTS[ITEMS.index(item)]
    for suspect in SUSPECTS:  # Select clue about each suspect.
        if random.randint(0, 1) == 0:  # Tells where the suspect is:
            clues[interviewee][suspect] = PLACES[SUSPECTS.index(suspect)]
        else:  # Tells what item the suspect has:
            clues[interviewee][suspect] = ITEMS[SUSPECTS.index(suspect)]

# Create data structures for clues the liars give about each item
# and suspect:
for i, interviewee in enumerate(SUSPECTS):
    if interviewee not in liars:
        continue  # We've already handled the truth-tellers.

    # This "clue dictionary" has keys=items & suspects,
    # value=the clue given:
    clues[interviewee] = {}
    clues[interviewee]['debug_liar'] = True  # Useful for debugging.

    # This interviewee is a liar and gives wrong clues:
    for item in ITEMS:
        if random.randint(0, 1) == 0:
            while True:  # Select a random (wrong) place clue.
                # Lies about where the item is.
                clues[interviewee][item] = random.choice(PLACES)
                if clues[interviewee][item] != PLACES[ITEMS.index(item)]:
                    # Break out of the loop when wrong clue is selected.
                    break
        else:
            while True:  # Select a random (wrong) suspect clue.
                clues[interviewee][item] = random.choice(SUSPECTS)
                if clues[interviewee][item] != SUSPECTS[ITEMS.index(item)]:
                    # Break out of the loop when wrong clue is selected.
                    break
    for suspect in SUSPECTS:
        if random.randint(0, 1) == 0:
            while True:  # Select a random (wrong) place clue.
                clues[interviewee][suspect] = random.choice(PLACES)
                if clues[interviewee][suspect] != PLACES[ITEMS.index(item)]:
                    # Break out of the loop when wrong clue is selected.
                    break
        else:
            while True:  # Select a random (wrong) item clue.
                clues[interviewee][suspect] = random.choice(ITEMS)
                if clues[interviewee][suspect] != ITEMS[SUSPECTS.index(suspect)]:
                    # Break out of the loop when wrong clue is selected.
                    break

# Create the data structures for clues given when asked about Sapphire:
SapphireClues = {}
for interviewee in random.sample(SUSPECTS, random.randint(3, 4)):
    kindOfClue = random.randint(1, 3)
    if kindOfClue == 1:
        if interviewee not in liars:
            # They tell you who has Sapphire.
            SapphireClues[interviewee] = culprit
        elif interviewee in liars:
            while True:
                # Select a (wrong) suspect clue.
                SapphireClues[interviewee] = random.choice(SUSPECTS)
                if SapphireClues[interviewee] != culprit:
                    # Break out of the loop when wrong clue is selected.
                    break

    elif kindOfClue == 2:
        if interviewee not in liars:
            # They tell you where Sapphire is.
            SapphireClues[interviewee] = PLACES[SUSPECTS.index(culprit)]
        elif interviewee in liars:
            while True:
                # Select a (wrong) place clue.
                SapphireClues[interviewee] = random.choice(PLACES)
                if SapphireClues[interviewee] != PLACES[SUSPECTS.index(culprit)]:
                    # Break out of the loop when wrong clue is selected.
                    break
    elif kindOfClue == 3:
        if interviewee not in liars:
            # They tell you what item Sapphire is near.
            SapphireClues[interviewee] = ITEMS[SUSPECTS.index(culprit)]
        elif interviewee in liars:
            while True:
                # Select a (wrong) item clue.
                SapphireClues[interviewee] = random.choice(ITEMS)
                if SapphireClues[interviewee] != ITEMS[SUSPECTS.index(culprit)]:
                    # Break out of the loop when wrong clue is selected.
                    break

# EXPERIMENT: Uncomment this code to view the clue data structures:
#import pprint
#pprint.pprint(clues)
#pprint.pprint(SapphireClues)
#print('culprit =', culprit)

# START OF THE GAME
print("""J'ACCUSE! (a mystery game)")
By Aditya Verma @youngcoder45
Inspired by Homestar Runner\'s "Where\'s an Egg?" game

You are the world-famous detective, Sherlock Holmes.
Sapphire Diamond from City Museum has gone missing, and you must sift through the clues.
Suspects either always tell lies, or always tell the truth. Ask them
about other people, places, and items to see if the details they give are
truthful and consistent with your observations. Then you will know if
their clue about Sapphire Diamond is true or not. Will you find Sapphire Diamond in time and accuse the guilty party?
""")
input('Press Enter to begin...')


startTime = time.time()
endTime = startTime + TIME_TO_SOLVE

while True:  # Main game loop.
    if time.time() > endTime or accusationsLeft == 0:
        # Handle "game over" condition:
        if time.time() > endTime:
            print('You have run out of time!')
        elif accusationsLeft == 0:
            print('You have accused too many innocent people!')
        culpritIndex = SUSPECTS.index(culprit)
        print('It was {} at the {} with the {} who Stole it!'.format(culprit, PLACES[culpritIndex], ITEMS[culpritIndex]))
        print('Better luck next time, Detective.')
        sys.exit()

    print()
    minutesLeft = int(endTime - time.time()) // 60
    secondsLeft = int(endTime - time.time()) % 60
    print('Time left: {} min, {} sec'.format(minutesLeft, secondsLeft))

    if currentLocation == 'TAXI':
        print('  You are in your TAXI. Where do you want to go?')
        for place in sorted(PLACES):
            placeInfo = ''
            if place in visitedPlaces:
                placeInfo = visitedPlaces[place]
            nameLabel = '(' + place[0] + ')' + place[1:]
            spacing = " " * (LONGEST_PLACE_NAME_LENGTH - len(place))
            print('{} {}{}'.format(nameLabel, spacing, placeInfo))
        print('(Q)UIT GAME')
        while True:  # Keep asking until a valid response is given.
            response = input('> ').upper()
            if response == '':
                continue  # Ask again.
            if response == 'Q':
                print('Thanks for playing!')
                sys.exit()
            if response in PLACE_FIRST_LETTERS.keys():
                break
        currentLocation = PLACE_FIRST_LETTERS[response]
        continue  # Go back to the start of the main game loop.

    # At a place; player can ask for clues.
    print('  You are at the {}.'.format(currentLocation))
    currentLocationIndex = PLACES.index(currentLocation)
    thePersonHere = SUSPECTS[currentLocationIndex]
    theItemHere = ITEMS[currentLocationIndex]
    print('  {} with the {} is here.'.format(thePersonHere, theItemHere))

    # Add the suspect and item at this place to our list of known
    # suspects and items:
    if thePersonHere not in knownSuspectsAndItems:
        knownSuspectsAndItems.append(thePersonHere)
    if ITEMS[currentLocationIndex] not in knownSuspectsAndItems:
        knownSuspectsAndItems.append(ITEMS[currentLocationIndex])
    if currentLocation not in visitedPlaces.keys():
        visitedPlaces[currentLocation] = '({}, {})'.format(thePersonHere.lower(), theItemHere.lower())

    # If the player has accused this person wrongly before, they
    # won't give clues:
    if thePersonHere in accusedSuspects:
        print('They are offended that you accused them,')
        print('and will not help with your investigation.')
        print('You go back to your TAXI.')
        print()
        input('Press Enter to continue...')
        currentLocation = 'TAXI'
        continue  # Go back to the start of the main game loop.

    # Display menu of known suspects & items to ask about:
    print()
    print('(J) "J\'ACCUSE!" ({} accusations left)'.format(accusationsLeft))
    print('(S) Ask if they know where Sapphire Diamond is.')
    print('(T) Go back to the TAXI.')
    for i, suspectOrItem in enumerate(knownSuspectsAndItems):
        print('({}) Ask about {}'.format(i + 1, suspectOrItem))

    while True:  # Keep asking until a valid response is given.
        response = input('> ').upper()
        if response in 'JST' or (response.isdecimal() and 0 < int(response) <= len(knownSuspectsAndItems)):
            break

    if response == 'J':  # Player accuses this suspect.
        accusationsLeft -= 1  # Use up an accusation.
        if thePersonHere == culprit:
            # You've accused the correct suspect.
            print('You\'ve cracked the case, Detective!')
            print('It was {} who had Stolen Sapphire Diamond.'.format(culprit))
            minutesTaken = int(time.time() - startTime) // 60
            secondsTaken = int(time.time() - startTime) % 60
            print('Good job! You solved it in {} min, {} sec.'.format(minutesTaken, secondsTaken))
            sys.exit()
        else:
            # You've accused the wrong suspect.
            accusedSuspects.append(thePersonHere)
            print('You have accused the wrong person, Detective!')
            print('They will not help you with anymore clues.')
            print('You go back to your TAXI.')
            currentLocation = 'TAXI'

    elif response == 'S':  # Player asks about Sapphire.
        if thePersonHere not in SapphireClues:
            print('"I don\'t know anything about Sapphire Diamond."')
        elif thePersonHere in SapphireClues:
            print('  They give you this clue: "{}"'.format(SapphireClues[thePersonHere]))
            # Add non-place clues to the list of known things:
            if SapphireClues[thePersonHere] not in knownSuspectsAndItems and SapphireClues[thePersonHere] not in PLACES:
                knownSuspectsAndItems.append(SapphireClues[thePersonHere])

    elif response == 'T':  # Player goes back to the taxi.
        currentLocation = 'TAXI'
        continue  # Go back to the start of the main game loop.

    else:  # Player asks about a suspect or item.
        thingBeingAskedAbout = knownSuspectsAndItems[int(response) - 1]
        if thingBeingAskedAbout in (thePersonHere, theItemHere):
            print('  They give you this clue: "No comment."')
        else:
            print('  They give you this clue: "{}"'.format(clues[thePersonHere][thingBeingAskedAbout]))
            # Add non-place clues to the list of known things:
            if clues[thePersonHere][thingBeingAskedAbout] not in knownSuspectsAndItems and clues[thePersonHere][thingBeingAskedAbout] not in PLACES:
                knownSuspectsAndItems.append(clues[thePersonHere][thingBeingAskedAbout])

    input('Press Enter to continue...')

