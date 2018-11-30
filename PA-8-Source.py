from tkinter import *
from functools import partial

errorLbl = None

def main():
    window = Tk()
    window.title('Depth-first Search')

    frameLeft = Frame(window)
    frameLeft.grid(row=0, column=0)
    frameRight = Frame(window)
    frameRight.grid(row=0, column=1)

    lbl = Label(frameLeft, text='Enter a list of adjacent nodes (Ex: AB,BC,AC):', fg='grey40')
    lbl.grid(row=0, column=0, columnspan=2, padx=(10,10), pady=(10,0), sticky=W)

    entry = Entry(frameLeft, relief=FLAT, width=50)
    entry.grid(row=1, column=0, columnspan=2, padx=(10,0), pady=(0,10), sticky=W)

    button = Button(frameLeft, text='Submit')
    button.config(command=partial(submit, frameLeft, frameRight, entry))
    button.grid(row=1, column=2, padx=(4,10), pady=(0,10))

    window.mainloop()

def convertEntry(entry):
    valid = True
    err = ''
    
    edges = entry.split(',')
    nodes = []
    
    for i in edges:
        if len(i) != 2:
            valid = False
            err = 'ERROR: Each edge must connect two nodes.'
            break
        if i[0] == i[1]:
            valid = False
            err = 'ERROR: A node cannot connect to itself.'
            break
        if i[0] not in nodes:
            nodes.append(i[0])
        if i[1] not in nodes:
            nodes.append(i[1])

    return edges, nodes, valid, err

def displayError(frameLeft, valid, err):
    global errorLbl

    if errorLbl != None:
        errorLbl.destroy()

    if valid == False:
        errVar = StringVar()
        errVar.set(err)

        errorLbl = Label(frameLeft, textvariable=errVar, fg='red')
        errorLbl.grid(row=2, column=0, padx=(10,10), sticky=W)
    
def submit(frameLeft, frameRight, entry):
    entry = entry.get()
    edges, nodes, valid, err = convertEntry(entry)
    displayError(frameLeft, valid, err)

    if valid == False:
        return

if __name__ == '__main__':
    main()
