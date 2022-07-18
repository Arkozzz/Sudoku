from encodings import utf_8
from tkinter import *
from GP1S2_solver import *
from PIL import Image,ImageTk
import time,os,sys,json


os.chdir(os.path.dirname(sys.argv[0]))

# collect language in config.txt
with open('config.txt') as f:
    contents = f.read()
    lang = contents[5:7]
    
#read the associate json
if lang == 'fr':
    data = open('lang_fr.json', encoding='utf_8')
    load = json.load(data)
else:
    data = open('lang_en.json', encoding='utf_8')
    load = json.load(data)


# Paramètre de la fenetre
fen = Tk()
fen.configure(bg="grey")
fen.attributes('-fullscreen', True)
fen.update()
larg = fen.winfo_width()
haut = fen.winfo_height()

logoimage=Image.open("Sudoko.jpg").resize((80,80))
logoimagetk = ImageTk.PhotoImage(logoimage)
profilimage=Image.open("profil.png").resize((100,100))
profilimagetk = ImageTk.PhotoImage(profilimage)

#Limiter le nombre de caractères d'une entrée
def validate( P ):
    if len(P) <= 1:
        return True
    else:
        return False

def validate2(P):
    if len(P) <= 11:
        return True
    else:
        return False

# Def qui permet de chronométrer
def sec2hms(ss):
    (hh, ss) = divmod(ss, 3600)
    (mm, ss) = divmod(ss, 60)
    return mm, ss

def grid(grille):
    List=[]
    state = ()
    
    if is_valid(grille)==False:
        state=True
    else:
        solve(grille,0)

    for i in range(9):
        for k in range(9):
            List.append(grille[i][k])
            
    for i in range(81):
        if List[i]==0:
            state=True
            break
        else :
            state=False
            if is_valid(grille)==False:
                state=True

    return List,state

# Def d'une liste qui nous sera utile

Liste_vierge=[]
for i in range(81):
    Liste_vierge.append("")

RTG_Solver=Liste_vierge.copy()

# Définition du menu d'accueil
def starting():
    for w in fen.winfo_children():
        w.destroy()
    close_button = Button(fen, text=load['quit'], bd=1, font=("Bahnschrift SemiBold", 12), command=fen.quit).place(x=0, y=0, width=60)
    title = Label(fen, text=load['enter.username'], bg="grey", font=("Bahnschrift SemiBold", 40)).place(x=larg / 2 - 350, y=35, width=700)
    vcmd = (fen.register(validate2), "%P")
    username_entry=Entry(fen,font=("Bahnschrift",20), justify="center", validate="key", validatecommand=vcmd)
    username_entry.place(x=larg/2-125,y=haut/3, width=200)
    profilimagetk2 = Label(fen, image=profilimagetk).place(x=larg/2-275, y=haut/3-30)

    def username_d():
        global username_var,username
        username_var=username_entry.get()
        if username_var=="":
            message=Label(fen,text=load['invalid.username'],font=("Bahnschrift SemiBold",17), fg="red", bg="grey").place(x=larg/2-160,y=haut/2-50,width=275)
        else:
            username=username_var
            menu()

    valid=Button(fen,text=load['valid'], bd=0,font=("Bahnschrift SemiBold", 16), command=username_d, foreground='limegreen')
    valid.place(x=larg/2+110,y=haut/3,width=70)

    #la touche <Entrée> permet de valider un button par défaut
    def EnterKey(event):
        username_d()
    fen.bind('<Return>',EnterKey)


# Définition du menu principal
def menu():

    for w in fen.winfo_children():
        w.destroy()
    close_button = Button(fen, text=load['quit'], bd=1, font=("Bahnschrift SemiBold", 12), command=fen.quit).place(x=0, y=0, width=60)
    restart_button = Button(fen, text=load['restart'], bd=1, font=("Bahnschrift SemiBold", 12), command=starting).place(x=60, y=0, width=100)
    title = Label(fen, text=load['principal.menu'], bg="grey", font=("Bahnschrift SemiBold", 50)).place(x=larg/2-250,y=35,width=500)
    message=Label(fen,text=load['hi.username']%username_var, bg="grey", fg='black', font=("Bahnschrift", 20)).place(x=larg/2-300,y=haut/3-20,width=600) 
    solver_button = Button(fen, text=load['solver'], bd=0, font=("Bahnschrift SemiBold", 20),command=solver_1).place(x=larg/2-60, y=haut/2-30, width=120)
    game_button = Button(fen, text=load['play'], bd=0, font=("Bahnschrift SemiBold", 20),command=game_1).place(x=larg/2-60, y=haut/2+40, width=120)
    options_button = Button(fen, text="Options", bd=0, font=("Bahnschrift SemiBold", 20),command=options_page).place(x=larg/2-60, y=haut/2+110, width=120)
    logoimagetk2 = Label(fen, image=logoimagetk).place(x=larg-120, y=20)

