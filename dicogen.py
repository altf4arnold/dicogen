import sqlite3
import hashlib
import sys
import os
from itertools import product

def select():
	#This module is watching if we are asking to generate the dictionnary
	arguments=sys.argv
	if len(arguments)==1:
		return 0
	else:
		if arguments[1]=='gen':
			return 1
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
	database = sqlite3.connect('dico.db')
	c=database.cursor()
	#print(words)   #Was used for testing
	#print(hashlib.sha1(words.encode('utf-8')).hexdigest())  #Was used for testing
	while turning<turns:
		c.execute("INSERT INTO words (clear,sha1,sha256,md5) VALUES (?,?,?,?)",( generated[turning] , generated[turning+1] , generated[turning+2], generated[turning+3] ))
		turning=turning+4
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
	database = sqlite3.connect('dico.db')
	c=database.cursor()
	clear = c.execute("SELECT clear FROM words WHERE clear OR sha1 OR sha256 OR md5 LIKE '%s'"%research).fetchone()
	sha1 = c.execute("SELECT sha1 FROM words WHERE clear OR sha1 OR sha256 OR md5 LIKE '%s'"%research).fetchone()
	sha256 = c.execute("SELECT sha256 FROM words WHERE clear OR sha1 OR sha256 OR md5 LIKE '%s'"%research).fetchone()
	md5 = c.execute("SELECT md5 FROM words WHERE clear OR sha1 OR sha256 OR md5 LIKE '%s'"%research).fetchone()
	print("clear : ",clear[0], "\nsha1 : ", sha1[0], "\nsha256 : ", sha256[0], "\nmd5 : ", md5[0])
	database.close()


generated=[]

if select()==0:
	reader()
elif select()==1:
	if databaseinit()==0:
		write(initiator(generatorcontrolpannel(),generated),generated)
	else:
		print("Whooops, an error occured while creating the database\n")
		print("Please verify your permissions")

elif select()==10:
	print("You've entered bullshit :'(")

#Made with ❤ by altf4