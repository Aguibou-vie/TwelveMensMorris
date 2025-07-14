import tkinter as tk
#creation de la fenetre principale

root = tk.Tk()
root.title("Twelve Men's Morris")
root.geometry("800x800") # taille de la fenetre
#canvas dessin
canvas = tk.Canvas(root, width=800, height=800, bg="beige")
canvas.pack()

root.mainloop()