#menu aide
def options_page():
    for w in fen.winfo_children():
        w.destroy()
    menu_button= Button(fen, text=load['menu'], bd=1, font=("Bahnschrift SemiBold", 12), command=menu).place(x=60, y=0, width=60)
    close_button = Button(fen, text=load['quit'], bd=1, font=("Bahnschrift SemiBold", 12), command=fen.quit).place(x=0, y=0, width=60)
    Options = Label(fen, text="Options:", bg="grey", font=("Bahnschrift SemiBold", 50)).place(x=larg/2-130, y=30, width=250)
    Tuto = Label(fen, text=load['tuto'], bg="grey", font=("Bahnschrift", 15)).place(x=larg/2-200, y=400, width=400)
    LinkYT = Label(fen, text="https://www.youtube.com/watch?v=tutorialSudoku", bg='grey', fg="royalblue", font=("Bahnschrift", 13, 'italic', 'underline')).place(x=larg/2-200, y=440, width=400)
    Version = Label(fen, text="• Version 1.0.1 (Windows ~ 32/64 bits)", bg="grey", font=("Bahnschrift", 15)).place(x=larg/2-200, y=600, width=400)
    lang = Label(fen, text=load['change.language'], bg="grey", font=("Bahnschrift", 15)).place(x=larg/2-200, y=500, width=400)
    langLink = Label(fen, text="./Sudoku/config.txt", bg="grey", fg='darkgoldenrod', font=("Bahnschrift", 13)).place(x=larg/2-200, y=540, width=400)
 
# Definition du menu solver
def solver_1():
    for w in fen.winfo_children():
        w.destroy()
    close_button = Button(fen, text=load['quit'], bd=1, font=("Bahnschrift SemiBold", 12), command=fen.quit).place(x=0, y=0, width=60)
    title= Label(fen, text=load['solver'], bg="grey", font=("Bahnschrift SemiBold", 50)).place(x=larg/2-150, y=30, width=300)
    menu_button= Button(fen, text=load['menu'], bd=1, font=("Bahnschrift SemiBold", 12), command=menu).place(x=60, y=0, width=60)
    grid_1=Canvas(fen, bd=0, width=360, height=360, bg="white")
    grid_1.place(x=larg/2-180,y=haut/2-160)

    for i in range(0, 4):
        grid_1.create_line(0, 3+i*119, 363, 3+i*119, fill="black", width=3)
        grid_1.create_line(3+i*119, 0, 3+i*119, 363, fill="black", width=3)
        for k in range(1, 3):
            grid_1.create_line(0, 120*i+1+40*k, 360, 120*i+1+40*k, fill="black", width=1)
            grid_1.create_line(120*i+1+40*k, 0, 120*i+1+40*k, 360, fill="black", width=1)

    L_name = []
    for i in range(0, 9):
        for u in range(0, 9):
            L_name.append("C%d" % (u+i*9+1))
            vcmd=(fen.register(validate),"%P")
            L_name[u + i * 9]=Entry(fen,bd=0, font=("Bahnschrift SemiBold", 14), justify="center", validate="key",validatecommand=vcmd)
            L_name[u + i * 9].insert(0, RTG_Solver[u+i*9])
            L_name[u+i*9].place(x=larg/2-174+40*u, y=haut/2-154+i*40, width=32, height=32)


    # Récupération des valeurs qui sont stocké ci-dessus
    def recup():
        state=True
        List = []
        List_4=[]
        nombre = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        List_5=[]
        for i in range(81):
            k = L_name[i].get()
            List_4.append(k)
            List_5.append(0)
            if k in nombre:
                k = int(k)
                List.append(k)
            elif k == "":
                List.append(0)
            else:
                List.append(0)
                state=False

        if List_5==List:
            state = False

        List_2 = []
        for i in range(9):
            List_3 = []
            for k in range(9):
                List_3.append(List[k + i * 9])
            List_2.append(List_3)
        solver_1_1(List_2,List_4,state)

    select_button = Button(fen, text=load["solver"], bd=0, font=("Bahnschrift SemiBold", 13), command=recup).place(x=larg/2-40, y=haut/2+220, width=80)
    def EnterKey(event):
        recup()
    fen.bind('<Return>',EnterKey)
