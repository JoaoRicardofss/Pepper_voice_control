# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 10:42:11 2019

@author: joao ricardo
"""
#This file is dedicated to the defining of the behaviour that will make pepper follow a person when called in thescript of the autonomous life
from naoqi import ALProxy

class FollowMe():
  def __init__(self):
      #as in the autonomouslife script, the initial function provides access to the defined and required API's. Establishes connection through the IP and port of Pepper
    self.dialog = ALProxy("ALTextToSpeech", "172.16.0.77", 9559)
    self.motion = ALProxy("ALMotion", "172.16.0.77", 9559)
    self.posture = ALProxy("ALRobotPosture", "172.16.0.77", 9559) # Qual a diferença entre este e a linha de cima?
    self.tracker = ALProxy("ALTracker", "172.16.0.77", 9559)
    self.memory = ALProxy("ALMemory","172.16.0.77",9559)
    self.perception = ALProxy("ALPeoplePerception", "172.16.0.77", 9559)
    
    #the variables defined directly below are the default values pretended for the different parameters of the tracking module
    self.targetName = "Face" #defines what kind of traget Pepper is looking for, can be a Face, a LandMark on even a red ball
    self.distanceX = 0.4 #distances to the target
    self.distanceY = 0.0
    self.angleWz = 0.0
    self.thresholdX = 0.1 #when moving towards the target, Pepper makes an evaluation of the distance left to reach the defined target. If thedistance to the target is smaller then the defined threshold Pepper will consider he reach the target
    self.thresholdY = 0.1
    self.thresholdWz = 0.3
    self.subscribeDone = False
    self.effector = "None"
    self.isRunning = False
    self.faceSize=0.1
    
    self.posture.goToPosture("StandInit",0.3) #This line will only make that pepper stand in a more neutral position instead of looking to the sky as it is initiated when the autonomous life is disabled

  def start(self):
    #setMode will define how whe want the robot to behave when following the target. Options are: moving the "Head" or "WholeBody" in place, or "Move" to the target. 
    mode = "Move"
    self.tracker.setMode(mode)

    #the effector is used when we want that pepper uses one of its members to chase an obstacle. E.g.If we set the effector to "Arms", Pepper will chase the target like a zombie with arms up pointing to the target.
    self.tracker.setEffector(self.effector)
    
    self.tracker.registerTarget(self.targetName, self.faceSize)
    #giving a correct size will make the calculations more accurate. this method assumes more importance when using landmarks, where higher precision is required.

    #we use the setRelativePosition method to set a relative position taking into acount the variables defined above
    self.tracker.setRelativePosition([-self.distanceX, self.distanceY, self.angleWz, self.thresholdX, self.thresholdY, self.thresholdWz])

    self.tracker.track(self.targetName) #Start tracker
    self.isRunning = True  
            
  def stop(self):
    self.tracker.stopTracker() #stop tracker
    self.tracker.unregisterAllTargets() #unregister targets in order to be able to search for a different one when someone runes it again.
   

    

    