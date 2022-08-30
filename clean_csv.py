# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 09:17:14 2022

@author: Rjjam
"""
import re
import pandas as pd

#Pokemon Information Github location
url = "https://gist.githubusercontent.com/armgilles/194bcff35001e7eb53a2a8b441e8b2c6/raw/92200bc0a673d5ce2110aaad4544ed6c4010f687/pokemon.csv"



#clean pokemon names and remove mega
def clean_names(pokemon_name):
    
    if re.search('.*Mega.*', pokemon_name):
        index = re.search('Mega.*', pokemon_name).start()
        
        return pokemon_name[index:]
    else:
        return pokemon_name

def clean_moves(movesets):
    
    for column in movesets.columns:
        movesets[column] = movesets[column].astype(str).str.replace("TM", "", regex = True)



def clean_data():
    
    #load csv's
    pokedex = pd.read_csv(url, index_col = 0)
    movesets = pd.read_csv("data/movesets.csv")
    
    #Removing other characters from Mega Pokemon
    pokedex["Name"] = pokedex["Name"].apply(clean_names)
    
    #Replace lengendary True and False with "Yes" & "No"
    pokedex["Legendary"] = pokedex["Legendary"].apply(lambda x: "Yes" if x == True else "No")
    
    #Save cleaned pokedex to csv
    pokedex.to_csv('data/pokedex.csv', index = True, encoding='utf-8')
    
    # Remove columns with TM movelists
    clean_moves(movesets)
    
    #Save as new csv file
    movesets.to_csv('data/movesets_modified.csv', index = True, encoding='utf-8')
    
    
if __name__ == "__main__":
    clean_data()