# Definition du menu solver 1.1
def solver_1_1(grille,List_2,state_2):
    for w in fen.winfo_children():
        w.destroy()
    close_button = Button(fen, text=load['quit'], bd=1, font=("Bahnschrift SemiBold", 12), command=fen.quit).place(x=0, y=0, width=60)
    title = Label(fen, text=load['solver'], bg="grey", font=("Bahnschrift SemiBold", 50)).place(x=larg/2-150, y=30, width=300)
    menu_button= Button(fen, text=load['menu'], bd=1, font=("Bahnschrift SemiBold", 12), command=menu).place(x=60, y=0, width=60)
    new_button= Button(fen, text=load['new'], bd=1, font=("Bahnschrift SemiBold", 12), command=solver_1).place(x=120, y=0, width=78)
    grid_2 = Canvas(fen, bd=0, width=360, height=360, bg="white")
    grid_2.place(x=larg/4-180, y=haut/2-160)

    for i in range(0, 4):
        grid_2.create_line(0, 3+i*119, 363,3+i*119, fill="black", width=3)
        grid_2.create_line(3+i*119, 0, 3+i*119, 363, fill="black", width=3)

        for k in range(1,3):
            grid_2.create_line(0, 120*i+1+40*k, 360, 120*i+1+40*k, fill="black", width=1)
            grid_2.create_line(120*i+1+40*k, 0, 120*i+1+40*k, 360, fill="black", width=1)

    List_1=[]
    if state_2==False:
        state=True
    else:
        List_1, state = grid(grille)

    for i in range(0, 9):
        for u in range(0, 9):
            List_2.append(grille[i][u])
            answers = Label(fen, text=List_2[u + i * 9], bg="white", font=("Bahnschrift SemiBold", 14)).place(x= larg/4-166+40*u, y=haut/2-153+i*40)

    if state==True:
        state_lab = Label(fen, text=load['not.solvable'], bg="grey", fg="red", font=("Bahnschrift SemiBold", 25)).place(x=3*larg/4-200, y=haut/2-50, width=400)
    else:
        grid_3 = Canvas(fen, bd=0, width=360, height=360, bg="white")
        grid_3.place(x=3 * larg/4-180, y=haut/2-160)
        for i in range(0, 4):
            grid_3.create_line(0, 3 + i * 119, 363, 3 + i * 119, fill="black", width=3)
            grid_3.create_line(3 + i * 119, 0, 3 + i * 119, 363, fill="black", width=3)

            for k in range(1, 3):
                grid_3.create_line(0, 120 * i + 1 + 40 * k, 360, 120 * i + 1 + 40 * k, fill="black", width=1)
                grid_3.create_line(120 * i + 1 + 40 * k, 0, 120 * i + 1 + 40 * k, 360, fill="black", width=1)

        for i in range(0, 9):
            for u in range(0, 9):
                answers = Label(fen, text=List_1[u+i*9], bg="white", font=("Bahnschrift SemiBold", 14)).place(x=3*larg/4-166+40*u, y=haut/2-153+i*40)

    global RTG_Solver
    RTG_Solver=Liste_vierge.copy()

    def BTG():
        global RTG_Solver
        RTG_Solver=List_2.copy()
        solver_1()
    select_button = Button(fen, text=load['back.grid'], bd=0, font=("Bahnschrift SemiBold", 13), command=BTG).place(x=larg/4-80, y=haut/2+220, width=160)


level=0

RTG_Play = Liste_vierge.copy()
RTG_GR = Liste_vierge.copy()

