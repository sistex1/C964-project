import tkinter as tk
import plots as p
import model_init


glass_types=["Building Windows (Float Processed)", "Building Windows (Non-Float Processed)","Vehicle Windows",
             "Containers", "Tableware", "Headlamps" ]

def center_window(window):
    window.update_idletasks()
    w = 600
    h = 500
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - w) // 2
    y = ((screen_height - h) // 2) - 100
    window.geometry(f"{w}x{h}+{x}+{y}")


def validate_input(value, min_val, max_val):
    try:
        value = float(value)
        if value < min_val:
            return str(min_val)
        elif value > max_val:
            return str(max_val)
        else:
            return value
    except ValueError:
        return str(min_val)


def submit_data():
    prediction_list=[]
    output = ""
    for element, var in spinboxes.items():
        output += f"{element}: {var.get()}%\n"
        prediction_list.append(var.get())
    output += f"Refractive Index: {ri_var.get()}\n"
    prediction_list.insert(0, ri_var.get())
    print(prediction_list)
    user_prediction = str(model_init.input_predict(prediction_list))
    print(user_prediction)
    output = f"These glass qualities point to glass type {user_prediction}: Meant for {glass_types[int(user_prediction)-1]}" + "\n"+ output
    output_text.config(state=tk.NORMAL)
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, output)
    output_text.config(state=tk.DISABLED)


def bargraph_window():
    plot_window = tk.Toplevel(window)
    plot_window.title("Glass Type Distribution")
    p.barGraph(plot_window)


def pairplot_window():
    plot_window = tk.Toplevel(window)
    plot_window.title("Pair Plot of Dataset")
    p.pairplot(plot_window)


def boxplot_window():
    plot_window = tk.Toplevel(window)
    plot_window.title("Box Plot of Dataset")
    p.boxplots(plot_window)

def show_metrics():
    a, b, c, d = model_init.metrics
    output_text.config(state=tk.NORMAL)
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, f"Accuracy: {a:.4f}\n")
    output_text.insert(tk.END, f"Precision: {b:.4f}\n")
    output_text.insert(tk.END, f"Recall: {c:.4f}\n")
    output_text.insert(tk.END, f"F1 Score: {d:.4f}\n")
    output_text.config(state=tk.DISABLED)

model_init.train_model()


window = tk.Tk()
window.title("Glass Classifier")
center_window(window)
window.resizable(False, False)


elements = {
    "Na (Sodium)": (10, 20),
    "Mg (Magnesium)": (0, 6),
    "Al (Aluminum)": (0, 5),
    "Si (Silicon)": (68, 77),
    "K (Potassium)": (0, 7),
    "Ca (Calcium)": (4, 18),
    "Ba (Barium)": (0, 5),
    "Fe (Iron)": (0, 1)
}

spinboxes = {}

for i in range(5):
    window.grid_rowconfigure(i, weight=0)

tk.Label(window, text="Weight Percentages", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=4, padx=10,
                                                                             pady=10, sticky="w")


for i, (element, (min_val, max_val)) in enumerate(elements.items()):
    row = (i // 2) + 1
    col = i % 2
    tk.Label(window, text=element).grid(row=row, column=col * 2, padx=10, pady=5, sticky="w")
    var = tk.DoubleVar()
    validate_cmd = (window.register(lambda v, min_v=min_val, max_v=max_val: validate_input(v, min_v, max_v)), "%P")
    spinbox = tk.Spinbox(window, from_=min_val, to=max_val, increment=0.001, textvariable=var, width=10)
    spinbox.grid(row=row, column=col * 2 + 1, padx=10, pady=5)
    spinboxes[element] = var

tk.Label(window, text="Glass Properties", font=("Arial", 12, "bold")).grid(row=row + 1, column=0, columnspan=4, padx=10,
                                                                           pady=10, sticky="w")

tk.Label(window, text="Refractive Index").grid(row=row + 2, column=0, padx=10, pady=5, sticky="w")
ri_var = tk.DoubleVar()
ri_spinbox = tk.Spinbox(window, from_=1.4, to=1.7, increment=0.001, textvariable=ri_var, width=10)
ri_spinbox.grid(row=row + 2, column=1, padx=10, pady=5)

submit_button = tk.Button(window, text="Submit", command=submit_data)
submit_button.grid(row=row + 2, column=3, padx=10, pady=5)

output_text = tk.Text(window, height=10, width=70, wrap=tk.WORD)
output_text.grid(row=row + 3, column=0, columnspan=4, padx=10, pady=10)

button1 = tk.Button(window, text="View Glass Type Distribution", command=bargraph_window, wraplength=100)
button1.grid(row=row + 4, column=0, padx=10, pady=5)

button2 = tk.Button(window, text="View Glass Type Pairwise Trends", command=pairplot_window, wraplength=100)
button2.grid(row=row + 4, column=1, padx=10, pady=5)

button3 = tk.Button(window, text="View Element Weight % By Glass Type", command=boxplot_window, wraplength=100)
button3.grid(row=row + 4, column=2, padx=10, pady=5)

button4 = tk.Button(window, text="Show ML Model Performance Metrics", wraplength=100, command=show_metrics)
button4.grid(row=row + 4, column=3, padx=10, pady=5)

window.mainloop()
