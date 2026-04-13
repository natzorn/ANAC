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
                   "alpinists", 
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
                   "Red Banks",
                   "avalanche",
                   "mixed",
                   "McKinley",
                   "Fuhrer's Finger",
                   "Mount Shuksan",
                   ],
        "rock": ["crux", 
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
                 "Happy Hour Crag",
                 "Hidden Valley",
                 "Mount Brock",
                 "Kid Goat",
                 "Tohasket",
                 "Sunnyside",
                 "Devil's Lake",
                 "Snaz",
                 "Royal Arches",
                 "Smuggler's Notch",
                 "Old Man’s Route",
                 "Chapel Ledges",
                 "Open Book",
                 "Spaceshot",
                 "Windy Point",
                 "Recompense",
                 "The Nose",
                 "Feast of Snakes",
                 "Solarium",
                 "Thatcher Park",
                 "Mickey’s Beach",
                 "Sycamore Falls",
                 "Lemon Reservoir",
                 "Sturs Chimney",
                 "Star Trek Wall",
                 "Frothing Green",
                 "Cooper’s Rock",
                 "New River Gorge"
                 ],
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
                "Buttermilk Falls",
                "Pearl Necklace",
                ]}

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
          "helmeted"
          "wear a helmet",
          "wearing a helmet",
          "had a helmet on",
          "helmet was on",
          "put on helmet",
          "put on a helmet",
          "climbing helmet",
          "his helmet",
          "her helmet",
          "their helmet",
          "helmet proved",
          "helmet saved",
          "helmet prevented",
          "helmet took",
          "helmet absorbed",
          "helmet protected"]
no_helmet = ["no helmet", 
             "not wearing a helmet",
             "helmet recommended"
             "not wearing helmet",
             "without a helmet",
             "without helmet",
             "no helmets",
             "neither climber was wearing a helmet",
             "neither was wearing a helmet",
             "was not wearing a helmet",
             "were not wearing helmets",
             "had removed his helmet",
             "had removed her helmet",
             "helmet was removed",
             "took off helmet",
             "removed helmet"]
    


#fucntions for tags
def safe_text(text):
    if pd.isna(text):
        return ""
    
    text = text.lower()
    text = text.replace("-", " ")
    return text

def tag_climb(text):
    text = safe_text(text)
    if not text:
        return []
    
    tags = []
    for tag, keywords in climb_tag.items():
        for k in keywords:
            if k.lower() in text:
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

    rope_score = 0
    no_rope_score = 0

    if re.search(r"(unknown|unclear|not known).{0,10}(rope|belay)", text):
        return "unknown"

    if re.search(r"(solo|free solo|soloing|unroped|without rope)", text):
        no_rope_score += 2

    if re.search(r"(no belay|not belayed)", text):
        no_rope_score += 2

    if re.search(r"(scramble|scrambling)", text):
        no_rope_score += 1

    if re.search(r"(belay|belayed|on belay)", text):
        rope_score += 2

    if re.search(r"(rappel|rappelling|rappelled)", text):
        rope_score += 2

    if re.search(r"(lowered|lowering)", text):
        rope_score += 2

    if re.search(r"(tied in|rope team|fixed line)", text):
        rope_score += 2

    if re.search(r"(leader|leading|lead climber)", text):
        rope_score += 2

    if re.search(r"(second|seconding|follower)", text):
        rope_score += 2

    if re.search(r"(pitch|multi pitch|pitch)", text):
        rope_score += 1

    if re.search(r"(caught|held).{0,10}rope", text):
        rope_score += 2

    if rope_score > no_rope_score and rope_score >= 1.5:
        return "rope"
    if no_rope_score > rope_score and no_rope_score >= 1.5:
        return "no_rope"

    return "unknown"


def tag_helmet(text):
    text = safe_text(text)

    if re.search(r"(unknown|unclear|not known).{0,10}helmet", text):
        return "unknown"

    if re.search(r"(might|may|could|would).{0,15}helmet", text):
        return "unknown"

    if re.search(r"(no|not|without|lacked|unhelmeted|bareheaded).{0,15}(helmet|headgear|protection)", text):
        return "no_helmet"

    if re.search(r"(no headgear|no helmet|no protective headgear|without head protection)", text):
        return "no_helmet"

    if re.search(r"(wearing|wore|had|with|helmeted|put on).{0,10}helmet", text):
        return "helmet"

    if re.search(r"(his|her|their).{0,3}helmet", text):
        return "helmet"

    if re.search(r"(helmet).{0,10}(struck|hit|impacted|cracked|damaged|absorbed)", text):
        return "helmet"

    if re.search(r"(landed on|fell on).{0,10}helmet", text):
        return "helmet"

    if re.search(r"(helmet).{0,10}(came off|knocked off|lost|dislodged)", text):
        return "helmet"


    if any(k in text for k in no_helmet):
        return "no_helmet"
    
    if any(k in text for k in helmet):
        return "helmet"

    return "unknown"

df = pd.read_csv("ANAC_mp_loc.csv")
df.columns = df.columns.str.strip()


df['climb_tags'] = df['Text'].apply(tag_climb)

def primary_from_tags(tags):
    for p in priority:
        if p in tags:
            return p
    return "unknown"

df['climb_primary'] = df['climb_tags'].apply(primary_from_tags)

df['Helmet'] = df['Text'].apply(tag_helmet)
df['Rope'] = df['Text'].apply(tag_rope)

print(df['climb_primary'].value_counts())
print(df['Helmet'].value_counts())
print(df['Rope'].value_counts())








