from matplotlib import pyplot as plt
from matplotlib import style
import pandas as pd 
def plot_graph(symbol):
    read_file=pd.read_excel('{}.xlsx'.format(symbol))
    column=read_file[['open','close']]
    
    fig=plt.figure()
    fig.suptitle("{} open and close graph".format(symbol))
    ax1=fig.add_subplot(211)
    ax1.plot(column['open'])
    plt.grid()
    ax2=fig.add_subplot(212)
    ax2.plot(column['close'])
    plt.grid()
    
    
    plt.show()
    
    
    #plt.plot(column['open'])

    #plot_graph_close('')

    
plot_graph('AI')





"""
x=[5,8,10]
y=[12,16,6]

x2=[6,9,11]
y2=[6,15,7]

plt.plot(x,y,"g",label="line one",linewidth=5)
plt.plot(x2,y2,"r",label="line two",linewidth=10)
plt.legend()
plt.grid(True,color="y")

x=[5,8,10]
y=[12,16,6]
plt.plot(x,y)


plt.title("Graph")
plt.ylabel("Yaxis")
plt.xlabel("Xaxis")

plt.bar([5,8,10],[12,20,14],label="Example one")
plt.bar([2,3,4,6],[3,6,8,9],label="Example two",color='g')
plt.legend()
"""