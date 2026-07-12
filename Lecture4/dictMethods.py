#Keys Method
Chess_Stats = {
    "Daily" : 1230,
    "Rapid" : 1084,
    "Bullet" : 1033,
    "Blitz" : 950,
    "Puzzles" : 1579,
    "Puzzle Rush" : 30,
    "Daily960" : 927,
    "Live960" : 619,
    "Bughouse" : 868
}

print(Chess_Stats.keys())
print(list(Chess_Stats.keys()))
print(len(Chess_Stats))
print(len(list(Chess_Stats.keys())))
print(Chess_Stats.keys())

#Values Method
Browsers = {
    "Chrome" : 71.22,
    "Safari" : 14.35,
    "Edge" : 4.98,
    "Firefox" : 2.3,
    "Opera" : 1.89
}

print(Browsers.values())
print(list(Browsers.values()))

#Items Method
Companies = {
    "NVIDIA" : 412.576,
    "Apple" : 365.08,
    "Alphabet" : 342.373,
    "Microsoft" : 325.915,
    "Amazon" : 223.192,
    "Meta" : 151.171
}

print(Companies.items())
print(list(Companies.items()))

#Get Method
Fav_Openings = {
    "Bird's Opening" : "1. f4",
    "Bishop's Opening" : "1. e4 e5 2. Bc4",
    "Scotch Gambit" : "1. e4 e5 2. Nf3 Nc6 3. d4 exd4 4. Bc4",
    "Vienna Gambit" : "1. e4 e5 2. Nc3 Nf6 3. f4",
    "Englund Gambit" : "1. d4 e5",
    "Center Game" : "1. e4 e5 2. d4",
    "Italian Game" : "1. e4 e5 2. Nf3 Nc6 3. Bc4",
    "Rousseau Gambit" : "1. e4 e5 2. Nf3 Nc6 3. Bc4 f5",
    "King's Gambit" : "1. e4 e5 2. f4"
}

print(Fav_Openings["Italian Game"])
print(Fav_Openings.get("Italian Game"))
#Line 58 and 59 mean the same thing, but if Line 58 can get an error if you put a non-existent value in the dictionary, but Line 59 will just give "None" response.
print(Fav_Openings.get("Philidor Defense")) #No error, returns NONE
#But in this code line below, it will return an error.
#print(Fav_Openings("Philidor Defense"))

#SAMPLE
print("Hi")
print("Welcome to")
print("ApnaCollege")
print("We are learning")
print("Coding")

a = 1
b = 2
sum = a + b
print(sum)

#If there is an error in Python, it will initially show an error. 
#But the rest of the code, which if even it is right, it will not run. 
#And this is a major problem in Python programming. 
#Suppose there is a website that has backend Python development, and if for example, an error comes, the whole website will stop working, making the system unstable. 
#There are bugs and errors everywhere in real life. 
#But this doesn't mean that the entire website should stop working. 
#So that's why it is preferable to not put a situation where a code gets an error and the rest of the code doesn't run. 
#To prevent that, we should use "GET METHOD", among others, which we will study later in the upcoming lectures. 
#For example, if I put print(ABCDEFG) randomly anywhere in the code, it will show an error and won't run, along with the rest of the code because you should put "" on it.
#We definetely have try-catch blocks and other measures to prevent all of this if a situation like this happens, but on a very basic level, we will try to use methods that don't throw errors.

print("BEFORE")
#print(Fav_Openings["French Defense"]) -> Not there, so it will show an error
print("AFTER")
#As you can see, BEFORE ran, and the error was also shown, fine, but AFTER, which is a valid command, did not run.

OS = {
    "Android" : 37.78,
    "Windows" : 32.68,
    "iOS" : 14.97,
    "macOS" : 2.28,
    "Linux" : 1.45,
}

OS.update({"ChromeOS": 0.76})
print(OS)

#Another Method, Same Result
OS_new1 = {"OS X" : 3.88, "Ubuntu" : 0.24}
OS.update(OS_new1)
print(OS)

#Duplicate Keys are not allowed.
OS_new2 = {"Linux" : 1.56}
OS.update(OS_new2)
print(OS)