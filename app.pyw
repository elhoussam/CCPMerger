import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import tkinter.font as tkFont
from pathlib import Path
from datetime import datetime
import os
import time

class App:
    def __init__(self, root):
        #setting title
        root.title("CCP Virement File")
        #setting window size
        width=285
        height=240
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)
        setattr( self , "win", root )        
        # label and entry for  CCP NUMBER
        lblCCP = tk.Label(root, text="COMPTE CCP")
        lblCCP["font"] = tkFont.Font(family='Times Bold',size=10)
        lblCCP.place(x=20,y=35)
        
        eCCP =tk.Entry(root)
        ft = tkFont.Font(family='Times',size=15)
        eCCP["font"] = ft
        eCCP["fg"] = "#333333"
        eCCP["justify"] = "center"
        eCCP.place(x=130,y=30,width=138,height=30)
        eCCP.insert(0, '21001561')
        setattr( self , "compte", eCCP )
        # label and entry for  CCP KEY NUMBER
        
        lblCLE = tk.Label(root, text="CLE CCP")
        lblCLE["font"] = tkFont.Font(family='Times Bold',size=10)
        lblCLE.place(x=20,y=75)
        
        eCLE =tk.Entry(root)
        ft = tkFont.Font(family='Times',size=15)
        eCLE["font"] = ft
        eCLE["fg"] = "#333333"
        eCLE["justify"] = "center"
        eCLE.place(x=130,y=70,width=138,height=30)
        eCLE.insert(0, '30')
        setattr( self , "cle", eCLE )
        # label and entry foR OUTPUT NAME FILE
        
        lblFILE = tk.Label(root, text="NOM FICHIER")
        lblFILE["font"] = tkFont.Font(family='Times Bold',size=10)
        lblFILE.place(x=20,y=115)
        
        eFile =tk.Entry(root)
        ft = tkFont.Font(family='Times',size=15)
        eFile["font"] = ft
        eFile["fg"] = "#333333"
        eFile["justify"] = "center"
        eFile.insert(0, 'DEPO')
        eFile.place(x=130,y=110,width=138,height=30)

        setattr( self , "eFile", eFile )

        lblDate = tk.Label(root, text="DATE")
        lblDate["font"] = tkFont.Font(family='Times Bold',size=10)
        lblDate.place(x=20,y=150)
        
        eMonth =tk.Entry(root)
        ft = tkFont.Font(family='Times',size=15)
        eMonth["font"] = ft
        eMonth["fg"] = "#333333"
        eMonth["justify"] = "center"
        eMonth.insert(0, str( datetime.now().month ) )
        eMonth.place(x=130,y=150,width=50,height=30)
        setattr( self , "Month", eMonth )
        
        eYear =tk.Entry(root)
        ft = tkFont.Font(family='Times',size=15)
        eYear["font"] = ft
        eYear["fg"] = "#333333"
        eYear["justify"] = "center"
        eYear.insert(0, str( datetime.now().year ) )
        eYear.place(x=190,y=150,width=80,height=30)
        setattr( self , "Year", eYear )
       
        # Button to run the merge
        
        GButton_331=tk.Button(root)
        GButton_331["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_331["font"] = ft
        GButton_331["fg"] = "#000000"
        GButton_331["justify"] = "center"
        GButton_331["text"] = "GENERE"
        GButton_331.place(x=200,y=185,width=73,height=30)
        GButton_331["command"] = self.GButton_331_command
        # progress bar 
        pgbar = ttk.Progressbar(root, length = 100, maximum = 100, value = 0, mode = 'determinate', ) 
        pgbar.place(x=20,y=186,width=175,height=29)
        setattr( self , "status", pgbar )         
        # status de traitement        
        lblTraitement = tk.Label(root, text=" ",justify='left')
        lblTraitement["font"] = tkFont.Font(family='Times Bold',size=8)
        lblTraitement.place(x=0,y=220,width=280,height=20)
        setattr( self , "statusbar", lblTraitement )        
    def GButton_331_command(self):
        # check if field are met the conditions
        if( self.fieldChecker("compte", self.compte.get() ) and self.fieldChecker("Mois", self.Month.get() ) and self.fieldChecker("Anneé", self.Year.get() )  and self.fieldChecker("cle", self.cle.get() ) and self.fieldChecker("nom de fichier", self.eFile.get() )  ):
            totalAmount = 0.0
            nombreEmp = 0
            OutputFileName = "F_"+self.eFile.get()+"_"+"".join(str(time.time()).split("."))+".txt"
            # print( self.compte.get() + self.cle.get() +  OutputFileName )
            self.status["value"] = 0
            files = os.listdir(os.curdir)  #files and directories
            fOutput = open(OutputFileName, "a")
            for el in files :
               filename, file_extension = os.path.splitext(el.strip())
               if file_extension=="" and os.path.isfile( el.strip() ) : # and os.path.isfile( el.strip() )
                    # my comment #self.statusbar["text"] = "Traitement : " + el.strip()
                    a,b = self.copyInto(el, fOutput)
                    totalAmount =  totalAmount + b
                    nombreEmp =  nombreEmp + a                 
                    #print(el)
            print(str(OutputFileName.split(".")[0]).ljust(20)+ " " + str(nombreEmp).ljust(4) +" " + str(round(totalAmount,2)).ljust(15) ) 
            self.statusbar["text"] = OutputFileName+ " " + str(nombreEmp) +" " + str(round(totalAmount,2) )
            fOutput.close()
            self.insertHeader(OutputFileName,str(round(totalAmount,2)),str(nombreEmp))  
            self.status["value"] = 100
            self.win.update_idletasks()
    def specialSplits(self, c ):
        # specialSplits: that extract information from the line of str
        myList = []
        myList.append( c[34:61].strip() ) 
        myList.append( c[9:19] ) 
        myList.append( c[19:21] ) 
        myList.append( ( float (c[21:34])/100) ) 
        return myList
    def fillTheGapWith(occ):
        # fillTheGapWith : fill the gap with Zeros
        local = ""
        for i in range(0,occ):
            local = local + "0"
        return local
    def prepend_line(file_name, line):
        """ Insert given string as a new line at the beginning of a file """
        # define name of temporary dummy file
        dummy_file = file_name + '.bak'
        # open original file in read mode and dummy file in write mode
        with open(file_name, 'r') as read_obj, open(dummy_file, 'w') as write_obj:
            # Write given line to the dummy file
            write_obj.write(line + '\n')
            # Read lines from original file one by one and append them to the dummy file
            for line in read_obj:
                write_obj.write(line)
        # remove original file
        os.remove(file_name)
        # Rename dummy file as the original file
        os.rename(dummy_file, file_name)
    def insertHeader(self, file, amount, nbr):
        Ccp = self.compte.get()
        Ccp = App.fillTheGapWith((10 - len(Ccp))) + str(Ccp)
        # print( Ccp ) 
        Cle = self.cle.get()
        Cle = App.fillTheGapWith(2 - len(Cle)) + str(Cle)
        # print( Cle ) 
        amount = "".join( str(amount).split(".") )
        amount = App.fillTheGapWith(13 - len(amount)) + amount
        nbr = str( nbr )
        nbr= App.fillTheGapWith(7 - len(nbr)) + nbr
        MM = self.Month.get()
        MM = App.fillTheGapWith(2 - len(MM)) + MM
        YY = self.Year.get()
        print("*00000000"+  Ccp+ Cle +  amount + nbr+ MM + YY + "              "+ "0" )
        App.prepend_line(file, "*00000000"+  Ccp+ Cle +  amount + nbr+ MM + YY + "              "+ "0")  
    def fieldChecker(self, fieldName, fieldtext ):
        # to disable this app
        # return True
        if len( fieldtext.strip() ) == 0 :
            messagebox.showerror(title="champ "+fieldName +" vide", message="vous devez remplir le champ "+fieldName)
            return False
        if fieldName != "nom de fichier" and not fieldtext.strip().isnumeric()  :
            messagebox.showerror(title="champ "+fieldName +" incorrect", message="vous devez corriger cela pour continuer. ")
            return False
        elif fieldName == "compte" and len( fieldtext.strip() ) > 10 :
            messagebox.showerror(title="champ "+fieldName +" incorrect", message="vous devez corriger cela pour continuer 10")
            return False
        elif fieldName == "cle" and len( fieldtext.strip() ) > 2 :
            messagebox.showerror(title="champ "+fieldName +" incorrect", message="vous devez corriger cela pour continuer 02")
            return False
        elif fieldName == "Mois" and ( int( fieldtext.strip() ) <= 0 or int( fieldtext.strip() ) > 12 )   :
            messagebox.showerror(title="champ "+fieldName +" incorrect", message="vous devez corriger cela pour continuer #AEDAED")
            return False        
        elif fieldName == "Anneé" and ( int( fieldtext.strip() ) < 2020 )   :
            messagebox.showerror(title="champ "+fieldName +" incorrect", message="vous devez corriger cela pour continuer #05478")
            return False
        return True
    def copyInto(self, fromFile, intoFile):
        # read text
        fInput = open(fromFile)
        line = fInput.readlines()
        # if ( Path(intoFile.name).stat().st_size != 0 ) :
        # intoFile.write("\n")   
        strock = ""
        endrofin = 0
        if [char for char in (str(datetime.now().year))][2:4] == ['2','0'] :
            strock = "*"
            endrofin = 1
        #print ( "my policy" + str( strock ) + " "+ str( endrofin ) )
        nbr = 0 
        amount = 0.0
        for e in line :
            if e.strip().startswith(str(strock)+"00000000") and e.strip().endswith( str(endrofin) ) and  len( e.strip() )==62 :
                self.statusbar["text"] = str(self.specialSplits(e.strip())[0]) + " " + str(self.specialSplits(e.strip())[3])
                self.status["value"] = self.status["value"] + 0.1
                self.win.update_idletasks() 
                time.sleep(1/1000) 
                amount = amount + self.specialSplits(e.strip())[3]
                nbr = nbr + 1
                intoFile.write(  e.strip()+"\n" )
                #print(  str(round(amount,2)) + " vs " + str(amount)[0:11]  )
        #print( " number : "+str(nbr) + " totol amount : "+ str(round(amount,2))  +"\t" + str(  fromFile ))
        print( str(  fromFile ).ljust(20)+" " + str(nbr).ljust(4)+" " +str(round(amount,2)).ljust(15)  )
        self.statusbar["text"] = str(  fromFile )+ str( round(amount,2) ) + " " + str(nbr)
        fInput.close()
        return nbr, amount 
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()