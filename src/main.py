import time
import datetime
import textwrap
import os
from random import randint
from tkinter import *
from tkinter.messagebox import askokcancel, askyesno, showinfo, showerror

### DROPDOWN TEXTS ###

SPC_MCD_PROB = [
    "*** CHOOSE AN OPTION ***",
    "SEVERE POTENTIAL...WATCH UNLIKELY", #5-30 percent
    "SEVERE POTENTIAL...WATCH POSSIBLE", #40-60 percent
    "SEVERE POTENTIAL...WATCH LIKELY", #70-90 percent
    "SEVERE POTENTIAL...WATCH NEEDED SOON", #95 percent
    "SEVERE POTENTIAL...TORNADO WATCH NEEDED", #95 percent
    "SEVERE POTENTIAL...SEVERE TSTM WATCH NEEDED" #95 percent
]

SPC_MCD_PERCENT = [
    "*** CHOOSE AN OPTION ***",
    "5 PERCENT",
    "10 PERCENT",
    "20 PERCENT",
    "30 PERCENT",
    "40 PERCENT",
    "50 PERCENT",
    "60 PERCENT",
    "70 PERCENT",
    "80 PERCENT",
    "90 PERCENT",
    "95 PERCENT"
]

SPC_MCD_EXPIRE = [
    "0000",
    "0100",
    "0200",
    "0300",
    "0400",
    "0500",
    "0600",
    "0700",
    "0800",
    "0900",
    "1000",
    "1100",
    "1200",
    "1300",
    "1400",
    "1500",
    "1600",
    "1700",
    "1800",
    "1900",
    "2000",
    "2100",
    "2200",
    "2300"
]

### VARIABLES AND SETTING TKINTER UP ###

wmoTiming = time.strftime("%d%H%M", time.gmtime())
expDay = time.strftime("%d", time.gmtime())

master = Tk()
master.title("SWIC SPC Mesoscale Discussion Tool")

bottom = Frame(master)
bottom.pack(side=BOTTOM, fill=BOTH, expand=True)

top = Frame(master)
top.pack(side=TOP, fill=BOTH, expand=True)

top2 = Frame(master)
top2.pack(side=TOP, fill=BOTH, expand=True)

wmo = "ACUS11 KWNS " + wmoTiming + "\nSWOMCD"
template = "MESOSCALE DISCUSSION #XXXX \nSWIC STORM PREDICTION CENTER INDIANAPOLIS IN\n" + str(time.strftime("%I%M %p EDT %a %b %d %Y")) + "\n"
upperCaseTemplate = template.upper()

### DEFINE QUITE LITERALLY EVERYTHING ###

