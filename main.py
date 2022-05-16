import tkinter as tk
from tkinter import *
from tkinter import messagebox as msg
from tkinter.filedialog import *
import webbrowser
import os

def createComponents(): # Initializam functia

    # -------------------------------------  Definirea functiilor ------------------------------------- #

    def exit(): # Definim functia exit
        root.destroy() # Distruge fereastra(notpad-ul)

    def cut():
        global  textArea # Preluam textul global selectat
        textArea.event_generate("<<Cut>>") # Ne folosim de functia cut

    def copy():
        global textArea # Preluam textul global selectat
        textArea.event_generate("<<Copy>>") # Ne folosim de functia copy

    global p
    global currentline
    global direction
    global sw
    global sw2
    global wrap
    global match
    direction = 1
    p=0
    currentline = 1
    sw = 0
    sw2 = 0
    wrap = 0
    match = 0

    def find_word(w):
        global textArea # Preluam textul global selectat
        global p
        global currentline
        global direction
        global wrap
        global sw2

        sw2=1

        lines = int(textArea.index('end').split('.')[0]) - 1

        if(direction==1):
            global sw
            if (sw == 0):
                currentline = lines
                sw = 1

            if (p == 0 and w in textArea.get(str(currentline) + ".0", str(currentline) + ".0 lineend")):
                p = textArea.get(str(currentline) + ".0", str(currentline) + ".0 lineend").rindex(w)
            elif (p != -1 and w in textArea.get(str(currentline) + ".0", str(currentline) + ".0 lineend")):
                p = textArea.get(str(currentline) + ".0", str(currentline) + "." + str(p)).rindex(w)

            if ((w in textArea.get(str(currentline) + ".0", str(currentline) + "." + str(p + len(w)))) and len(w) > 0):
                textArea.tag_delete("selectedtext", 1.0, END)
                textArea.tag_add("selectedtext", str(currentline) + "." + str(p),str(currentline) + "." + str(p + len(w)))
                textArea.tag_config("selectedtext", background="#0078d7", foreground="white")
                if (textArea.get(str(currentline) + ".0", str(currentline) + "." + str(p + len(w))).index(w) == textArea.get(str(currentline) + ".0",
                        str(currentline) + "." + str(p + len(w))).rindex(w)):
                    p = -1

            elif (currentline != 1):
                currentline = currentline - 1
                p = 0
                find_word(w)
            else:
                if (wrap == 1):
                    p = 0
                    sw = 0
                    find_word(w)
                else:
                    msg.showinfo("Notepad",
                                 'Cannot find "' + w + '" ')  # Apelam functia si aplicam atribute / Afiseaza un text bar si intializeaza varibila choise cu alegerea ta
        else:
            if ((w in textArea.get(str(currentline) + "." + str(p), str(currentline) + ".0 lineend")) and len(w) > 0):
                p = p + textArea.get(str(currentline) + "." + str(p), END).index(w) + len(w) - 1
                textArea.tag_delete("selectedtext", 1.0, END)
                textArea.tag_add("selectedtext", str(currentline) + "." + str(p - len(w) + 1),
                                 str(currentline) + "." + str(p + 1))
                textArea.tag_config("selectedtext", background="#0078d7", foreground="white")
                if (len(w) == 1):
                    p = p + 1

            elif (currentline != lines):
                currentline = currentline + 1
                p = 0
                find_word(w)
            else:
                if (wrap == 1):
                    p = 0
                    currentline = 1
                    find_word(w)
                else:
                    msg.showinfo("Notepad",
                                 'Cannot find "' + w + '" ')  # Apelam functia si aplicam atribute / Afiseaza un text bar si intializeaza varibila choise cu alegerea ta

    def find():
        find_file = tk.Tk()  # Creezi fereastra pentru notpad
        find_file.title("Find")  # Afisezi fereastra cu titlul 'Untitled - Notepad'
        find_file.iconbitmap('npi.ico')
        find_file.maxsize(390,150)
        find_file.minsize(390,150)
        up = tk.IntVar(find_file)
        up.set(1)
        down = tk.IntVar(find_file)
        m_case = tk.IntVar(find_file)
        wrap_a = tk.IntVar(find_file)

        def actwrap():
            global wrap
            wrap = wrap_a.get()


        Label(find_file, text = 'Find what:').grid(row=1,column=1)
        w = tk.Entry(find_file, width=28,borderwidth = 1, highlightthickness=1, highlightcolor="#0078d7")
        w.grid(row=1,column=2, padx=20)

        def check(x):
            global direction
            global p
            global sw
            global sw2
            if(x==1):
                direction=2
                up.set(0)
                if(sw2==1):
                    sw2=0
                    p = p + len(w.get())
                if(p==-1):
                    p=0
            elif(x==3):
                down.set(0)
                direction = 1
                if (p == -1):
                    p = 0
            else:
                down.set(0)
                direction = 1
                if (p == -1):
                    p = 0
                if(not w.get() in textArea.get(str(currentline) + ".0", str(currentline) + "." + str(p))):
                    p = -1


            if(not up.get() and not down.get()):
                direction=1
                up.set(1)

        def cancel():
            find_file.destroy()
            global p
            global currentline
            global direction
            global sw
            global sw2
            global wrap
            direction = 1
            p = 0
            currentline = 1
            sw = 0
            sw2 = 0
            wrap = 0
            check(3)
            textArea.tag_delete("selectedtext", 1.0, END)

        b_find = tk.Button(find_file, text="Find next", width=7, bd=1, bg = '#e1e1e1',activebackground='#e5f1fb',  command=lambda: find_word(w.get()))
        b_find.grid(row=1,column=3, pady=5)
        Label(find_file, text='Direction').grid(row=2, column=2)
        b_cancel = tk.Button(find_file, text="Cancel", width=7, bd=1, bg='#e1e1e1', command=lambda:cancel())
        b_cancel.grid(row=2, column=3, pady=5)
        f = tk.Frame(find_file)
        f.grid(row=3, column=2, sticky="nsew")
        Checkbutton(f, text="Down", onvalue=1, offvalue=0 , variable=down, command=lambda: check(1)).pack(side=RIGHT, padx=20)
        Checkbutton(f, text="Up", onvalue=1, offvalue=0 , variable=up, command=lambda: check(2)).pack(side=RIGHT)
        Checkbutton(find_file, text='Match case', onvalue=1, offvalue=0, variable=m_case).grid(row=4,column=1, padx=5)
        Checkbutton(find_file, text='Wrap around', variable=wrap_a, command=lambda: actwrap()).grid(row=5,column=1, padx=5)


        find_file.mainloop()  # Mentine fereastra deschisa


    def paste():
        global textArea # Preluam textul global selectat
        textArea.event_generate("<<Paste>>") # Ne folosim de functia paste


    def viewhelp():
        webbrowser.open_new('https://www.bing.com/search?q=ob%c8%9bine%c8%9bi+ajutor+pentru+notepad+%c3%aen+windows+10&filters=guid:%224466414-ro-dia%22%20lang:%22ro%22&form=T00032&ocid=HelpPane-BingIA')

    def sendfeedback():
        webbrowser.open_new('https://www.microsoft.com/en-us/p/windows-notepad/9msmlrh6lzf3?activetab=pivot:overviewtab')

    def aboutnotepad():
        webbrowser.open_new('https://ro.wikipedia.org/wiki/Notepad')

        #webbrowser.open_new - deschide o noua fila in browser cu link-ul precizat

    def openFile():
        global textArea # Preluam textul global
        file = askopenfilename(defaultextension=".txt",
                                      filetypes=[("All Files", "*.*"),
                                                 ("Text Documents", "*.txt")]) # Functia pentru cautarea documentului text pe care vrei sa-l deschizi

        if file == "": # Verificam daca este selectat un document
            file = None # Daca nu e selectat atunci nu se intampla nimic
        else: # Daca este selectat atunci
            root.title(os.path.basename(file) + " - Notepad") # Schimbam titlul notpad-ului cu titlul documentului text ales
            # os.path.basename(file) - preluam doar numele documentului fara cale(path)
            textArea.delete(1.0, END) # Stergem textul global de la primul caracter pana la ultimul
            file = open(file, "r") # Deschidem documentul text in modul reading (citire)

            textArea.insert(1.0, file.read()) # Inseram in textul global textul din documnetul text pe care l-am deschis

            file.close() # Iesim din documentul text

    def saveFile(): # Definim functia save
        global file, textArea # Preluam textul si documentul global

        if file == None: # Verificam daca este selectat un document

            file = asksaveasfilename(initialfile='Untitled.txt',
                                            defaultextension=".txt",
                                            filetypes=[("All Files", "*.*"),
                                                       ("Text Documents", "*.txt")]) # Functia pentru salvarea documentului text

            if file == "": # Verificam daca este selectat un document
                file = None
            else:
                file = open(file, "w") # Deschidem documentul text in modul writing (citire)
                file.write(textArea.get(1.0, END)) # Scriem in el din textul global
                file.close() # Inchidem documentul
                root.title(os.path.basename(file) + " - Notepad") # Schimbam titlul notpad-ului cu titlul documentului text ales
                # os.path.basename(file) - preluam doar numele documentului fara cale(path)
        else:
            file = open(file, "w") # Deschidem documentul text in modul writing (citire)
            file.write(textArea.get(1.0, END))
            file.close()

    def newFile():
        global textArea  # Preluam textul global
        if len(textArea.get(1.0,END)) == 1: # Verificam daca lungimea textului global este 1 atunci nu este nimic scris in notepad si executam urmatoarele
            root.title("Untitled - Notepad")  # Schimbam titlul
            file = None  # Intializam documentul text cu nimic
            textArea.delete(1.0, END)  # Stergem textul global de la primul caracter pana la ultimul
        else: # Altfel este scris ceva in notepad si executam urmatoarele
            choise = msg.askyesnocancel("Notepad", "Do you want to save changes?", icon='warning') # Apelam functia si aplicam atribute / Afiseaza un text bar si intializeaza varibila choise cu alegerea ta

            if choise: # Daca alegerea ta este adevarata (Yes) atunci salvam documentul text
                saveFile() # Apelam functia save
            if choise == False: # Daca nu este adevarata (No) atunci executam urmatoarele
                root.title("Untitled - Notepad")  # Schimbam titlul
                textArea.delete(1.0, END)  # Stergem textul global de la primul caracter pana la ultimul


                # ------------------------------------- / ------------------------------------- #

    # -------------------------------------  Creearea interfatei ------------------------------------- #

    global textArea # Initializam o variabila pentru textul din notpad
    textArea = Text(root, bd=0, width=500, wrap=NONE) # Asociem textul ferestre-i
    textArea.config(yscrollcommand=scroll_bar_ver.set, xscrollcommand=scroll_bar_or.set)  # Setam scrollbar-ul pentru textul nostru din notepad atat vertical cat si orizontal
    textArea.pack(side=LEFT, fill=tk.Y) # Pozitionam textul in notepad pe partea stanga respectiv pe toata lungimea notepad-ului

    menuBar = Menu(root) # Creem bara de meniu
    root.config(menu=menuBar) # Configuram meniul

    fileMenu = Menu(menuBar, tearoff=0) # Initializam submeniul pentru file, tearoff - renunta la detasarea ferestrei de notpad
    fileMenu.add_command(label="New", command=newFile) # Adaugam in submeniu butonul new si asociem butonul cu functia newFile
    fileMenu.add_command(label="Open", command=openFile) # Adaugam in submeniu butonul open si asociem butonul cu functia openFile
    fileMenu.add_command(label="Save", command=saveFile) # Adaugam in submeniu butonul save si asociem butonul cu functia saveFile
    fileMenu.add_separator() # Separam printr-o line butonul exit de celelalte butoane
    fileMenu.add_command(label="Exit", command=exit) # Adaugam in submeniu butonul exit si asociem butonul cu functia exit

    editMenu = Menu(menuBar, tearoff=0)  # Initializam submeniul pentru edit, tearoff - renunta la detasarea ferestrei de notpad
    editMenu.add_command(label="Cut", command=cut)  # Adaugam in submeniu butonul cut si asociem butonul cu functia cut
    editMenu.add_command(label="Copy", command=copy)  # Adaugam in submeniu butonul copy si asociem butonul cu functia copy
    editMenu.add_command(label="Find", command=find)  # Adaugam in submeniu butonul find si asociem butonul cu functia find
    editMenu.add_command(label="Paste", command=paste)  # Adaugam in submeniu butonul paste si asociem butonul cu functia paste

    aboutMenu = Menu(menuBar,tearoff=0)  # Initializam submeniul pentru about, tearoff - renunta la detasarea ferestrei de notpad
    aboutMenu.add_command(label="View Help",command=viewhelp)  # Adaugam in submeniu butonul cut si asociem butonul cu functia
    aboutMenu.add_command(label="Send Feedback",command=sendfeedback)  # Adaugam in submeniu butonul cut si asociem butonul cu functia
    aboutMenu.add_separator() # Separam printr-o line butonul About Notepad de celelalte butoane
    aboutMenu.add_command(label="About Notpad", command=aboutnotepad)  # Adaugam in submeniu butonul cut si asociem butonul cu functia

    menuBar.add_cascade(label="File", menu=fileMenu) # Adugam in meniu butonul file si il asociem submeniului fileMenu
    menuBar.add_cascade(label="Edit", menu=editMenu)  # Adugam in meniu butonul edit si il asociem submeniului editMenu
    menuBar.add_cascade(label="Help", menu=aboutMenu)  # Adugam in meniu butonul help si il asociem submeniului aboutMenu


root = tk.Tk() # Creezi fereastra pentru notpad
root.title("Untitled - Notepad") # Afisezi fereastra cu titlul 'Untitled - Notepad'
root.geometry('630x430') # Setam rezolutia notepad-ului
root.iconbitmap('npi.ico') #Setam iconita de la notpad
scroll_bar_ver = tk.Scrollbar(root, orient=VERTICAL) # Creem scrollbar vertical
scroll_bar_ver.pack(side=RIGHT, fill=Y) # Asezam scrollbar-ul pe partea dreapta a notepad-ului si pe toata lungimea lui
scroll_bar_or = tk.Scrollbar(root, orient=HORIZONTAL) # Creem scrollbar orizontal
scroll_bar_or.pack(side=BOTTOM, fill=X) # Asezam scrollbar-ul si pe toata latimea notepad-ului
file = None # Initializam o variabila file pentru documentul text
createComponents() # Apelam functia
root.mainloop() # Mentine fereastra deschisa

                # ------------------------------------- / ------------------------------------- #
