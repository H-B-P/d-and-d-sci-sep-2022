import numpy as np
import pandas as pd

import random

random.seed(0)

def roll_dX(X):
 return random.choice(list(range(X)))+1

def roll_NdX(N,X):
 op=0
 for i in range(N):
  op+=roll_dX(X)
 return op

def roll_NdX_keep_L(N,X,L=[0]):
 rolls = []
 for i in range(N):
  rolls+=[roll_dX(X)]
 rolls = sorted(rolls)
 op=0
 for l in L:
  op+=rolls[l]
 return op
 
def pseudoPoisson(N, X):
 op=0
 for i in range(N):
  if roll_dX(X)==X:
   op+=1
 return op

def gen_stat():
 return roll_NdX_keep_L(4,80,[1])

def gen_drag_score(lect, rity, cour, refl, pati):
 warrior = 3*min(refl+9, cour-9)
 guardian = 5*(min(lect, rity, cour, refl, pati)-1)
 return max(warrior, guardian)

def gen_thou_score(lect, rity, cour, refl, pati):
 innovator = 5*(min(lect, pati, cour, rity)-3)
 scholar = 3*min(lect-4, pati+4)
 return max(innovator, scholar)

def gen_serp_score(lect, rity, cour, refl, pati):
 duelist = 3*min(lect+7, refl-7)
 schemer = 3*min(lect+8, pati-8)
 return max(duelist, schemer)

def gen_humb_score(lect, rity, cour, refl, pati):
 organizer = 3*min(rity-6,lect+6)
 citizen = 35+max(pati, rity) 
 return max(organizer, citizen)

#def allocate_student_deprecated(lect, rity, cour, refl, pati, Y=1000):
# pRandomChoice=min(max(0.04, 0.04+0.96*(Y-1512)*(Y-1512)*(Y-1512)/(500*500*500)), 1)
# print(Y,pRandomChoice)
# maxStat = max([lect, rity, cour, refl, pati])
# secondStat = sorted([lect, rity, cour, refl, pati])[-2]
# if random.random()>pRandomChoice:
#  if (cour in [maxStat, secondStat]) and (refl in [maxStat, secondStat]):
#   return "Dragonslayer"
#  if (refl in [maxStat, secondStat]) and (lect in [maxStat, secondStat]):
#   return "Serpentyne"
#  if (lect in [maxStat, secondStat]) and (pati in [maxStat, secondStat]):
#   return "Thought-talon"
#  if (rity in [maxStat, secondStat]) and (lect in [maxStat, secondStat]):
#   return "Humblescrumble"
# return random.choice(["Dragonslayer", "Serpentyne", "Thought-talon","Humblescrumble"])

def allocate_student(dScore, sScore, tScore, hScore, Y=1000):
 
 pRandomChoice=min(max(0.09, 0.09+0.91*(Y-1512)*(Y-1512)*(Y-1512)/(500*500*500)), 1)
 print(Y,pRandomChoice)
 
 if random.random()>pRandomChoice:
  maxScore=max([dScore, sScore, tScore, hScore])
  if dScore==maxScore:
   return "Dragonslayer"
  if sScore==maxScore:
   return "Serpentyne"
  if tScore==maxScore:
   return "Thought-Talon"
  if hScore==maxScore:
   return "Humblescrumble"
 
 return random.choice(["Dragonslayer", "Serpentyne", "Thought-Talon","Humblescrumble"])

def gen_student(Y=1000):
 lect=gen_stat()
 rity=gen_stat()
 cour=gen_stat()
 refl=gen_stat()
 pati=gen_stat()
 
 dragScore=gen_drag_score(lect,rity,cour,refl,pati)
 thouScore=gen_thou_score(lect,rity,cour,refl,pati)
 serpScore=gen_serp_score(lect,rity,cour,refl,pati)
 humbScore=gen_humb_score(lect,rity,cour,refl,pati)
 
 House = allocate_student(dragScore, serpScore, thouScore, humbScore, Y)
 if House=="Dragonslayer":
  Score=dragScore
 if House=="Thought-Talon":
  Score=thouScore
 if House=="Serpentyne":
  Score=serpScore
 if House=="Humblescrumble":
  Score=humbScore
 
 return lect, rity, cour, refl, pati, dragScore, thouScore, serpScore, humbScore, House, Score

def gen_class(N, Y=1000):
 classDict = {"Intellect":[], "Integrity":[], "Courage":[], "Reflexes":[], "Patience":[], "dScore":[], "tScore":[], "sScore":[], "hScore":[], "House":[],"Score":[], "Ofstev Rating":[]}
 for i in range(N):
  lect, rity, cour, refl, pati, dragScore, thouScore, serpScore, humbScore, House, Score = gen_student(Y)
  classDict["Intellect"].append(lect)
  classDict["Integrity"].append(rity)
  classDict["Courage"].append(cour)
  classDict["Reflexes"].append(refl)
  classDict["Patience"].append(pati)
  
  classDict["dScore"].append(dragScore)
  classDict["tScore"].append(thouScore)
  classDict["sScore"].append(serpScore)
  classDict["hScore"].append(humbScore)
  
  classDict["House"].append(House)
  classDict["Score"].append(Score)
  classDict["Ofstev Rating"].append(pseudoPoisson(Score, 4))
  
  
 return pd.DataFrame(classDict)
 


FINAL_YEAR = 2022

df = gen_class(20, 2022)
df["Year"]=FINAL_YEAR

df.to_csv('eval.csv')

pd.options.display.max_rows=100

print(df)
print(df.sum())



STARTING_YEAR = 1511

df = gen_class(61, STARTING_YEAR)
df["Year"]=STARTING_YEAR

for year in range(STARTING_YEAR+1, 2022):
 if year<2000:
  Nstudents = pseudoPoisson(403, 10)
 else:
  Nstudents = pseudoPoisson(403-(year-1980)*5, 10)
 
 newDf=gen_class(Nstudents, year)
 newDf["Year"]=year
 
 df = df.append(newDf)

df=df.reset_index(drop=True)
df=df[1:]

pd.options.display.max_rows=100

print(df)
print(df.sum())

df=df[["Intellect", "Integrity", "Courage", "Reflexes", "Patience", "House","Ofstev Rating","Year"]]

df.to_csv('dset.csv')
