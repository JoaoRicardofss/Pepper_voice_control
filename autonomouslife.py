# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 15:02:00 2019

@author: joao ricardo
"""


from naoqi import ALProxy #provided by softbanks, imports the modules and methods that can be used
import time
from Activity import FollowMe #from the script titled Activity imports the class called FollowMe. it allows for the utilization of its variables.
from implementation import Fios # Este tb se pode dizer o mm que a linha de cima ...
from loop_implementation import Scan #...
#the several scripts that constitute the different applications use should be placed in the same directory in order to facilitate comunication and to be able to import them

#add: look for outside stimuli (sound and face detection)

class Vocal():  
  def __init__(self, proxies): # initial function, establishes communication with the modules defined in preini. the proxy arguments consist on organizing all the methods in a list in order to turn the calling simpler.
                               # using the self as a variable of every defined function makes it possible to comunicate arguments between different function.
    self.asr = proxies[0]
    self.tts = proxies[1]
    self.memory = proxies[2]
    self.dialog = proxies[3]
    self.anime = proxies[4]
#    self.perception = ALProxy("ALPeoplePerception", "172.16.0.77", 9559)

#words to be recognized (voice commands) initialy by pepper when the program is launched. (without wordspotting)
    self.vocabulary = ["Pepper", "Hello", "Follow Me", "stop", "explore", "define points","Store the object"] 
    
#associated responses to each of the recognized words (voice answer from Pepper). care maust be taken to associate the same order for recognized words and answers 
    self.answers = ["Human", "Hello!", "ok! I will follow you", "No Worries, bye!", "Alright, let's explore", "I will define the points in the map" ,"Ok, let me store it for you"] 
    
#set vocabulary indica as palavras do self.vocabulary devem ser identificadas. False designate that word spotting is disable. in the case that the word spotting becomes enable (True), Pepper will spot the designated words in the middle of phrases
    self.asr.setVocabulary(self.vocabulary, False)
    
#like every argument of the vocabulary ??????????has is associated answers, it also has the associated actions. this actions will trigger the defined functions defined in bellow in the script. 
    self.actions = ["","","follow_start","follow_stop","explore","def_point","move_object"]
    
#    self.perception.isFaceDetectionEnabled(True) #o que é isto??
    
  def preinit(naoip="172.16.0.77", port=9559): #function that provides access to the defined and required API's. Establishes connection through the IP and port of the pepper
    asr = ALProxy("ALSpeechRecognition", naoip, port)
    tts = ALProxy("ALTextToSpeech", naoip, port)
    memory = ALProxy("ALMemory", naoip, port)
    dialog = ALProxy("ALDialog",naoip,port)
    anime = ALProxy("ALAnimatedSpeech", naoip, port)  
 #The return statement causes the function to exit and hand back a value to its caller. in this case it sends the data from the arguments defined directly above
    return asr, tts, memory, dialog, anime   

  def start(self):
    # Start the speech recognition engine with user Test_ASR. the name can be any whatever you feel like, but it has to be consisten when it's called throughout the rest of the script
    try:
      while True: 
        time.sleep(2) #time of loop
        self.asr.subscribe("Test_ASR") #this method subscribes to ALSpeechRecognition. this causes the module to start writing information to ALMemory in “WordRecognized”
        
        wordReco = self.memory.getData("WordRecognized")  #the method accesses the ALMemory and retrieves the information written in "wordRecognized".
        print wordReco #prints the words being recognized every 2 seconds (in the computer that is also executing this code).if no word is recognized it prints "[]" if any of the vocabulary words are recognized then it will print it
        
        if wordReco[0] and wordReco[1] >= 0.445: #Means: If the word recognized is in the defined vocabulary and it is identified with a precision over 44.5% then it will trigger the answer and action

          idx = self.vocabulary.index(wordReco[0]) # Return the index of the voice command recognized which is stored in variable "self.vocabulary"
          act = self.actions[idx]
          print wordReco[0]
          self.configuration = {"bodyLanguageMode":"contextual"}
          self.anime.say(self.answers[idx],self.configuration)
          #these last two lines are the configuration for animated speech, it make pepper talk with movement. It is better then text to speech because it looks more interative and attractive to outside users.
          self.asr.unsubscribe("Test_ASR") #everytime a loop is completed the method must be unsubscribed in order to clean it. It should be done regardless of if it has recognized a word or not.
          
          if act: 
            eval(act+"()") #??????
            #locals()[act]
            #self.actions[act]() #variavel referente a função, como o function handle do matlab    
          
        elif wordReco[0] and wordReco[1] < 0.445: #if a word is recognized but not with enough precision it will ask for you to repeat the word. here animated speech is not used because it is a small answer that should be heard often, the movement can become anoying           
          self.tts.say("Come again?")
          self.asr.unsubscribe("Test_ASR")       
       
    except KeyboardInterrupt: #To stop the running program press ctrl+c. It will unsubcribe and stop:
      self.asr.unsubscribe("Test_ASR")
      print "Unsubscribed."

  def unsub_asr(self):
    self.asr.unsubscribe("Test_ASR")  
          
#in the beginning of the script we import the class relative to other scripts (eg. Activity import FollowMe. // Activity is the name of the file, FollowMe the name of the class) that are in the same directory of the current script. 
#To call a certain function from a specific script, we must first define a variable that is equal to the class of the other script we want to use (follower = FollowMe()). After that we can use the functions of that script (follower.start())
#the actions triggered by the voice commands defined in the vocabulary are defined bellow
def follow_start():
    print "Started following."
    follower = FollowMe() #defines the class FollowMe from the Activity script as a variable. this has to be done in order to call trhe specific functions which belongs to this specific class
    follower.start() #it calls the function start that will run the program from activity. makes pepper follow a person
    
def follow_stop():
    print "Stopped following."
    follower = FollowMe()
    follower.stop() #stops pepper from following a person     
 
def move_object():
    print "bringging the box"
    scan=Scan()
    scan.steps()

def explore():
    print"exploring"
    scan=Scan()
    scan.explore()
    
def def_point():
    print "defining points"
    scan=Scan()
    scan.def_point()

      
if __name__ == "__main__":
    naoip="172.16.0.77"
    port=9559
    asr = ALProxy("ALSpeechRecognition", naoip, port)
    tts = ALProxy("ALTextToSpeech", naoip, port)
    anime=ALProxy("ALAnimatedSpeech", naoip, port)
    memory = ALProxy("ALMemory", naoip, port)
    dialog=ALProxy("ALDialog",naoip,port)
    v = Vocal((asr,tts,memory,dialog,anime))
    v.start()
    
    #time.sleep(10)
    #asr.unsubscribe("Test_ASR")

# Alinhar os comentarios que começam no inicio da linha
# Retirar codigo em comentario que não é utilizado
# qual a diferença entre "main" e "preinit"? Esta ultima pode ser eliminada?