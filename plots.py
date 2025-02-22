import matplotlib.pyplot as plt
import pandas as pd
import seaborn as s
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

data = pd.read_csv('glass.csv')



def barGraph(master):
    order = [1, 2, 3, 4, 5, 6]
    type_counts = data['Type'].value_counts()
    type_counts = type_counts[order]
    fig, ax = plt.subplots(figsize=(8, 6))
    type_counts.plot(kind='bar', color='skyblue', ax=ax)

    ax.set_xlabel('Glass Type')
    ax.set_ylabel('Count')
    ax.set_title('Distribution of Glass Types')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    canvas = FigureCanvasTkAgg(fig, master=master)
    canvas.draw()
    canvas.get_tk_widget().pack(side="top", fill="both", expand=True)


def pairplot(master):
    pplt = s.pairplot(data, hue='Type', palette='viridis', corner=True)
    plt.suptitle('Pairplot of Features Colored by Glass Type', y=1.02, fontsize=16)

    canvas = FigureCanvasTkAgg(pplt.fig, master=master)
    canvas.draw()
    canvas.get_tk_widget().pack(side="top", fill="both", expand=True)


def boxplots(master):
    plt.figure(figsize=(18, 12))

    for i, column in enumerate(data.columns[1:-1], 1):
        plt.subplot(3, 3, i)
        s.boxplot(x='Type', hue='Type', y=column, data=data, palette='viridis')
        plt.title(f'{column} by Glass Type', fontsize=12)

    plt.suptitle('Boxplots of Element Weight % by Glass Type', y=1.02, fontsize=16)
    plt.tight_layout()

    canvas = FigureCanvasTkAgg(plt.gcf(), master=master)
    canvas.draw()
    canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