def randomProdIdent(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def clearText():
    product.delete("1.0", "end-1c")
    setDefaultTextParamsForPlaceholder()
    prob.set(SPC_MCD_PROB[0])
    percent.set(SPC_MCD_PERCENT[0])
    exptime.set(SPC_MCD_EXPIRE[0])

def clickStates(*args):
    states.delete(1.0, "end")

def clickWfos(*args):
    wfos.delete(1.0, "end")

def clickMdNum(*args):
    mdnum.delete(1.0, "end")

def insertTemplate():
    if str(prob.get()) == "*** CHOOSE AN OPTION ***":
        prbget = "!* DID NOT SELECT PROBABILITY *!"
    else:
        prbget = prob.get()
    if str(percent.get()) == "*** CHOOSE AN OPTION ***":
        prcget = "!* DID NOT SELECT PERCENT *!"
    else:
        prcget = percent.get()
    if str(states.get("1.0", "end-1c")) == "":
        stsget = "!* DID NOT SELECT STATES *!"
    elif str(states.get("1.0", "end-1c")) == "Enter affected states":
        stsget = "!* DID NOT SELECT STATES *!"
    else:
        stsget = states.get("1.0", "end-1c")
    if str(wfos.get("1.0", "end-1c")) == "":
        wfoget = "!* DID NOT SELECT WFO(S) *!"
    elif str(wfos.get("1.0", "end-1c")) == "Enter affected WFOs":
        wfoget = "!* DID NOT SELECT WFO(S) *!"
    else:
        wfoget = wfos.get("1.0", "end-1c")
    product.insert(1.0, str(randomProdIdent(3)) + "\n" + wmo + "\n" + "SPC MCD " + wmoTiming + "\n" + stsget + "-" + str(expDay) + str(exptime.get()) + "-" + "\n\n" + upperCaseTemplate + "\nAREAS AFFECTED...\n" + "\n" + "CONCERNING..." + prbget + "\n\nVALID " + wmoTiming + "Z - " + str(expDay) + str(exptime.get()) + "Z\n\nPROBABILITY OF WATCH ISSUANCE..." + prcget + "\n\nSUMMARY...\n\nDISCUSSION...\n\n..FORECASTER.. " + time.strftime("%m/%d/%Y") + "\n\nPLEASE SEE SPC.SWIC.TK FOR GRAPHICAL PRODUCT.\n\nATTN...WFO..." + wfoget + "...")

# probabilities
prob = StringVar(master)
prob.set(SPC_MCD_PROB[0])

# percents
percent = StringVar(master)
percent.set(SPC_MCD_PERCENT[0])

# exp time
exptime = StringVar(master)
exptime.set(SPC_MCD_EXPIRE[0])

# prob menu
spcprob = OptionMenu(master, prob, *SPC_MCD_PROB)
spcprob.pack(in_=top, side=LEFT)

# percent menu
spcpercent = OptionMenu(master, percent, *SPC_MCD_PERCENT)
spcpercent.pack(in_=top, side=RIGHT)

# states input
states = Text(master, height=1, width=28)
states.pack(in_=top2, side=LEFT)

# wfos input
wfos = Text(master, height=1, width=28)
wfos.pack(in_=top2, side=RIGHT)

# clickaway for both states and wfos
states.bind("<FocusIn>", clickStates)
wfos.bind("<FocusIn>", clickWfos)

# product text box
product = Text(master, wrap=WORD, width=69)
product.pack()

# generate button
generateButton = Button(master, activebackground="#ffa500", activeforeground="#000000", height=1, width=10, text="Generate", command=lambda:insertTemplate())
generateButton.pack(in_=bottom, side=RIGHT)

# send button
sendButton = Button(master, activebackground="#32a852", activeforeground="#ffffff", height=1, width=10, text="Send", command=lambda:jmsSendProduct())
sendButton.pack(in_=bottom, side=RIGHT)

def jmsSendProduct():
    jmsSendConfirm = askyesno("Warning!", "***STOP!***\n\nYou are about to TRANSMIT a IN-HOUSE DEMO MESOSCALE DISCUSSION.\n\nThis sandbox environment is firewalled. If you choose to continue, the product will not leave your computer.\n\nContinue?")
    if jmsSendConfirm == True:
        data = str(product.get(1.0, "end"))
        parsedData = "".join(data)
        parsedUpperData = parsedData.upper()
        product.delete(1.0, "end")
        product.insert(1.0, parsedUpperData)
        showerror("Send Failed", "The text product was not transmitted.\n\nCould not connect to live server: This environment is sandboxed (403)")
    elif jmsSendConfirm == False:
        showinfo("Cancelled", "Operation was cancelled.")
    else:
        showerror("Exception", "An unknown error occurred.")

# expiration menu
spcexpire = OptionMenu(master, exptime, *SPC_MCD_EXPIRE)
spcexpire.pack(in_=bottom, side=RIGHT)

# clear button
clearButton = Button(master, height=1, width=10, text="Clear Text", command=lambda:clearText())
clearButton.pack(in_=bottom, side=LEFT)

def setDefaultTextParamsForPlaceholder():
    states.delete(1.0, "end")
    wfos.delete(1.0, "end")
    states.insert(1.0, "Enter affected states")
    wfos.insert(1.0, "Enter affected WFOs")

### INITIALIZE TEXT BOXES DEFAULT VALUES ###
setDefaultTextParamsForPlaceholder()

mainloop()
