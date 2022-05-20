# Imports
import tkinter as tk
import random, math, time
import matplotlib.pyplot as plt
from delaunay import randomized_incremental_delaunay
from divide_delaunay import div_and_conq_delaunay
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

# Root Creation
root = tk.Tk()
root.title('Delaunay Triangulation Visualizer and Analyzer')
root.geometry("750x750")

# Create frame
main_frame = tk.Frame(root)
main_frame.pack()

def CreateRandomPointsOfArray(n):
    """
    Generate a random set of points in 2D
    """
    global count
    count = 0
    return [[random.uniform(0, 10000), random.uniform(0, 10000)] for i in range(n)]

pointSet = CreateRandomPointsOfArray(0)

fig = plt.Figure(figsize = (4, 3), dpi = 100)
ax = fig.add_subplot(111)
scatter3 = FigureCanvasTkAgg(fig, root)    
widget = scatter3.get_tk_widget()
widget.pack(fill=tk.BOTH)
    
# creating the Matplotlib toolbar
toolbar = NavigationToolbar2Tk(scatter3, root)
toolbar.update()
    
# placing the toolbar on the Tkinter window
scatter3.get_tk_widget().pack()

text = tk.StringVar()
algorithm = "Incremental"

# Methods
def CreateAndDraw():
    global algorithm
    algorithm = "Incremental"
    n = int(text_input.get(1.0, "end-1c"))

    # plot the triangulation (draw)
    clear_graph()
    Draw(n)

def CreateAndDrawDivide():
    global algorithm
    algorithm = "Divide&Conquer"
    n = int(text_input.get(1.0, "end-1c"))

    # plot the triangulation (draw)
    clear_graph()
    Draw(n)
    
def AddPoint():
    global pointSet
    clear_graph()
    xy = text_input1.get(1.0, "end-1c")
    splitted = [float(x) for x in xy.split()]
    pointSet.append(splitted)
    TriangulateAndPlot()
    
def RemovePoint():
    global pointSet
    clear_graph()
    xy = text_input2.get(1.0, "end-1c")
    splitted = [float(x) for x in xy.split()]
    pointSet.remove(splitted)
    
    if ( len(pointSet) == 0):
        ClearPoints()
    else:
        TriangulateAndPlot()

def Draw(n):
    global pointSet
    pointSet = CreateRandomPointsOfArray(n)
    TriangulateAndPlot()
    
def add_triangle_to_plot(plt, triangle):
    plt.plot([triangle[0][0], triangle[1][0]], [triangle[0][1],
             triangle[1][1]], color='k', linestyle='-', linewidth=1)
    plt.plot([triangle[0][0], triangle[2][0]], [triangle[0][1],
             triangle[2][1]], color='k', linestyle='-', linewidth=1)
    plt.plot([triangle[1][0], triangle[2][0]], [triangle[1][1],
             triangle[2][1]], color='k', linestyle='-', linewidth=1)

def add_edge_to_plot(plt, edge):
    plt.plot([edge.from_[0], edge.to[0]], [edge.from_[1], edge.to[1]]
                 , color='k', linestyle='-', linewidth=1)
    
def plot_triangulation(triangles, pointSet):
    global algorithm
    ax.scatter([p[0] for p in pointSet], [p[1] for p in pointSet])

    if algorithm == "Incremental":
        for triangle in triangles:
            add_triangle_to_plot(ax, triangle)
    else:
        for edge in triangles:
            add_edge_to_plot(ax, edge)

    scatter3.draw()

def clear_graph():
    global ax, widget
    ax.clear()
    widget.place_forget()
    
def RotateShape():
    clear_graph()
    global pointSet
    degree = float(text_input3.get(1.0, "end-1c"))
    degree %= 360
    cos = float(format(math.cos(math.radians(degree)), '.8f'))
    sin = float(format(math.sin(math.radians(degree)), '.8f'))
    for points in pointSet:
        # x cos + y sin
        X = points[0] * cos + points[1] * sin
        # -x sin + y cos
        Y = -points[0] * sin + points[1] * cos
        
        points[0] = X
        points[1] = Y
    
    TriangulateAndPlot()
    
def ClearPoints():
    global pointSet
    pointSet = CreateRandomPointsOfArray(0)
    clear_graph()
    scatter3.draw()

def TriangulateAndPlot():
    global pointSet, triangulation, algorithm
    start_time = time.time()
    
    if algorithm == "Incremental":
        triangulation = randomized_incremental_delaunay(pointSet)
    else:
        triangulation = div_and_conq_delaunay(pointSet)
    print(time.time() - start_time)
    changeText("With " + str(len(pointSet)) + " inputs, the " + algorithm + " algorithm took --- %s seconds ---" % (time.time() - start_time))
    plot_triangulation(triangulation, pointSet)

def changeText( var):
    text.set(var)

def SimulateShape():
    global pointSet, triangulation, count
    ax.scatter([p[0] for p in pointSet], [p[1] for p in pointSet])
    
    if ( algorithm == "Incremental" and count < len(triangulation)):
        add_triangle_to_plot(ax, triangulation[count])
        count += 1
        scatter3.draw()
        
    if ( algorithm == "Divide&Conquer" and count < len(triangulation)):
        add_edge_to_plot(ax, triangulation[count])
        count += 1
        scatter3.draw()

# Label Creation
label6 = tk.Label(root, text='To start the simulation, you must first press the Clear button.\nEach press of the simulation button advances a triangulation step.')
label6.pack()

# Button Creation
button_SimulateShape = tk.Button(root, text="Simulate Shape", command=SimulateShape)
button_SimulateShape.pack()

# Label Creation
label = tk.Label(root, text='Enter number of points')
label.pack()

# TextBox Creation
text_input = tk.Text(root, height = 1, width = 10)
text_input.pack()

# Button Creation
button_CreateAndDraw = tk.Button(root, text="Create and Draw with Incremental Algorithm", command=CreateAndDraw)
button_CreateAndDraw.pack()

# Button Creation
button_CreateAndDraw = tk.Button(root, text="Create and Draw with Divide&Conquer Algorithm", command=CreateAndDrawDivide)
button_CreateAndDraw.pack()

# Label Creation
label2 = tk.Label(root, text='Enter a point (x y):')
label2.pack()

# TextBox Creation
text_input1 = tk.Text(root, height = 1, width = 10)
text_input1.pack()

# Button Creation
button_AddPoint = tk.Button(root, text="Add Point", command=AddPoint)
button_AddPoint.pack()

# Label Creation
label3 = tk.Label(root, text='Remove a point (x y):')
label3.pack()

# TextBox Creation
text_input2 = tk.Text(root, height = 1, width = 10)
text_input2.pack()

# Button Creation
button_RemovePoint = tk.Button(root, text="Remove Point", command=RemovePoint)
button_RemovePoint.pack()

# Label Creation
label4 = tk.Label(root, text='Enter a degree:')
label4.pack()

# TextBox Creation
text_input3 = tk.Text(root, height = 1, width = 10)
text_input3.pack()

# Button Creation
button_RotateShape = tk.Button(root, text="Rotate Shape", command=RotateShape)
button_RotateShape.pack()

# Button Creation
button_ClearPoints = tk.Button(root, text="Clear Shape and Points", command=ClearPoints)
button_ClearPoints.pack()

# Label Creation
label5 = tk.Label(root, textvariable=text)
label5.pack()

# MainLoop
root.mainloop()