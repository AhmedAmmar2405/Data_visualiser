import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def import_data():
    global data
    file= filedialog.askopenfilename()
    data =pd.read_csv(file)
    display_data()

def display_data():
    if 'data' in globals():
        text_area.config(state='normal')
        text_area.delete('1.0', tk.END)
        text_area.insert(tk.END, data.to_string(index=False))
        text_area.config(state='disabled')
        numerical_columns =data.select_dtypes(include=[np.number]).columns.tolist()
        column_select['values']=numerical_columns
        X['values']=data.columns.tolist()  
        Y['values']=data.columns.tolist()  

def calculate_statistics():
    if 'data' in globals():
        selected_column = column_select.get()
        if selected_column:
            selected_data = data[selected_column]
            mean = np.mean(selected_data)
            median = np.median(selected_data)
            std_dev = np.std(selected_data)
            messagebox.showinfo("Statistics", f"Mean: {mean}\nMedian: {median}\nStandard Deviation: {std_dev}")
        else:
            messagebox.showwarning("Warning", "Please select a column first.")

def plot():
    if 'data' in globals():
        selected_column = column_select.get()
        x_column = X.get()
        y_column = Y.get()
        if x_column and y_column:
            plt.figure(figsize=(6, 4))
            plt.scatter(data[x_column], data[y_column])
            plt.xlabel(x_column)
            plt.ylabel(y_column)
            plt.title(f'Scatter Plot: {x_column} vs {y_column}')
            fig = plt.gcf()
            canvas = FigureCanvasTkAgg(fig, master=frame)
            canvas.draw()
            canvas.get_tk_widget().grid(row=3, column=5, columnspan=2)
        else:
            messagebox.showwarning("Warning", "Please select X and Y variables.")
    else:
        messagebox.showwarning("Warning", "Insert data.")

root = tk.Tk()
root.title("DATA VISUALISER")
root.geometry("800x600")
# Configuration du cadre principal
frame=ttk.Frame(root,padding="10")

frame.grid(row=0,column=0,sticky=(tk.W,tk.E,tk.N,tk.S))

# Ajout du bouton pour importer les données
import_button = ttk.Button(frame, text="Import Data", command=import_data)
import_button.grid(row=0,column=0,pady=10,padx=10)

# Ajout d'une zone de texte pour afficher les données
text_area =tk.Text(frame,height=20,width=80,wrap=tk.NONE)
text_area.grid(row=3,column=0, pady=10,padx=10)

# Ajout du sélecteur de colonnes
column_select = ttk.Combobox(frame,state="readonly")
column_select.grid(row=1,column=0,pady=10,padx=10)

X = ttk.Combobox(frame,state="readonly")
X.grid(row=5,column=0,pady=10,padx=10)

Y=ttk.Combobox(frame,state="readonly")
Y.grid(row=6,column=0,pady=10,padx=10)

# Ajout du bouton pour calculer les statistiques
calculate_button=ttk.Button(frame,text="Calculate Statistics",command=calculate_statistics)
calculate_button.grid(row=2,column=0,pady=10,padx=10)

Tracer=ttk.Button(frame,text="Tracer",command=plot)
Tracer.grid(row=7,column=0,pady=10,padx=10)

#Ajoutdes barres de défilement
scrollbar_y=ttk.Scrollbar(frame,orient=tk.VERTICAL,command=text_area.yview)
scrollbar_y.grid(row=3,column=1,sticky=(tk.N,tk.S))
text_area.config(yscrollcommand=scrollbar_y.set)

scrollbar_x=ttk.Scrollbar(frame,orient=tk.HORIZONTAL,command=text_area.xview)
scrollbar_x.grid(row=4,column=0,sticky=(tk.W,tk.E))
text_area.config(xscrollcommand=scrollbar_x.set)

#Démarrage de la boucle principale de Tkinter
root.mainloop()