def game_1():
    for w in fen.winfo_children():
        w.destroy()
    menu_button= Button(fen, text=load['menu'], bd=1, font=("Bahnschrift SemiBold", 12), command=menu).place(x=60, y=0, width=60)
    close_button = Button(fen, text=load['quit'], bd=1, font=("Bahnschrift SemiBold", 12), command=fen.quit).place(x=0, y=0, width=60)
    title = Label(fen, text=load['solver'], bg="grey", font=("Bahnschrift SemiBold", 50)).place(x=larg/2-150, y=30, width=300)

    global RTG_GR, RTG_Play
    RTG_Play = Liste_vierge.copy()
    RTG_GR = Liste_vierge.copy()

    #Change la couleur du bouton dès lors qu'il est séléctionné
    def choose_your_level(level_chose,color):
        global level
        if color == 1:
            level_easy_button.config(bg='chartreuse'), level_medium_button.config(bg='white'), level_hard_button.config(bg='white')
        if color == 2:
            level_easy_button.config(bg='white'), level_medium_button.config(bg='goldenrod'), level_hard_button.config(bg='white')
        if color == 3:
            level_easy_button.config(bg='white'), level_medium_button.config(bg='white'), level_hard_button.config(bg='brown')
        level=level_chose

        def launch():
            global start
            game_2()
            start = time.time()
        valid_button = Button(fen, text=load['play'], bd=0, font=("Bahnschrift SemiBold", 20), command=launch).place(x=larg / 2 - 50, y=haut / 2 + 150, width=100)

    level_easy_button = Button(fen, text=load["level.easy"], bd=0, font=("Bahnschrift SemiBold", 20),command=lambda:choose_your_level(0.97,1))
    level_easy_button.place(x=larg/2-275, y=haut/2-50, width=150)
    level_medium_button = Button(fen, text=load["level.medium"], bd=0, font=("Bahnschrift SemiBold", 20), command=lambda:choose_your_level(0.55,2))
    level_medium_button.place(x=larg/2-75, y=haut/2-50, width=150)
    level_hard_button = Button(fen, text=load["level.hard"], bd=0, font=("Bahnschrift SemiBold", 20), command=lambda:choose_your_level(0.45,3))
    level_hard_button.place(x=larg/2+125, y=haut/2-50, width=150)



def game_2():
    for w in fen.winfo_children():
        w.destroy()
        
    close_button = Button(fen, text=load['quit'], bd=1, font=("Bahnschrift SemiBold", 12), command=fen.quit).place(x=0, y=0, width=60)
    menu_button= Button(fen, text=load['menu'], bd=1, font=("Bahnschrift SemiBold", 12), command=menu).place(x=60, y=0, width=60)
    level_button = Button(fen, text=load['levels'], bd=1, font=("Bahnschrift SemiBold", 12), command=game_1).place(x=120, y=0, width=70)
    title = Label(fen, text=load['solver'], bg="grey", font=("Bahnschrift SemiBold", 50)).place(x=larg/2-150, y=30, width=300)

    grid_2 = Canvas(fen, bd=0, width=360, height=360, bg="white")
    grid_2.place(x=larg/2-180, y=haut/2-160)

    for i in range(0, 4):
        grid_2.create_line(0, 3+i*119, 363,3+i*119, fill="black", width=3)
        grid_2.create_line(3+i*119, 0, 3+i*119, 363, fill="black", width=3)

        for k in range(1,3):
            grid_2.create_line(0, 120*i+1+40*k, 360, 120*i+1+40*k, fill="black", width=1)
            grid_2.create_line(120*i+1+40*k, 0, 120*i+1+40*k, 360, fill="black", width=1)

    global level, RTG_GR, RTG_Play
    List=[]

    if RTG_Play == Liste_vierge:
        grille = randomgrid(level)
        RTG_GR.clear()
        for i in range(0, 9):
            for u in range(0, 9):
                List.append(grille[i][u])
                RTG_GR.append(grille[i][u])

    else:
        List = RTG_Play.copy()

    L_nombre_1=[1,2,3,4,5,6,7,8,9]
    L_nombre_2 = ['1','2','3','4','5','6','7','8','9']
    L_name = []
    for i in range(81):
        if List[i] in L_nombre_2:
            a=int(List[i])
            if a==RTG_GR[i]:
                List[i]=a

    for i in range(0, 9):
        for u in range(0, 9):
            L_name.append("C%d"%(u+i*9+1))

            if List[u + i * 9] == 0:
                List[u + i * 9] = ""

            if List[u+i*9] != "":
                L_name[u+i*9] = Entry(fen)

                if List[u+i*9] in L_nombre_1:
                    L_name[u+i*9].insert(0, int(List[u+i*9]))
                    L_name[u+i*9].configure(state=DISABLED, disabledbackground='white', bd=0, disabledforeground='red', font=("Bahnschrift SemiBold", 14), justify="center")
                else:
                    L_name[u+i*9].insert(0, List[u+i*9])
                    L_name[u+i*9].configure(background='white', bd=0, foreground='black', font=("Bahnschrift SemiBold", 14), justify="center")

                L_name[u+i*9].place(x=larg/2-174+40*u, y=haut/2-154+i*40, width=32, height=32)

            else:
                vcmd = (fen.register(validate), "%P")
                L_name[u+i*9] = Entry(fen, bd=0, font=("Bahnschrift SemiBold", 14), justify="center", validate="key",validatecommand=vcmd)
                L_name[u+i*9].place(x=larg/2-174+40*u, y=haut/2-154+i*40, width=32, height=32)

    def save_val():
        global stop
        stop=time.time()
        state=True
        List = []
        List_4=[]
        nombre = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

        for i in range(81):
            k = L_name[i].get()
            List_4.append(k)
            if k in nombre:
                k = int(k)
                List.append(k)
            elif k == "":
                List.append(0)
            else:
                List.append(0)
                state=False

        List_2 = []
        for i in range(9):
            List_3 = []
            for k in range(9):
                List_3.append(List[k + i * 9])
            List_2.append(List_3)
        game_2_1(List_2,List_4,state)

    check_button = Button(fen, text=load['check'], bd=0, font=("Bahnschrift SemiBold", 13), command=save_val).place(x=larg/2-40, y=haut/2+220, width=80)


