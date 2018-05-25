import sqlite3
import hashlib
import sys
import os
from itertools import product
import math

def select():
    #This module is watching if we are asking to generate the dictionnary
    arguments=sys.argv
    if len(arguments)==1:
        return 0
    else:
        if arguments[1]=='gen':
            return 1
        elif arguments[1]=='comp':
            return 2
        else:
            return 10

def databaseinit():
    #this module will generate the database 
    os.system("rm -f dico.db")
    database = sqlite3.connect('dico.db')
    c=database.cursor()
    c.execute('''CREATE TABLE words(clear text, sha1 text, sha256 text, md5 text)''')
    #Here we just created the database and the table.
    database.commit()
    c.close()
    database.close()
    return 0

def write(initiator,generated):

	#Here, we are writing the results and making hashes and writing them to the database
	turns=len(generated)
	turning=0
	writer=1 #Because it's a prime number, it can be divided by 0 so it's at one to not triger the database.commit at the first turn
	database = sqlite3.connect('dico.db')
	c=database.cursor()
	#print(words)   #Was used for testing
	#print(hashlib.sha1(words.encode('utf-8')).hexdigest())  #Was used for testing
	while turning<turns:
		#9 592 is a prime number (I used it so that every X possibilitys, we flush the RAM to the DB)
		if writer%9592==0:
			database.commit()
			writer=0
		else:
			c.execute("INSERT INTO words (clear,sha1,sha256,md5) VALUES (?,?,?,?)",( generated[turning] , generated[turning+1] , generated[turning+2], generated[turning+3] ))
			turning=turning+4
		writer=writer+1
	database.commit()
	c.close()
	database.close()

def allwords(chars, length):
    #generating words
    for letters in product(chars, repeat=length):
        yield ''.join(letters)

def initiator(characters,output):
    #Setting up words
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    for wordlen in range(characters[0],characters[1]+1):
        for word in allwords(letters, wordlen):
            output.append(word)
            output.append(hashlib.sha1(word.encode('utf-8')).hexdigest())
            output.append(hashlib.sha256(word.encode('utf-8')).hexdigest())
            output.append(hashlib.md5(word.encode('utf-8')).hexdigest())
    print("DONE !")

def generatorcontrolpannel():
    #Control pannel for the user to reate his database
    numberofchars=[]
    numberofchars.append(int(input("Minimum char number : ")))
    numberofchars.append(int(input("Maximim char number : ")))
    return numberofchars

def reader():
    #Module used to read the database
    research=input("What do you want to look up ? : ")
    #print (research) #Used for testing purpose
    database = sqlite3.connect('dico.db')
    c=database.cursor()
    clear = c.execute("SELECT clear FROM words WHERE clear=? OR sha1=? OR sha256=? OR md5=?",(research,research,research,research,)).fetchone()
    sha1 = c.execute("SELECT sha1 FROM words WHERE clear=? OR sha1=? OR sha256=? OR md5=?",(research,research,research,research,)).fetchone()
    sha256 = c.execute("SELECT sha256 FROM words WHERE clear=? OR sha1=? OR sha256=? OR md5=?",(research,research,research,research,)).fetchone()
    md5 = c.execute("SELECT md5 FROM words WHERE clear=? OR sha1=? OR sha256=? OR md5=?",(research,research,research,research,)).fetchone()
    print("clear : ",clear[0], "\nsha1 : ", sha1[0], "\nsha256 : ", sha256[0], "\nmd5 : ", md5[0])
    database.close()

def comparer(wordsinput):
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    for wordlen in range(0,11):
        for word in allwords(letters, wordlen):
            if wordsinput==word:
                print ("clear : ",word,"\nsha1 : ",hashlib.sha1(word.encode('utf-8')).hexdigest(),"\nsha256 : ",hashlib.sha256(word.encode('utf-8')).hexdigest(),"\nmd5 : ",hashlib.md5(word.encode('utf-8')).hexdigest())
                return 0

            elif wordsinput==hashlib.sha1(word.encode('utf-8')).hexdigest():
                print ("clear : ",word,"\nsha1 : ",hashlib.sha1(word.encode('utf-8')).hexdigest(),"\nsha256 : ",hashlib.sha256(word.encode('utf-8')).hexdigest(),"\nmd5 : ",hashlib.md5(word.encode('utf-8')).hexdigest())
                return 0

            elif wordsinput==hashlib.sha256(word.encode('utf-8')).hexdigest():
                print ("clear : ",word,"\nsha1 : ",hashlib.sha1(word.encode('utf-8')).hexdigest(),"\nsha256 : ",hashlib.sha256(word.encode('utf-8')).hexdigest(),"\nmd5 : ",hashlib.md5(word.encode('utf-8')).hexdigest())
                return 0

            elif wordsinput==hashlib.md5(word.encode('utf-8')).hexdigest():
                print ("clear : ",word,"\nsha1 : ",hashlib.sha1(word.encode('utf-8')).hexdigest(),"\nsha256 : ",hashlib.sha256(word.encode('utf-8')).hexdigest(),"\nmd5 : ",hashlib.md5(word.encode('utf-8')).hexdigest())
                return 0


generated=[]

if select()==0:
    reader()
elif select()==1:
    if databaseinit()==0:
        write(initiator(generatorcontrolpannel(),generated),generated)
    else:
        print("Whooops, an error occured while creating the database\n")
        print("Please verify your permissions")
elif select()==2:
    comparer(input("What do you want to look up? : "))
elif select()==10:
    print("You've entered bullshit :'(")

#Made with ❤ by altf4