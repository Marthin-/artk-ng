#!/usr/bin/env python
import configparser
#import time
#import math
#import random
import readline

class MyCompleter(object):  # Custom completer

    def __init__(self, options):
        self.options = sorted(options)

    def complete(self, text, state):
        if state == 0:  # on first trigger, build possible matches
            if text:  # cache matches (entries that start with entered text)
                self.matches = [s for s in self.options 
                    if s and s.startswith(text)]
            else:  # no text entered, all matches possible
                self.matches = self.options[:]

    # return match indexed by state
        try: 
            return self.matches[state]
        except IndexError:
            return None


def help():
    print('''
              ______====TT====______
    ==========================================
    -- Cthulhu feuille de perso interactive --
    ==========================================
    | help.................afficher ce texte |
    | list..............lister les commandes |
    | set <cat.> <nom> <val.>.......modifier |
    |  -> ex.: set carac for 14              |
    | save.................sauver la feuille |
    | exit...........................quitter |
    ==========================================
    ||   utiliser <TAB> à tout moment pour  ||
    ||      l'autocompletion/suggestion     ||
    ==========================================
    ||  Cthulhu     _.(;,;)._   Ftahgn      ||
    ||             ^^^^(o)^^^^              ||
    ==========================================
    ''')


#    print("-- Cthulhu feuille de perso interactive --")
#    print(" Taper une des commandes suivantes pour voir")
#    print("   les informations du perso dans fp.txt :")
#    print("       Taper 'help' pour revoir ce texte")
#    print("         list pour lister les sections")
#    print("             ou 'exit' pour quitter")
#    print("---------------------------------------------")
#    print(" Pour changer une valeur taper ")
#    print(" set <catégorie> <nom> <valeur>")
#    print(" (ex. : set pv actuels 16)")
#    print("---------------------------------------------")
#    print("  Taper save pour sauvegarder la fiche /!\\")

def set_value(config, section, key, value=""):
    config[section][key] = value

def list(mylist):
    print("=======================")
    for key in mylist:
        print(key)
    print("=======================")

def menu():
    config = configparser.ConfigParser()
    config.read('fp.txt')
    help()
    auto=['exit', 'save', 'set', 'list']
    for key in config:
        auto.append(key)
    auto.remove('DEFAULT')
    readline.set_completer_delims('')
    completer = MyCompleter(auto[:])
    readline.set_completer(completer.complete)
    readline.parse_and_bind('tab: complete')
    while 1:
        rawcom = str(input("~^(;,;)^~ > "))
        if rawcom != '':
            com = rawcom.split(" ")[0]
        else:
            com = ''
        # à remplacer par une liste =_=
        if com != '' and com != 'list' and com != "atk" and com != 'svg' and com != 'set' and com != 'exit' and com != 'help' and com != 'save' and com != 'calc' and com != 'test':
            try:
                print("==== " + com.upper() + " ====")
                for key in config[com]:
                    print(key + ": " + config[com][key])
            except KeyError:
                print("Tape la bonne commande vieux bouc")
        elif com == 'exit':
            break
        elif com == 'help':
            help()
        elif com == 'set':
            try:
                toto = ' '.join(rawcom.split(" ")[3:])
            except IndexError:
                toto = ""
            set_value(config, rawcom.split(" ")[1], rawcom.split(" ")[2], toto)
        elif com == 'save':
            with open('fp.txt', 'w') as configfile:
                try:
                    config.write(configfile)
                    print("saved file [OK]")
                except:
                    print("could not save file!")
        elif com == '':
            help()
        elif com == 'list':
            list(auto)
        else:
            help()
if __name__ == "__main__":
    menu()
