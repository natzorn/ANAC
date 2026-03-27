#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 14:32:00 2026

@author: nataliezorn
"""

"""
Tagging data based on incident occurence:
    - Type: Climbing, Skiing, Mountaineering
    - Roped or Unroped
    - Group Type (Solo, Duo, 3+)
    - Experience
    - Protection
    
Notes so far:
    - having trouble differetiating ice and alpine, most entries for ice/alpine have corresponding verbage
    - for now, im labeling ice climbing simply as those mentioned with ice climbers and will see what results look like
    - unfortunately, a camming protection piece is called a Friend, hopefully there is no other reference of friends
"""

import re
import pandas as pd
    
#climbing tags
climb_tag = {
        "alpine": ["alpine", 
                   "alpininists", 
                   "mountaineering", 
                   "mountaineers", 
                   "glissade", 
                   "summit", 
                   "face", 
                   "ridge", 
                   "gully", 
                   "couloir", 
                   "glacier", 
                   "cornice", 
                   "corniced", 
                   "crevasse", 
                   "col", 
                   "bergschrund", 
                   "third class", 
                   "fourth class", 
                   "class-four", 
                   "blade serac", 
                   "pinnacle", 
                   "summiting", 
                   "mountain", 
                   "peak", 
                   "Red Banks", ],
        "rock": ["led", 
                 "leading", 
                 "pitch", 
                 "crux", 
                 "slab", 
                 "slabs", 
                 "piton", 
                 "top rope", 
                 "top-rope", 
                 "Friend", 
                 "chock", 
                 "5.", 
                 "spire", 
                 "trad", 
                 "pillar", 
                 "rock climbing", 
                 "Trapps", 
                 "Robinson Park", 
                 "East Ledges", 
                 "Oak Creek Vista", 
                 "free climb", 
                 "bouldering", 
                 "boulder problem", 
                 "sport route", 
                 "quickdraws", 
                 "bolt", 
                 "Jill's Thrill", 
                 "bolts", 
                 "Empor", 
                 "Foothill Crag", 
                 "Church Vaults", 
                 "Coal Pit Gulch", 
                 "Blockbuster", 
                 "Three Pines", 
                 "Bruise Brothers wall", 
                 "sport climb", 
                 "Jolly Rodger", 
                 "top- roping", 
                 "sport climbing", 
                 "Directissima Route", 
                 "Hemateria", 
                 "East Buttress route", 
                 "Dire Straights", 
                 "The Bastille", 
                 "top-roping", 
                 "Parleys Canyon", 
                 "Chimney Pond", 
                 "Bastille Crack", 
                 "Rincon Wall", 
                 "Birdland", 
                 "Grasshopper", 
                 "Vertical Endeavors Climbing Gym", 
                 "Whitney Gilman rock climb", 
                 "Fairview Dome", 
                 "Solid Gold", 
                 "China Wall", 
                 "Condor Crag", 
                 "Commitment", 
                 "Boulderado Crag", 
                 "Delay of the Game", 
                 "Poudre Canyon", 
                 "Flatiron", 
                 "Happy Hour Crag"],
        "ice": ["ice climbers", 
                "ice-climbers", 
                "smear", 
                "ice-capped", 
                "crampon", 
                "ice climb", 
                "ice route", 
                "WI4 route", 
                "WI4", 
                "Ouray Ice Park", 
                "Buttermilk Falls"]}

#roping tags
roped = ["belay", 
         "belayers", 
         "climbing rope", 
         "figure 8", 
         "figure-8", 
         "roped", 
         "ropelengths", 
         "rappel", 
         "rappelled", 
         "rappelling", 
         "rope team", 
         "fixed line", 
         "tied in", 
         "Grade 3", ]
unroped = ["unroped",
           "scramble", 
           "scrambler", 
           "solo", 
           "downclimbing",
           "no rope"]

#helmet tags NEEDS UPDATINF
helmet = ["wearing helmet", 
          "wore helmet", 
          "with helmet", 
          "helmeted"]
no_helmet = ["no helmet", 
             "not wearing a helmet",
             "helmet recommended"]
    

#fucntions for tags
def safe_text(text):
    if pd.isna(text):
        return ""
    return text.lower()


def tag_climb(text):
    if pd.isna(text):
        return []
    
    text = text.lower()
    tags = []

    for tag, keywords in climb_tag.items():
        for k in keywords:
            k = k.lower()
            
            if " " in k:
                if k in text:   # phrase match
                    tags.append(tag)
                    break
            else:
                if re.search(rf"\b{re.escape(k)}\b", text):
                    tags.append(tag)
                    break

    return tags

priority = ["ice", "rock", "alpine"]

def tag_primary_climb(text):
    tags = tag_climb(text)
    for p in priority:
        if p in tags:
            return p
    return "unknown"

def tag_rope(text):
    text = safe_text(text)

    if any(k in text for k in unroped):
        return "no_rope"
    if any(k in text for k in roped):
        return "rope"

    return "unknown"


def tag_helmet(text):
    text = safe_text(text)

    if any(k in text for k in no_helmet):
        return "no_helmet"
    if any(k in text for k in helmet):
        return "helmet"

    return "unknown"


df = pd.read_csv("ANAC_mp_loc.csv")
df.columns = df.columns.str.strip()


df['climb_tags'] = df['Text'].apply(tag_climb)
df['climb_primary'] = df['climb_tags'].apply(lambda x: x[0] if x else "unknown")

df['Helmet'] = df['Text'].apply(tag_helmet)
df['Rope'] = df['Text'].apply(tag_rope)

print(df['climb_primary'].value_counts())
print(df['Helmet'].value_counts())
print(df['Rope'].value_counts())







