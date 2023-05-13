import tkinter as tk
from final_project_2 import App,Data

if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    data = Data(root, "https://cloudbox.ku.ac.th/index.php/s/ERym8CC9zjzKGop/download", app)
    root.mainloop()