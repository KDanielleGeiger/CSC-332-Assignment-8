import sys
from tkinter import *
from functools import partial
import matplotlib.pyplot as plot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

errorLbl = None
adjMatrixLbl = None
adjListLbl = None
listbox = None
listbox2 = None
trackingLbl = None
orderLbl = None

def main():
    window = Tk()
    window.geometry('900x580')
    window.title('Depth-first Search')

    ##  Left frame for user input and adjacency matrix
    frameLeft = Frame(window)
    frameLeft.grid(row=0, column=0, sticky=N)
    ##  Right frame for adjacency list and other tables
    frameRight = Frame(window)
    frameRight.grid(row=0, column=1)

    ##  Exit button
    quitBtn = Button(frameRight, text='Quit')
    quitBtn.config(command=partial(quitProgram, window))
    quitBtn.grid(row=4, column=0, padx=(480,10), pady=(545,8), sticky=E)
    
    ##  Create user input prompt
    lbl = Label(frameLeft, text='Enter a list of adjacent nodes (Ex: AB,BC,AC):', fg='grey40')
    lbl.grid(row=0, column=0, columnspan=2, padx=(10,10), pady=(10,0), sticky=W)

    entry = Entry(frameLeft, relief=FLAT, width=50)
    entry.grid(row=1, column=0, columnspan=2, padx=(10,0), pady=(0,10), sticky=W)

    button = Button(frameLeft, text='Submit')
    button.config(command=partial(submit, frameLeft, frameRight, entry, quitBtn))
    button.grid(row=1, column=2, padx=(4,10), pady=(0,10), sticky=W)

    window.mainloop()

##  Convert input to an array of edges and an array of nodes
def convertEntry(entry):
    valid = True
    err = ''
    
    entry = entry.split(',')
    nodes = []
    edges = []
    
    for i in entry:
        i = i.strip()
        ##  Check that each edge connects exactly 2 nodes
        if len(i) != 2:
            valid = False
            err = 'ERROR: Each edge must connect two nodes.'
            break
        ##  Make sure a node does not connect to itself
        if i[0] == i[1]:
            valid = False
            err = 'ERROR: A node cannot connect to itself.'
            break
        ##  Make sure the same edge isn't listed twice
        if i in edges:
            valid = False
            err = 'ERROR: There can\'t be 2 edges joining the same nodes.'
            break
        if i[::-1] in edges:
            valid = False
            err = 'ERROR: There can\'t be 2 edges joining the same nodes.'
        ##  Add a node to the nodes array if necessary
        if i[0] not in nodes:
            nodes.append(i[0])
        if i[1] not in nodes:
            nodes.append(i[1])
        edges.append(i)

    ##  Sort nodes and edges in ascending order
    nodes.sort()
    for i in range(0, len(edges)):
        edges[i] = ''.join(sorted(edges[i]))
    edges.sort()

    return edges, nodes, valid, err

##  Display an error if there is one
def displayError(frameLeft, valid, err):
    global errorLbl

    ##  Remove current error label
    if errorLbl != None:
        errorLbl.destroy()

    ##  If user entry is not valid, display an error message
    if valid == False:
        errVar = StringVar()
        errVar.set(err)

        errorLbl = Label(frameLeft, textvariable=errVar, fg='red')
        errorLbl.grid(row=2, column=0, columnspan=2, padx=(10,10), sticky=W)

##  Create and display the adjacency matrix
def createMatrix(frameRight, edges, nodes):
    plot.close('all')

    figure = plot.figure()
    chart = figure.add_subplot(111)

    ##  Create and format ticks
    length = len(nodes)
    xlim = length
    ylim = length

    chart.set_xlim(left=0, right=xlim)
    chart.set_ylim(bottom=ylim, top=0)
    chart.xaxis.tick_top()
    chart.set_xticks(range(0, xlim, 1))
    chart.set_yticks(range(0, ylim, 1))
    chart.set_xticks([i+0.5 for i in range(0, xlim)], minor=True)
    chart.set_yticks([i+0.5 for i in range(0, ylim)], minor=True)
    chart.xaxis.set_major_formatter(plot.NullFormatter())
    chart.yaxis.set_major_formatter(plot.NullFormatter())
    chart.set_xticklabels(nodes, minor=True)
    chart.set_yticklabels(nodes, minor=True)
    chart.tick_params(axis='both', which='minor', length=0, width=0)
    chart.grid(True)

    ##  Fill in matrix
    for i in range(0, length):
        for j in range(0, length):
            edge = '%s%s' % (nodes[i],nodes[j])
            
            if edge in edges:
                num = 1
            elif edge[::-1] in edges:
                num = 1
            else:
                num = 0

            x = i + 0.5
            y = j + 0.5
            chart.text(x, y, num, ha='center', va='center', color='blue')

    ##  Label the matrix as "Adjacency Matrix"
    global adjMatrixLbl
    if adjMatrixLbl == None:
        adjMatrixLbl = Label(frameRight, text='Adjacency Matrix', fg='grey40')
        adjMatrixLbl.grid(row=0, column=0, padx=(80,10), pady=(10,0))

    ##  Display the matrix in the UI
    canvas = FigureCanvasTkAgg(figure, master=frameRight)
    canvas.draw()
    canvas.get_tk_widget().grid(row=1, column=0, padx=(80,10), pady=(0,10))
    canvas.get_tk_widget().config(width=300, height=300)