def game_2_1(List_1,List_2,state):
    for w in fen.winfo_children():
        w.destroy()
    close_button = Button(fen, text=load['quit'], bd=1, font=("Bahnschrift SemiBold", 12), command=fen.quit).place(x=0, y=0, width=60)
    menu_button= Button(fen, text=load['menu'], bd=1, font=("Bahnschrift SemiBold", 12), command=menu).place(x=60, y=0, width=60)
    title = Label(fen, text=load['solver'], bg="grey", font=("Bahnschrift SemiBold", 50)).place(x=larg/2-150, y=30, width=300)
    grid_2 = Canvas(fen, bd=0, width=360, height=360, bg="white")
    grid_2.place(x=larg / 4 - 180, y=haut / 2 - 160)

    for i in range(0, 4):
        grid_2.create_line(0, 3 + i * 119, 363, 3 + i * 119, fill="black", width=3)
        grid_2.create_line(3 + i * 119, 0, 3 + i * 119, 363, fill="black", width=3)

        for k in range(1, 3):
            grid_2.create_line(0, 120 * i + 1 + 40 * k, 360, 120 * i + 1 + 40 * k, fill="black", width=1)
            grid_2.create_line(120 * i + 1 + 40 * k, 0, 120 * i + 1 + 40 * k, 360, fill="black", width=1)


    nombre = [1,2,3,4,5,6,7,8,9]
    if state==False:
        state=False
    else :
        for i in range(9):
            for k in range(9):
                if List_1[i][k] in nombre:
                    continue
                else:
                    state=False
                    break
        if state == False:
            state = False
        else:
            state = is_valid(List_1)
    mm,ss = sec2hms(int(stop-start))
    if state == True:
        state_lab = Label(fen, text=load['congrats']%(username, mm, ss), bg="grey", fg="chartreuse", font=("Bahnschrift SemiBold", 19)).place(x=3*larg/4-250, y=haut/2-50, width=500)
        play_again_button = Button(fen, text=load['play.again'], bd=1, font=("Bahnschrift SemiBold", 12), command=game_1).place(x=3*larg/4-50, y=haut/2+50, width=100)
        for i in range(0, 9):
            for u in range(0, 9):
                answers = Label(fen, text=List_2[u + i * 9], bg="white",fg="chartreuse", font=("Bahnschrift SemiBold", 14)).place(
                    x=larg / 4 - 166 + 40 * u, y=haut / 2 - 153 + i * 40)
    else:
        state_lab = Label(fen, text=load['incorrect.grid']%(username,mm,ss), bg="grey", fg="red", font=("Bahnschrift SemiBold", 19)).place(x=3*larg/4-250, y=haut/2-50, width=500)
        play_again_button = Button(fen, text=load['play.again'], bd=1, font=("Bahnschrift SemiBold", 12), command=game_1).place(x=3*larg/4-150, y=haut/2+50, width=100) #laisser 19
        for i in range(0, 9):
            for u in range(0, 9):
                answers = Label(fen, text=List_2[u + i * 9], bg="white", font=("Bahnschrift SemiBold", 14)).place(x=larg/4-166+40*u, y=haut/2-153+i*40)

        global RTG_Play
        RTG_Play = Liste_vierge

        def BTG():
            global RTG_Play
            RTG_Play = List_2
            game_2()
        level_but = Button(fen, text=load['back.grid'], bd=1, font=("Bahnschrift SemiBold", 12),command=BTG).place(x=3*larg/4, y=haut/2+50, width=150)


starting()
fen.mainloop()