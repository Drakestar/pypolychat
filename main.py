# An idea for a "secure" chat app
# Use a polybius sqaure as the means for encryption and the random number generation of python to update
# the square's code i.e. flip position of a (1,1) and b(1,2) so that their coordinates are different

# Random for "encryption"
# Pickle for saving decryption code
# Os for ?
import random
import pickle
import os


# Delete previous data, make extremely sure. as this would ruin chances for communication
def datdel():
    s = input("Are you sure you want to delete square data? y/n:")
    if s == 'y':
        new = input("type, \"yes\"")
        if new == "yes":
            # Probably better ways than just deleting the text file but this was a prototype.
            os.remove("data.txt")


# Decrypt given string
def decrypt(string, polsq):
    c = list(map(int, string))  # Go from what the user copied to a usable integer list
    changes = c[0]  # Get number up to character 9
    c.pop(0)  # Get rid of int for number of changes
    message = []  # Variable for message, will hold list of chars
    # Loop through, swapping necessary
    while changes:
        # Variable to get up to 4 numbers to swap polsq locations
        i = 0
        # List for which indices to swap
        slist = [4, 3, 2, 1]
        # Get 4 indices for swapping
        while i < 4:
            # Set changelist[var] to new index
            slist[i] = c[0]
            # Pop off used number
            c.pop(0)
            # If you have enough variables
            if i == 3:
                temp = polsq[slist[0]][slist[1]]  # Set temp
                polsq[slist[0]][slist[1]] = polsq[slist[2]][slist[3]]  # Replace temped
                polsq[slist[2]][slist[3]] = temp  # Put temp into other one
            # next iteration of janky
            i += 1
        changes -= 1
    # DECRYPT
    # for two values in c get append the character to message
    while c:
        # If there is an escape character
        if c[0] == 6:
            if c[1] == 1:
                message.append(' ')
            if c[1] == 0:
                message.append('.')
        else:
            message.append(polsq[c[0]][c[1]])
        c.pop(0)
        c.pop(0)
    s = map(str, message)  # ['1','2','3']
    s = ''.join(s)  # '123'
    s = str(s)  # 123
    print(s)
    # Print decrypted
    # Return new Polsq
    return polsq


# Take in text string encrypt it
def encrypt(string, polsq):
    # Choose a random number between 1 and 15
    changed = [random.randrange(1, 10)]
    # Multiply by 4 for number of randoms needed
    created = changed[0] * 4
    tempswappers = []
    while created:
        tempswappers.append(random.randrange(0, 5)) # Loop that amount of times adding rand ([0-4]) to an array
        created -= 1
    # For every 4 elements pair off and move polsq values
    i = 0
    swaplist = ['a', 'b', 'c', 'd']
    while tempswappers:
        changed.append(tempswappers[0])
        swaplist[i] = tempswappers[0]
        tempswappers.pop(0)
        if i == 3:
            temp = polsq[swaplist[0]][swaplist[1]]
            polsq[swaplist[0]][swaplist[1]] = polsq[swaplist[2]][swaplist[3]]
            polsq[swaplist[2]][swaplist[3]] = temp
            i = -1
        i += 1
    # TIME FOR ACTUAL ENCRYPTION
    # Loop through string adding polsq value to array above
    for x in string:
        for y in polsq:
            if x in y:
                changed.append(polsq.index(y))
                changed.append(y.index(x))
        if x is '.':
            changed.append(60)
        if x is ' ':
            changed.append(61)
    # Print array
    s = map(str, changed)  # ['1','2','3']
    s = ''.join(s)  # '123'
    s = int(s)  # 123
    print(s)
    #
    return polsq


def loader():
    # Try to load previous text hidden file
    try:
        with open("data.txt", "rb") as file:
            pp = pickle.load(file)
            file.close()
    # No previous file create a new list like that to return something
    except:
        print("No previous contacts!")
        pp = {"base":
              [['a', 'b', 'c', 'd',  'e', 0],
               ['f', 'g', 'h', 'i',  'j', 1],
               ['k', 'l', 'm', 'n',  'o', 2],
               ['p', 'q', 'r', 's',  't', 3],
               ['u', 'v', 'w', 'y',  'z', 4],
               ['.', ' ', '?', '\'', '!', 5],
               [',',  6,   7,   8,    9]]}
    return pp


def saver(squares):
    # Put squares into file
    with open("data.txt", "wb+") as file:
        pickle.dump(squares, file)
    file.close()


def main():
    # Case checking for what the user wants to do
    to = ("sending", "send", 's', 1)
    fr = ("recieving", "recieve", "r", 2)
    qu = ("quit", 'q')
    de = ("delete")
    squares = loader()  # If any previous contacts are there, load them
    lst2 = [item[0] for item in squares]
    lst2.pop(0)

    print("Welcome to josh's encrypted messaging service!")  # Welcome the user
    print("Accepted commands are:")
    print(to)
    print(fr)
    print(qu)
    print(de)
    print("You can talk with ", lst2)
    person = input("Who are you talking with?")  # Get who they are talking to
    if person in qu:
        return 0
    if person in de:
        datdel()
        return 0
    # Go through master square list
    found = False
    for x in squares:
        # If the person is found set the square being used and break otherwise make a new one
        if person in x:
            found = True
            squareused = x[1]
            break
    # Couldn't find that person make a new element in total squares
    if not found:
        squareused = squares[0][1]

    # MAIN LOOP
    while True:
        # Ask whether they are sending or receiving message.
        status = input("Are you sending or receiving a message?")
        if status in qu:
            # save
            squares.append([person, squareused])
            saver(squares)
            # break
            break

        # Send
        if status in to:
            sen = input("What is the message?")  # Input
            squareused = encrypt(sen, squareused)  # Call function

        # Receive message
        if status in fr:
            rec = input("What is the message? ")  # Input
            squareused = decrypt(rec, squareused)  # Call to Function

        # Delete square data
        if status in de:
            datdel()
            break


if __name__ == "__main__":
    main()