##  Output Adjacency List
def formatAdjList(nodes, edges):
    strings = ["" for x in range(len(nodes))]

    for x in range (0, len(nodes)):
        ## Add Node as start of list 
        strings[x] += nodes[x] 
        for y in range (0, len(edges)):
            temp = edges[y]
            ## If current Node exists in edge, then add the other node to the string
            if(temp[0] == nodes[x]):
                strings[x] += " ->" + temp[1]
            elif(temp[1] == nodes[x]):
                strings[x] += " ->" + temp[0]
        ## End every string with this
        strings[x] += " -> /"
        
    return(strings)

##  Display Adjacency List
def displayAdjList(frameRight, adjList):
    global adjListLbl
    global listbox

    ##  Label the list as "Adjacency List"
    if adjListLbl == None:
        adjListLbl = Label(frameRight, text='Adjacency List', fg='grey40')
        adjListLbl.grid(row=2, column=0, padx=(80,10), pady=(10,0))

    ##  Display the listbox in the UI
    if listbox == None:
        listbox = Listbox(frameRight, width=50, relief=FLAT)
        scrollbar = Scrollbar(frameRight, orient=VERTICAL)
        listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)
        listbox.grid(row=3, column=0, padx=(80,10), pady=(0,10))
        scrollbar.grid(row=3, column=0, padx=(80,10), pady=(0,10), sticky=E+NS)

    ##  Add data to listbox
    listbox.delete(0, END)
    for i in adjList:
        listbox.insert(END, i)

##  Display tracking tables
def displayTables(frameLeft, adjTables):
    global listbox2
    global trackingLbl

    ##  Label the list as "Tracking Tables"
    if trackingLbl == None:
        trackingLbl = Label(frameLeft, text='Tracking Tables', fg='grey40')
        trackingLbl.grid(row=4, column=0, columnspan=3, padx=(10,10), pady=(10,0))

    ##  Display the list in the UI
    if listbox2 == None:
        listbox2 = Listbox(frameLeft, width=80, height=21, relief=FLAT)
        scrollbar2 = Scrollbar(frameLeft, orient=VERTICAL)
        listbox2.config(yscrollcommand=scrollbar2.set)
        scrollbar2.config(command=listbox2.yview)
        listbox2.grid(row=5, column=0, columnspan=3, padx=(10,10), pady=(0,10))
        scrollbar2.grid(row=5, column=0, columnspan=3, padx=(10,10), pady=(0,10), sticky=E+NS)

    ##  Add tables to the listbox
    listbox2.delete(0, END)
    for i in adjTables:
        listbox2.insert(END, i)

##  Display visit order
def displayVisitOrder(frameLeft, order):
    global orderLbl

    order = 'Visit Order: %s' % order
    
    orderVar = StringVar()
    orderVar.set(order)

    if orderLbl == None:
        orderLbl = Label(frameLeft, textvariable=orderVar, fg='blue')
        orderLbl.grid(row=3, column=0, columnspan=3, padx=(10,10), pady=(80,0))

##  Exit the program
def quitProgram(window):
    plot.close('all')
    window.destroy()
    sys.exit()

##  Submit user input
def submit(frameLeft, frameRight, entry, quitBtn):
    ##  Check user entry
    entry = entry.get()
    ##  Check and convert the input to something more useful
    edges, nodes, valid, err = convertEntry(entry)
    ##  Display an error if there is one
    displayError(frameLeft, valid, err)

    ##  Exit function if there is an error
    if valid == False:
        return

    ##  Regrid the quit button before other UI elements are added
    quitBtn.grid_forget()
    quitBtn.grid(row=4, column=0, padx=(0,7), sticky=E)
    
    ##  Display adjacency matrix
    createMatrix(frameRight, edges, nodes)
    ##  Display adjacency list
    adjList = formatAdjList(nodes, edges)
    displayAdjList(frameRight, adjList)
    ##  Display tracking tables
    displayTables(frameLeft, ['Testing', '123'])
    ##  Display visit order
    displayVisitOrder(frameLeft, 'Testing 123')

if __name__ == '__main__':
    main()
