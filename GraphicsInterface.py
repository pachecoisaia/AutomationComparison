from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from Comparison import *
from datetime import datetime
import pause,os

class GraphicsInterface:
    # GUI Events, Commands, Widgets, etc. go here
    def __init__(self):
        self.window = Tk()
        self.window.geometry("750x500")
        self.dictionaryA = {} #empty dictionary
        self.filenameA = ""
        self.filenameB = ""
        self.clickedHour = IntVar()
        self.clickedHour.set(17)
        self.clickedMinute = IntVar()
        self.clickedMinute.set(0)
        self.clickedSecond = IntVar()
        self.clickedSecond.set(0)
        self.clickedMonth = IntVar()
        self.clickedMonth.set(11)
        self.clickedDay = IntVar()
        self.clickedDay.set(24)
        self.clickedYear = IntVar()
        self.clickedYear.set(2021)
        self.filenameDefault = StringVar()
        self.filenameDefault.set("MOST_RECENT_VOICEMAILS_OF_HOUSEHOLDIDS.csv")
        intructionsStr = StringVar()
        intructionsStr.set("ENTER DATE AND TIME TO RUN AUTOMATION")
        hourStr = StringVar()
        hourStr.set("HH:")
        minuteStr = StringVar()
        minuteStr.set("MM:")
        secondStr = StringVar()
        secondStr.set("SS:")
        monthStr = StringVar()
        monthStr.set("MM/")
        dayStr = StringVar()
        dayStr.set("DD/")
        yearStr = StringVar()
        yearStr.set("YY/")
        intructions_b_Str = StringVar()
        intructions_b_Str.set("ENTER THE FILE NAME YOU WISH TO SAVE OUTPUT FILE AS")
        offset = 250
        hourOptions = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
        monthOptions = [0,1,2,3,4,5,6,7,8,9,10,11,12]
        dayOptions = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]
        yearOptions = [2021,2022,2023,2024,2025,2026,2027,2028,2029]
        minutesecondsOptions = [ 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,
                                 32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59 ]

        # create buttons
        btnFileSelectA = Button(master=self.window, text="SELECT FILE A (InputFile)")
        btnFileSelectB = Button(master=self.window, text="SELECT FILE B (ComparisonFile)")
        btnRunAutomation = Button(master=self.window, text="RUN AUTOMATION")


        # bind left click events to specified event handlers for each button
        btnFileSelectA.bind('<Button-1>', self.OnFileSelectA_Click)
        btnFileSelectB.bind('<Button-1>', self.OnFileSelectB_Click)
        btnRunAutomation.bind('<Button-1>', self.OnRunAutomation_Click)

        #Create Dropdown
        dropdownHour = OptionMenu(self.window,self.clickedHour,*hourOptions)
        dropdownMinute = OptionMenu(self.window, self.clickedMinute, *minutesecondsOptions)
        dropdownSecond = OptionMenu(self.window, self.clickedSecond, *minutesecondsOptions)
        dropdownMonth = OptionMenu(self.window, self.clickedMonth, *monthOptions)
        dropdownDay = OptionMenu(self.window,self.clickedDay, *dayOptions)
        dropdownYear = OptionMenu(self.window,self.clickedYear, *yearOptions)


        #create widgets
        intructionsLabel = Label(self.window, textvariable=intructionsStr)
        hourLabel = Label(self.window, textvariable=hourStr)
        minuteLabel = Label(self.window, textvariable=minuteStr)
        secondLabel = Label(self.window, textvariable=secondStr)
        monthLabel = Label(self.window, textvariable=monthStr)
        dayLabel = Label(self.window, textvariable=dayStr)
        yearLabel = Label(self.window, textvariable=yearStr)
        intructions_b_Label = Label(self.window, textvariable=intructions_b_Str)
        filenameInput = Entry(self.window, text=self.filenameDefault, width= 53)


        # display and position widgets
        intructionsLabel.place(x=offset, y=35)
        btnFileSelectA.place(x = 125, y=130)
        btnFileSelectB.place(x = 475, y=130)
        hourLabel.place(x = 0 + offset, y=65)
        dropdownHour.place(x = 30 + offset, y=60)
        minuteLabel.place(x = 90 + offset, y=65)
        dropdownMinute.place(x = 120+ offset, y=60)
        secondLabel.place(x=180+ offset, y=65)
        dropdownSecond.place(x = 210+ offset, y=60)
        monthLabel.place(x=0+ offset, y=95)
        dropdownMonth.place(x = 30+ offset, y=90)
        dayLabel.place(x=90+ offset, y=95)
        dropdownDay.place(x = 120+ offset, y=90)
        yearLabel.place(x=180+ offset, y=95)
        dropdownYear.place(x = 210+ offset, y=90)
        btnRunAutomation.place(x = offset + 95, y=230)
        intructions_b_Label.place(x=offset, y=170)
        filenameInput.place(x = offset, y=200)

        self.window.mainloop()

    def OnFileSelectA_Click(self, event):
        print("OnFileSelectA Click")
        # code openFileDialog
        file = fd.askopenfile(initialdir=os.getcwd(), title="Select CSV file", filetypes=[("CSV Files", "*.csv")],
                               mode='r')
        self.filenameA = file.name
        self.fileA = file


    def OnFileSelectB_Click(self, event):
        print("OnFileSelectB Click")
        # code openFileDialog
        file = fd.askopenfile(initialdir=os.getcwd(), title="Select CSV file", filetypes=[("CSV Files", "*.csv")],
                               mode='r')
        self.filenameB = file.name
        self.fileB = file


    def OnRunAutomation_Click(self, event):
        print("Run Automation Clicked")
        mb.showinfo("Notification", "Automation Scheduled! DO NOT CLOSE!")
        pause.until(datetime(self.clickedYear.get(), self.clickedMonth.get(), self.clickedDay.get(),
                             self.clickedHour.get(), self.clickedMinute.get(), self.clickedSecond.get()))
        self.dictionaryA = csv_toDictionary(self.filenameA)
        createSuccessfulVoicemailFile(self.filenameB, self.dictionaryA, self.filenameDefault.get())
        createDisconnectedOutputFile(self.filenameB)
        self.fileA.close()
        self.fileB.close()
        mb.showinfo("Notification", "Tasks Completed!")
