# Prototype for Koutashi Manga Progress Checker

from tkinter import *
import tkinter as tk
import sys
import os
import pickle

root = Tk()
root.title('Sample')
root.geometry('400x400')
pickle_out = open('data.pickle','rb')
dct = pickle.load(pickle_out)
pickle_out.close()
dataOpen = False
updatePickle = open('updateList.pickle','rb')
updatePickleDictionary = updatePickle.load(updatePickle)
updatePickle.close()

sampleString = tk.StringVar()

def cleanDirectoryPathName(originalPathName):
    cleanedPath = ''
    for i in originalPathName:
        cleanedPath += i
    return cleanedPath

def mappedFolderNames(directoryList, mangaTitle):
    cleanedDirectoryList, updateListDeclaration = [], []
    titleCheck = '_'.join(x for x in mangaTitle.split())
    #check if folder format came from MangaFreak
    if titleCheck == directoryList[0][:len(titleCheck)]:
        for i in range(len(directoryList)):
            cleanedDirectoryList.append((float(directoryList[i][len(titleCheck)+1:]),directoryList[i]))
            updateListDeclaration.append((float(directoryList[i][len(titleCheck)+1:]), False)
    #else, manual chapter check
    else:
        for i in range(len(directoryList)):
            title = directoryList[i]
            for j in range(len(title)):
                if title[j:j+7] == 'Chapter':
                    value = ''
                    for k in range(j+8,len(title)):
                        if (title[k] >= '0' and title[k] <= '9') or title[k] == '.':
                            value += title[k]
                        else:
                            break
                    cleanedDirectoryList.append((float(value),title))
                    updateListDeclaration.append((float(directoryList[i][len(titleCheck)+1:]), False)
                    break
    return (sorted(cleanedDirectoryList),sorted(updateListDeclaration))

def viewFolder(pathName, mangaTitle, index):
    #filler function for viewManga()
    os.system("explorer.exe " + pathName)
    updatePickleDictionary[mangaTitle][index][1] = True
    #update if already read

def viewManga(mangaTitle,pathName):
    newFrame = Toplevel()
    folderList = dct[mangaTitle]
    labels, buttons = [], []
    for i in range(10):
        Label(newFrame, text=folderList[i][0]).pack()
        pathValue = pathName+'\\'+folderList[i][1]
        if not updatePickleDictionary[mangaTitle][i][1]:
            Button(newFrame,text='Open',command=lambda pathValue=pathValue: viewFolder(pathValue, mangaTitle, i)).pack()
        else:
            Label(newFrame, text='Already read').pack()

def addNewTitle(title,pathName):
    Label(root,text=title).pack()
    Button(root,text='View',command = lambda: viewManga(title,pathName)).pack()

def addMangaAndUpdate():
    pathName = sampleString.get()
    directoryList = os.listdir(pathName)
    mangaTitle = ''
    for i in range(len(pathName)-1,-1,-1):
        if pathName[i] == '\\':
            break
        mangaTitle = pathName[i] + mangaTitle
    (mappedDirectoryList, readMangaCounter) = mappedFolderNames(directoryList, mangaTitle)
    if mangaTitle not in dct:
        dct[mangaTitle] = mappedDirectoryList + [(len(mappedDirectoryList),pathName)]
        updatePickleDictionary[mangaTitle] = readMangaCounter
    listCount.set('Current list size: ' + str(len(dct)))
    addNewTitle(mangaTitle,pathName)

def destroyFrame(frame):
    global dataOpen
    pickle_out = open('data.pickle','wb')
    pickle.dump(dct,pickle_out)
    pickle_out.close()
    dataOpen = False
    frame.destroy()

def addToList():
    global dataOpen
    if not dataOpen:
        pickle_out = open('data.pickle','rb')
        dct = pickle.load(pickle_out)
        pickle_out.close()
        dataOpen = True
    secondFrame = Toplevel()
    secondFrame.geometry('250x100')
    secondFrame.title('Sample Title 2')
    sampleEntry1 = Entry(secondFrame,textvariable = sampleString,width=30).place(x=40,y=40)
    sampleBtn = Button(secondFrame,text='Add',command=lambda: [addMangaAndUpdate(), destroyFrame(secondFrame)])
    sampleBtn.place(x=40,y=70)

addBtn = Button(root,text='+',command=addToList)
addBtn.pack()
listCount = StringVar()
listCount.set('Current list size: ' + str(len(dct)))
addLbl = Label(root, textvariable=listCount)
addLbl.pack()
ind = 0
newLabel, newButton = [], []
for key,value in dct.items():
    newLabel.append(Label(root,text=key).pack())
    newButton.append(Button(root,text='View',command=lambda: viewManga(key,dct[key][-1][1])).pack())
    ind += 1
root.mainloop()

# when clicked, update the button as read and update the number of read files in the database
