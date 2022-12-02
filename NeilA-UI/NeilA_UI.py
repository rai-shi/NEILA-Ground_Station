
from tkinter import *
# saat için
import time 
# graph için
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
# resimler için
from PIL import ImageTk, Image 
# battery
import psutil 
# yeni özellikleri için
from tkinter import ttk 
from tkinter import messagebox

from tkinter.font import Font

# kamera görüntüsü
import cv2 
# map
import tkintermapview 

import numpy as np
import math

import os
import csv 
import serial
import ftplib
import threading
from tkinter import filedialog


global stopFlag
stopFlag = False

global datas
datas = []


root = Tk()

root.title("KTU UZAY NEILA")
root.state('zoomed')
root.configure(bg="#0059aa")
plt.style.use('bmh')

font = Font(family = "Helvetica", size = 12)
root.option_add("*TCombobox*Listbox*Font", font)

#iconbitmap
root.iconphoto(True, ImageTk.PhotoImage(Image.open("ktu_uzay_neila.png"))) 

#logo
logo = ImageTk.PhotoImage(Image.open("ktu_uzay_neila.png").resize((200,152)))
logo_label = Label( root, image=logo, bg="white", width=232 ) 
logo_label.place(x=5,y=50)

#----------------------------------------------------------------------------------------------------------------------------------

# dosyayı temizleme
if (os.path.exists("TELEMETRI VERILERI/telemetri.csv")):

    print("yol bulundu")

    datafile_csv = open("TELEMETRI VERILERI/telemetri.csv", "a", newline='')
    datafile_csv.seek(0)
    datafile_csv.truncate(0)

    headers = [ "TAKIMNO", "PAKETNUMARASI", "GÖNDERMESAATİ", "BASINÇ1", "BASINÇ2", 
               "YÜKSEKLİK1", "YÜKSEKLİK2", "İRTİFAFARKI", "İNİŞHIZI", "SICAKLIK", "PİLGERİLİMİ", 
               "GPS1 LATITUDE", "GPS1 LONGITUDE", "GPS1 ALTITUDE", "GPS2 LATITUDE", "GPS2 LONGITUDE", "GPS2 ALTITUDE",
             "UYDUSTATÜSÜ", "PITCH", "ROLL", "YAW", "DÖNÜŞSAYISI", "VİDEO AKTARIMI BİLGİSİ"]
    headerWriter = csv.DictWriter(datafile_csv, fieldnames= headers )
    headerWriter.writeheader()
    datafile_csv.close()



#------------------------------------------------------------------------------------------------------------------------------------

top_frame_label = LabelFrame(root,
                             background="#0059aa",
                             border=0,
                             width=1920,
                             height=50)
top_frame_label.place(x=0,y=0)



#------------------------------------------------------------------------------------------------------------------------------------

#clock function
def clock():
    hour = time.strftime("%H")
    minute = time.strftime("%M")
    second = time.strftime("%S")
    day= time.strftime("%d")
    month= time.strftime("%m")
    year= time.strftime("%Y")
    
    clock_label.config(text= hour+":"+minute+":"+second+"   "+day+"/"+month+"/"+year)
    clock_label.after(1000,clock)

#clock widgets
clock_label = Label(top_frame_label,
                    text="", 
                    width=35, 
                    font=("Helvetica",20),
                    fg="white", bg="#0059aa", anchor="w")
clock_label.place(x=0,y=4)
clock()




#------------------------------------------------------------------------------------------------------------------------------------

#takım no:
teamNoLabel = Label(top_frame_label, 
                    text="Takım No: 356356",
                    width=50, 
                    font=("Helvetica",20),
                    fg="white", bg="#0059aa",anchor="w")
teamNoLabel.place(x=325,y=4)




#------------------------------------------------------------------------------------------------------------------------------------
#gelen paket adedi

numPacket = Label(top_frame_label,text="Gelen paket adedi: ", 
                    width=50, 
                    font=("Helvetica",20),
                    fg="white", bg="#0059aa",anchor="w")
numPacket.place(x=610,y=4)

#------------------------------------------------------------------------------------------------------------------------------------

# manuel control button

def leave():
    global ser 
    leavetext= b'a'
    if (ser.isOpen() ):
        ser.write(leavetext)


def sis():
    global ser 
    sistext= b's'
    if (ser.isOpen() ):
        ser.write(sistext)


def buzzer():
    global ser 
    buzzertext= b'b'
    if (ser.isOpen() ):
        ser.write(buzzertext)


def motor():
    global ser 
    motortext = b'r'
    if (ser.isOpen() ):
        ser.write(motortext)



def plus():
    global ser 
    plustext = b'p'
    if (ser.isOpen() ):
        ser.write(plustext)



def minus():
    global ser 
    minustext = b'm'
    if (ser.isOpen() ):
        ser.write(minustext)


leaveBtn = Button(top_frame_label, text= u"Görev Yükünü Ayır",font=("Helvetica",12), state= DISABLED ,command= leave, width = 15)
leaveBtn.place(x=1250, y=10)

sisBtn = Button(top_frame_label, text= u"Sis",font=("Helvetica",12), state= DISABLED , command= sis, width = 15)
sisBtn.place(x=1400, y=10)

buzzerBtn = Button(top_frame_label, text= u"Buzzer",font=("Helvetica",12), state= DISABLED , command= buzzer, width = 15)
buzzerBtn.place(x=1550, y=10)

activeBtn = Button(top_frame_label, text = u"Motoru Aktifleştir", font=("Helvetica",12), state=DISABLED, command= motor, width=15 )
activeBtn.place(x=965, y=10) 

plusBtn = Button(top_frame_label, text=u"🔼", font=("Helvetica",12), state=DISABLED, command= plus, width=5 )
plusBtn.place(x=1115, y=10)

minusBtn = Button(top_frame_label, text=u"🔽", font=("Helvetica",12),  state=DISABLED, command= minus, width=5 )
minusBtn.place(x=1175, y=10)




#------------------------------------------------------------------------------------------------------------------------------------

#battery
def battery():
    battery_info = psutil.sensors_battery
    global percent
    percent = battery_info().percent
    battery_label.config(text="%" + str(percent))

    battery_label.after(1000,battery)

battery_label = Label(top_frame_label, 
                      text="",
                      width=5, 
                      font=("Helvetica",20),
                      fg="white", bg="#0059aa",anchor="w")
battery_label.place(x=1772,y=6)
battery()

def battery_progress(): 
    global percent
    battery_progress_bar['value'] = percent
    battery_progress_bar.after(1000,battery_progress)

battery_progress_bar = ttk.Progressbar(top_frame_label,
                                       orient=HORIZONTAL,
                                       length=60, mode="determinate")
battery_progress_bar.place(x=1850,y=15)


battery_progress()




#------------------------------------------------------------------------------------------------------------------------------------


#seri port 

seriPortOuter = LabelFrame(root,text=u"SERİ PORT",border=3, width=235, height=225)
seriPortOuter.place(x=5,y=402)


global text1 # global çünkü bağlantı sağlanınca configure ediliyor
text1= Label(seriPortOuter,text=u"Bağlantıyı Sağlayın", width=20, 
                    font=("Helvetica",12),
                    fg="white", bg="red")
text1.place(x=20,y=5)


text2= Label(seriPortOuter,text="COM Port : ", width=10, 
                    font=("Helvetica",12), anchor="w")
text2.place(x=18,y=35)

portList = ["COM3", "COM4", "COM5", "COM6", "COM7", "COM8"]
port = StringVar()
portCombo = ttk.Combobox(seriPortOuter, textvariable=port, font=("Helvetica",12), values = portList, width=8, height=4)
portCombo.set("port seçin") 
portCombo.place(x=106,y=35)



text3= Label(seriPortOuter,text=u"Hız: ", width=10, 
                    font=("Helvetica",12), anchor="w")
text3.place(x=18,y=60)

speedList = ["921600", "115200", "19200","157600", "74880"]
speed = StringVar()
speedCombo = ttk.Combobox(seriPortOuter, textvariable=speed, font=("Helvetica",12), values = speedList, width=8, height=4)
speedCombo.set("hız seçin") 
speedCombo.place(x=106,y=65)



def portConnect():
    global ser
    try:
        ser = serial.Serial() # timeout=0.050
        ser.port = port.get()
        ser.baudrate = int(speed.get())
        ser.setDTR(False)
        ser.setRTS(False)

        ser.open()
        # port not open error u varmış 
        if ser.isOpen():
            global text1
            text1['background'] = "green"
            text1.configure(text="Bağlantı kuruldu")

            leaveBtn['state']= NORMAL
            sisBtn['state']= NORMAL
            buzzerBtn['state']= NORMAL
            activeBtn['state'] = NORMAL
            plusBtn['state'] = NORMAL
            minusBtn['state'] = NORMAL

    except:
        #messagebox.showerror('Seri Port Hatası', 'Hata: Eksik bilgi girdiniz.')
            text1['background'] = "red"
            text1.configure(text="Eksik Bilgi Girildi")
        
        


threadPortConnect = threading.Thread(target=portConnect )


def GetPureData(mylist):
    global pureTelemetry
    pureTelemetry = mylist
    


def GetData():
    global ser
    global datas 
    global text1
    datas.clear()

    
    if ser.isOpen():
            pureData = ser.readline()  
    
            if pureData != None :
                GetPureData(pureData)
                convertedData = pureData.decode('UTF-8')
                convertedData = convertedData.replace("<"," ")
                convertedData = convertedData.replace(">"," ")
                convertedData = convertedData.split(",")
                
                # boşlukları kaldırma
                for item in range(0,24):
                    convertedData[item] = convertedData[item].lstrip()
                    convertedData[item] = convertedData[item].rstrip()


                # hayır \r\n düzeltme kısmı
                fix = convertedData[-1]
                fix = fix.replace(" \r\n"," ")
                convertedData[-1] = fix

                # 0 takım no, 
                # 2 zaman

                # veriler hatalı olursa patlar burası


                convertedData[1]= int(convertedData[1])     # paket no
                convertedData[3]= float(convertedData[3])   # gy basınç
                convertedData[4]= float(convertedData[4])   # t basınç
                convertedData[5]= float(convertedData[5])   # gy yükseklik
                convertedData[6]= float(convertedData[6])   # t yükseklik
                convertedData[7]= float(convertedData[7])   # irtifa
                convertedData[8]= float(convertedData[8])   # hız
                convertedData[9]= float(convertedData[9])   # sıcaklık
                convertedData[10]= float(convertedData[10]) # pil
                convertedData[11]= float(convertedData[11]) # gy la
                convertedData[12]= float(convertedData[12]) # gy long
                convertedData[13]= float(convertedData[13]) # gy al
                convertedData[14]= float(convertedData[14]) # t la
                convertedData[15]= float(convertedData[15]) # t long
                convertedData[16]= float(convertedData[16]) # t al
                convertedData[17]= str(convertedData[17])   # statu
                convertedData[18]= float(convertedData[18]) # pitch 
                convertedData[19]= float(convertedData[19]) # roll
                convertedData[20]= float(convertedData[20]) # yaw
                convertedData[21]= float(convertedData[21]) # dönüş sayısı
                convertedData[22]= str(convertedData[22])   # video
                convertedData[23]= float(convertedData[23]) # işlemci sıcaklığı

                datas = convertedData.copy()
                # threadstoreCSV.start()   
                storeCSV()


                datas.append( " " ) # 24. boş veri 0-24, csv'ye bu boş veri eklenmiyor

                print(datas)

            else:
                text1['background'] = "red"
                text1.configure(text="Boş Veri")
                print(pureData)
               #  messagebox.showerror('Veri Hatası', 'Hata: Boş dönüştürülemeyen telemetri verisi.')





def storeCSV():
    global datas
    csv_datas = {}
    i=0
    
    headers = [ "TAKIMNO", "PAKETNUMARASI", "GÖNDERMESAATİ", "BASINÇ1", "BASINÇ2", 
               "YÜKSEKLİK1", "YÜKSEKLİK2", "İRTİFAFARKI", "İNİŞHIZI", "SICAKLIK", "PİLGERİLİMİ", 
               "GPS1 LATITUDE", "GPS1 LONGITUDE", "GPS1 ALTITUDE", "GPS2 LATITUDE", "GPS2 LONGITUDE", "GPS2 ALTITUDE",
             "UYDUSTATÜSÜ", "PITCH", "ROLL", "YAW", "DÖNÜŞSAYISI", "VİDEO AKTARIMI BİLGİSİ"]

    for head in headers:
        csv_datas[head] = datas[i] 
        i += 1


    # "C:/Users/Pc/Desktop/NeilA-UI/NeilA-UI/TELEMETRI VERILERI/telemetri.csv"
    # "C:\Users\Pc\Desktop\NeilA-UI\NeilA-UI\TELEMETRI VERILERI\telemetri.csv"


    # veriler için klasör oluştur
    if not  (os.path.exists("TELEMETRI VERILERI")):  #"C:\Users\Pc\Desktop\NeilA-UI\NeilA-UI\TELEMETRI VERILERI\telemetri.csv"
        dirName = "TELEMETRI VERILERI"
        os.makedirs(dirName)


    # veriler için csv oluştur
    if not (os.path.exists("TELEMETRI VERILERI/telemetri.csv")):
        datafile_csv = open("TELEMETRI VERILERI/telemetri.csv","x")
        datafile_csv.close()


    # verileri .csv içine yaz
    if (os.path.exists("TELEMETRI VERILERI/telemetri.csv")):
        datafile_csv = open("TELEMETRI VERILERI/telemetri.csv", "a", newline='')

        writer = csv.DictWriter(datafile_csv, fieldnames= headers )

        writer.writerow(csv_datas)

        datafile_csv.close()

# threadstoreCSV = threading.Thread(target=storeCSV )


#grafik için
global x
x=0
global old_datas
old_datas=[]

def StartListing():                                  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    #global datas
    if not stopFlag : 

        global x
        #global datas
        global old_datas
        global ser

        GetData()
        if datas != []:

            paketno = datas[1]
            numPacket.configure(text="Gelen paket adedi: "+ str(paketno)) 

            StatuChange(datas)

            GraphIt(plot1, x, 3, plot1Canvas)
            GraphIt(plot2, x, 4, plot2Canvas) 
            GraphIt(plot3, x, 5, plot3Canvas)
            GraphIt(plot4, x, 6, plot4Canvas)
            GraphIt(plot5, x, 23, plot5Canvas)
            GraphIt(plot6, x, 9, plot6Canvas)
            GraphIt(plot7, x, 10, plot7Canvas)
            GraphIt(plot8, x, 8, plot8Canvas)

            #threadGraphItGYP.start()
            #threadGraphItTP.start()
            #threadGraphItGYY.start()
            #threadGraphItTY.start()
            #threadGraphItIS.start()
            #threadGraphItS.start()
            #threadGraphItP.start()
            #threadGraphItH.start()


            x= x+1
            old_datas = datas.copy()

            #threadDotTelemetryListing.start()
            #threadTeleTableListing.start()

            DotTelemetryListing()
            TeleTableListing()


            angles = (datas[18], datas[19], datas[20])
            animation.FuncAnimation(fig, animate(angles), interval=1000, blit=True, repeat=True)


            x_locationYuk = datas[11]
            y_locationYuk = datas[12]
            x_locationTasiyici = datas[14]
            y_locationTasiyici = datas[15]
            yukMap.set_position(x_locationYuk,y_locationYuk, marker=True)
            tasiyiciMap.set_position(x_locationTasiyici,y_locationTasiyici, marker=True)


            if datas[22] == 'Evet':
                text7["background"] = "green"
                text7["foreground"] = "white"
                text7.configure(text="Dosya Görev Yükünde")

        else:
            text1['background'] = "red"
            text1.configure(text="Hatalı Veri Formatı")
            print(datas)
        #    messagebox.showerror('Veri Hatası', 'Hata: Veriler listelemeye uygun değil.')

    seriPortOuter.after(2000,StartListing)



threadStartListing = threading.Thread(target=StartListing )


def StopListing():
    global stopFlag
    stopFlag = True

threadStopListing = threading.Thread(target=StopListing )


def AgainListing():
    global stopFlag
    stopFlag = False
    seriPortOuter.after(2000,threadStartListing.start)

threadAgainListing = threading.Thread(target=AgainListing )



def OpenTelemetryFolder():
    if (os.path.exists("TELEMETRI VERILERI/telemetri.csv")):
        os.startfile(r"C:\Users\Pc\Desktop\NeilA-UI\NeilA-UI\TELEMETRI VERILERI")

threadOpenTelemetryFolder = threading.Thread(target=OpenTelemetryFolder )




portConnectButton = Button(seriPortOuter, text=u"Bağlantı Kur",font=("Helvetica",11), command=portConnect, width=20)  #  command=lambda: threadPortConnect.start()
portConnectButton.place(x=18,y=93)

ListingButton = Button(seriPortOuter, text=u"Başla",font=("Helvetica",11), command=lambda: threadStartListing.start() , width=9) 
ListingButton.place(x=18,y=132)

StopButton = Button(seriPortOuter, text=u"Durdur",font=("Helvetica",11), command=lambda: threadStopListing.start() , width=9) 
StopButton.place(x=118,y=132)

openTeleFoldBtn = Button(seriPortOuter, text=u"Telemetri Klasörünü Aç",font=("Helvetica",11), command=OpenTelemetryFolder , width=20) 
openTeleFoldBtn.place(x=18,y=167)

#AgainListingButton = Button(seriPortOuter, text=u"Devam Et",font=("Helvetica",11), command=lambda: threadAgainListing.start() , width=9) 
#AgainListingButton.place(x=118,y=167)




#------------------------------------------------------------------------------------------------------------------------------------



#uydu durumu


statuFrame = LabelFrame(root,text="UYDU DURUMU", border=3, width =215, height= 230)
statuFrame.place(x=5,y=210)

defaultColorLabel = Label(statuFrame) # for default color

statuText1 = Label(statuFrame, text=u"Görev Başladı", anchor='w',width=24, font=("Helvetica",12)) # , bg="green" vardı
statuText1.grid(row=0,column=0,padx=4)

statuText2 = Label(statuFrame, text=u"Uçuş Bekleniyor", anchor='w',width=24, font=("Helvetica",12))
statuText2.grid(row=1,column=0,padx=4)

statuText3 = Label(statuFrame, text=u"Model Uydu Yükselmekte", anchor='w',width=24, font=("Helvetica",12))
statuText3.grid(row=2,column=0,padx=4)

statuText4 = Label(statuFrame, text=u"Model Uydu İnişte", anchor='w',width=24, font=("Helvetica",12))
statuText4.grid(row=3,column=0,padx=4)

statuText5 = Label(statuFrame, text=u"Ayrılma Gerçekleşti", anchor='w',width=24, font=("Helvetica",12))
statuText5.grid(row=4,column=0,padx=4)

statuText6 = Label(statuFrame, text=u"G.Yükü Kurtarılmayı Bekliyor", anchor='w',width=24, font=("Helvetica",12))
statuText6.grid(row=5,column=0,padx=4)

statuText7 = Label(statuFrame, text=u"Görev Tamamlandı", anchor='w',width=24, font=("Helvetica",12))
statuText7.grid(row=6,column=0,padx=4)

def StatuChange(datas):
    if datas[17] != None:
        if datas[17] == "Görev Başladı":
            statuText1['background'] = "green"
            statuText2['background'] = defaultColorLabel['background']
            statuText3['background'] = defaultColorLabel['background']
            statuText4['background'] = defaultColorLabel['background']
            statuText5['background'] = defaultColorLabel['background']
            statuText6['background'] = defaultColorLabel['background']
            statuText7['background'] = defaultColorLabel['background']

        elif datas[17] == "Uçuş Bekleniyor":
            statuText1['background'] = "green"
            statuText2['background'] = "green"
            statuText3['background'] = defaultColorLabel['background']
            statuText4['background'] = defaultColorLabel['background']
            statuText5['background'] = defaultColorLabel['background']
            statuText6['background'] = defaultColorLabel['background']
            statuText7['background'] = defaultColorLabel['background']

        elif datas[17] == "Model Uydu Yükselmekte":
            statuText1['background'] = "green"
            statuText2['background'] = "green"
            statuText3['background'] = "green"
            statuText4['background'] = defaultColorLabel['background']
            statuText5['background'] = defaultColorLabel['background']
            statuText6['background'] = defaultColorLabel['background']
            statuText7['background'] = defaultColorLabel['background']

        elif datas[17] == "Model Uydu İnişte":
            statuText1['background'] = "green"
            statuText2['background'] = "green"
            statuText3['background'] = "green"
            statuText4['background'] = "green"
            statuText5['background'] = defaultColorLabel['background']
            statuText6['background'] = defaultColorLabel['background']
            statuText7['background'] = defaultColorLabel['background']

        elif datas[17] == "Ayrılma Gerçekleşti":
            statuText1['background'] = "green"
            statuText2['background'] = "green"
            statuText3['background'] = "green"
            statuText4['background'] = "green"
            statuText5['background'] = "green"
            statuText6['background'] = defaultColorLabel['background']
            statuText7['background'] = defaultColorLabel['background']

        elif datas[17] == "Görev Yükü Kurtarılmayı Bekliyor":
            statuText1['background'] = "green"
            statuText2['background'] = "green"
            statuText3['background'] = "green"
            statuText4['background'] = "green"
            statuText5['background'] = "green"
            statuText6['background'] = "green"
            statuText7['background'] = defaultColorLabel['background']

        elif datas[17] == "Görev Tamamlandı":
            statuText1['background'] = "green"
            statuText2['background'] = "green"
            statuText3['background'] = "green"
            statuText4['background'] = "green"
            statuText5['background'] = "green"
            statuText6['background'] = "green"
            statuText7['background'] = "green"

        else:
            statuText1['background'] = "red"
            statuText2['background'] = "red"
            statuText3['background'] = "red"
            statuText4['background'] = "red"
            statuText5['background'] = "red"
            statuText6['background'] = "red"
            statuText7['background'] = "red"
           


# threadStatuChange = threading.Thread(target=StatuChange, args= (datas), )

#------------------------------------------------------------------------------------------------------------------------------------

#dosya yükle

dosyaYukleOuter = LabelFrame(root,text=u"DOSYA YÜKLE",border=3, width=235,height=275)
dosyaYukleOuter.place(x=5,y=630)

text4 = Label(dosyaYukleOuter,text= "Server: ", anchor="w", width=7, font=("Helvetica",12))
text4.place(x=3, y=5)
serverEntry = Entry(dosyaYukleOuter, font=("Helvetica",12),  width=14)
serverEntry.insert(0, "192.168.4.3")
serverEntry.place(x=85,y=5)

text5 = Label(dosyaYukleOuter,text="Name: ", anchor="w", width=7, font=("Helvetica",12))
text5.place(x=3, y=35)
nameEntry = Entry(dosyaYukleOuter, font=("Helvetica",12), width=14)
nameEntry.insert(0, "NeilA")
nameEntry.place(x=85,y=35)

text6 = Label(dosyaYukleOuter,text="Password: ", anchor="w", width=9, font=("Helvetica",12))
text6.place(x=3, y=65)
passwordEntry = Entry(dosyaYukleOuter, font=("Helvetica",12), width=14)
passwordEntry.place(x=85,y=65)


def getConnect():
    
    #serverIP= serverEntry.get()
    #name= nameEntry.get()
    #password = passwordEntry.get()

    #serverIP= 'sosyalhizmetvedanismanlik.com'
    #name= 'sos96lhizmetcom'
    #password= '02wvVz!.fczc'

    serverIP= 'ftp.dlptest.com' 
    name= 'dlpuser' 
    password= 'rNrKYTX9g7z3RgJRmxWuGHbeu' 

    global ftp
    ftp = ftplib.FTP(serverIP)
    ftp.login(name , password)

    if(ftp.getwelcome()):
        text7["background"] = "green"
        text7["foreground"] = "white"
        text7.configure(text="Bağlantı Kuruldu")

threadgetConnect = threading.Thread(target=getConnect )


def GetFileName(paramP):
    global f_path
    f_path = paramP

def GetFileSize(paramS):
    global f_size
    f_size = paramS


def PickFile():
     filepath = filedialog.askopenfilename(initialdir= "C:/Users/Pc/Downloads",
                                          title= "Select File",
                                          filetypes= ( ("video files","*.mp4"),
                                                       ("all files","*.*") ) )  
     
     if filepath != None:
         text7["background"] = "green"
         text7["foreground"] = "white"
         text7.configure(text="Dosya Seçildi")

     GetFileName(filepath)

threadPickFile = threading.Thread(target = PickFile)



def UploadProgress(param): 
    uploadBar['value'] += (8192*185)/f_size

def SendFile():
    global ftp
    global f_path

    targetVideo = f_path
    targetFile = open(targetVideo, "rb")
    filesize = os.path.getsize(targetVideo)
    GetFileSize(filesize)

    if(ftp.getwelcome()):

        ftp.storbinary('STOR '+'neilaftp.mp4', targetFile, callback = UploadProgress )

        targetFile.close()
        ftp.quit()
        text7["background"] = "green"
        text7["foreground"] = "white"
        text7.configure(text="Aktarım Gerçekleşti")

threadSendFile = threading.Thread(target = SendFile)

getConnectButton = Button(dosyaYukleOuter, text="Bağlantı Kur",font=("Helvetica",11), command = lambda: threadgetConnect.start(), width=20)   # getConnect
getConnectButton.place(x=20,y=95)

filePickButton = Button(dosyaYukleOuter, text="Dosya Seç", font=("Helvetica",11), command = lambda: threadPickFile.start(), width=20)       # PickFile
filePickButton.place(x=20,y=130) 

fileUploadButton = Button(dosyaYukleOuter, text="Dosya Yükle", font=("Helvetica",11), command= lambda: threadSendFile.start(), width=20)    # SendFile
fileUploadButton.place(x=20,y=165) 


text7 = Label(dosyaYukleOuter,text=u" Bağlantı Durumu ", width=20, font=("Helvetica",12), anchor = "center",bg="green")
text7.place(x=22,y=200)
    
    

uploadBar = ttk.Progressbar(dosyaYukleOuter,
                                       orient=HORIZONTAL,
                                       length=185, mode="determinate")
uploadBar.place(x=23,y=230)




#------------------------------------------------------------------------------------------------------------------------------------

# asenkron video

secondUI = LabelFrame(root,text=u"ASENKRON VİDEO ALIMI",border=3, width=235, height=70)
secondUI.place(x=5,y=908)

def openSecPage():

    secondroot = Tk()
    secondroot.title(u"DOSYA İNDİR")
    secondroot.geometry("500x400")
    secondroot.configure(bg="#0059aa")


    secPort = LabelFrame(secondroot, text=u"SERİ PORT", border=5, width=400,height=325)
    secPort.place(relx=.5, rely=.5, anchor="center")


    secPortLabel= Label(secPort, text="Port: ", width=5, font=("Helvetica",10) )
    secPortLabel.place(x=50,y=30)

    secPortList = ["Option1", "Option2", "Option3",
              "Option4", "Option5", "Option6"]
 
    secPortCombo = ttk.Combobox(secPort, values = secPortList, width=10)
    secPortCombo.set("") # port seç yazılabilir
    secPortCombo.place(x=95,y=30)


    secHizLabel = Label(secPort, text=u"Hız: ", width=4, font=("Helvetica",10))
    secHizLabel.place(x=195,y=30)

    secHizList = ["Option1", "Option2", "Option3",
              "Option4", "Option5", "Option6"]
 
    sechizCombo = ttk.Combobox(secPort, values = secHizList, width=10)
    sechizCombo.set("") 
    sechizCombo.place(x=235,y=30)

    sec_text = Label(secPort, text=u"Bağlantı Durumu", width=30, font=("Helvetica",10))
    sec_text.place(x=80,y=70)

    openConButton = Button(secPort,text=u"Bağlantıyı Kur", width=30)
    openConButton.place(x=80,y=100)


    DownloadButton = Button(secPort,text=u"Dosyayı İndir", width=30)
    DownloadButton.place(x=80,y=140)

    # percent tanımla 
    percentUpload = 50
    def UploadProgress(): 
    
        upload_progress_bar['value'] = percentUpload
        upload_progress_bar.after(1000,UploadProgress)


    upload_progress_bar = ttk.Progressbar(secPort,
                                           orient=HORIZONTAL,
                                           length=223, mode="determinate") # length eşit mi?
    upload_progress_bar.place(x=80,y=190)
    UploadProgress()

    openButton = Button(secPort,text=u"Dosya Konumunu Aç", width=30)
    openButton.place(x=80,y=230)
    
    secondroot.focus()
    # window.after(1, lambda: window.focus_force())

openSecUIButton = Button(secondUI, text=u"Dosya İndir", font=("Helvetica",12) ,width=20, command = openSecPage)
openSecUIButton.pack(padx=20,pady=11)




#------------------------------------------------------------------------------------------------------------------------------------
#camera
camera_frame = LabelFrame(root, text=u"KAMERA STREAMING",
                     border=2,
                     width=250,
                     height=100)
camera_frame.place(x=249,y=50)

camera_label = Label(camera_frame,width=62,height=20)
camera_label.grid(row=0,column=0)

global capture

capture = cv2.VideoCapture(1) 

global out
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('neila.mp4', fourcc, 20.0, (640, 480))

global stopCam
stopCam = False


def show_frames():

    global capture
    global out

    # read the capture
    ret, frame = capture.read()

    # record
    out.write(frame)

    # turned into image and display
    cv2image = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image = img) 
    camera_label.imgtk = imgtk
    camera_label.configure(image=imgtk,width=436,height=302)


    # quit
    if (stopCam):       
        capture.release()
        out.release()
        cv2.destroyAllWindows()
        return

    camera_label.after(20,show_frames)



threadCamera = threading.Thread(target=show_frames)


buttonLabel = Label(camera_frame) 
buttonLabel.grid(row=1,column=0)

connectButton = Button (buttonLabel, text=u"Kameraya Bağlan ve Kayıt Et", command=threadCamera.start, width=25)
connectButton.grid(row=0,column=0,padx=5)

stopButton = Button(buttonLabel, text=u"Kamerayı Durdur", command= lambda: globals().update(stopCam=True) , width=13)
stopButton.grid(row=0,column=1,padx=5)

#recordButton = Button(buttonLabel, text=u"Kayıt Et", width= 13)
#recordButton.grid(row=0,column=2,padx=3)

def openFile():

    os. startfile(r"C:\Users\Pc\Desktop\NeilA-UI\NeilA-UI")
    

openFileButton = Button(buttonLabel, text=u"Dosyayı Aç", command = openFile, width= 13)
openFileButton.grid(row=0,column=2,padx=5)





#------------------------------------------------------------------------------------------------------------------------------------

mapFrame = LabelFrame(root,text="KONUM",
                     border=5,
                     width=300,
                     height=275)
mapFrame.place(x=249,y=408)

yukMap = tkintermapview.TkinterMapView(mapFrame, width=211,height=250, corner_radius=0)
yukMap.grid(row=0,column=0,padx=3, pady=3)
yukMap.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
yukMap.set_position(40.998066,39.763824, marker=True) # (40.998066,39.763824)
# yukMap.set_zoom(10)


tasiyiciMap = tkintermapview.TkinterMapView(mapFrame, width=211,height=250, corner_radius=0)
tasiyiciMap.grid(row=0,column=1,padx=3, pady=3)
tasiyiciMap.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
tasiyiciMap.set_position(40.995251,39.776928, marker=True) # (40.995251,39.776928)
# tasiyiciMap.set_zoom(10)

#------------------------------------------------------------------------------------------------------------------------------------


d3Frame = LabelFrame(root,text=u"UYDUNUN DURUŞU",
                     border=5,
                     width=255,
                     height=225)
d3Frame.place(x=249,y=690)

def x_rotation(p, roll):
    x0, y0, z0 = p
    roll = math.radians(roll)
    x1 = x0
    y1 = y0 * math.cos(roll) - z0 * math.sin(roll)
    z1 = y0 * math.sin(roll) + z0 * math.cos(roll)
    return (x1, y1, z1)

def y_rotation(p, pitch):
    x0, y0, z0 = p
    pitch = math.radians(pitch)
    x1 = x0 * math.cos(pitch) + z0 * math.sin(pitch)
    y1 = y0
    z1 = z0 * math.cos(pitch) - x0 * math.sin(pitch)
    return (x1, y1, z1)

def z_rotation(p, yaw):
    x0, y0, z0 = p
    yaw = math.radians(yaw)
    x1 = x0 * math.cos(yaw) - y0 * math.sin(yaw)
    y1 = x0 * math.sin(yaw) + y0 * math.cos(yaw)
    z1 = z0
    return (x1, y1, z1)

# uydunun cizimi

def uydu(pitch, roll, yaw): # x,y,z rotation angles
    path = "ABPNCDMLEFKJGHIRPNMLKJIRASTBCUVDEYZFGXWHA"  # "ABPNCDMLEFKJGHIRPNMLKJIRABCDEFGHASTBCUVDEYZFGXWH" "ABPNCDMLEFKJGHIRPNMLKJIRASTBCUVDEYZFGXWHA"
    points_0 = {
        # üst kısım
        "A": ( 0.65,1.65,2.5 ),
        "B": ( 0.65,1.15,2.5 ),
        "C": ( 1,0.8,2.5 ),
        "D": ( 1.5,0.8,2.5 ),
        "E": ( 1.85,1.15,2.25 ),
        "F": ( 1.85,1.65,2.5 ),
        "G": ( 1.5,2,2.5 ),
        "H": ( 1,2,2.5 ),
        # alt kısım
        "I": ( 1,2,0 ),
        "J": ( 1.5,2,0 ),
        "K": ( 1.85,1.65,0 ),
        "L": ( 1.85,1.15,0 ),
        "M": ( 1.5,0.8,0 ),
        "N": ( 1,0.8,0 ),
        "P": ( 0.65,1.15,0 ),
        "R": ( 0.65,1.65,0 ),
        # kollar
        "S": ( -0.1,1.65,2.5 ),
        "T": ( -0.1,1.15,2.5 ),
        "U": ( 1,0.05,2.5 ),
        "V": ( 1.5,0.05,2.5 ),
        "Y": ( 2.6,1.15,2.5 ),
        "Z": ( 2.6,1.65,2.5 ),
        "X": ( 1.5,2.75,2.5 ),
        "W": ( 1,2.75,2.5 ),
    }
    points = {k:points_0[k] for k in points_0.keys()}
  
    points = {k:x_rotation(points[k], pitch) for k in points.keys()}
    points = {k:y_rotation(points[k], roll) for k in points.keys()}
    points = {k:z_rotation(points[k], yaw) for k in points.keys()}
    
    return [points[p] for p in path]

# animasyon

def animate(angle_tuple):

    pitch, roll, yaw = angle_tuple

    X,Y,Z = list(zip( *uydu(roll, pitch, yaw) ))

    X = np.array(X)
    Y = np.array(Y)
    Z = np.array(Z)
    line.set_data(X, Y)
    line.set_3d_properties(Z)
    return line,


fig = plt.figure(figsize=(4.34,2.70), dpi=100) 

canvas = FigureCanvasTkAgg(fig, master=d3Frame)
canvas.draw()

ax = Axes3D(fig, auto_add_to_figure=False)
fig.add_axes(ax)

# NOTE: Can't pass empty arrays into 3d version of plot()
dataset = list(zip(*uydu(0,0,0)))


line, = plt.plot(dataset[0], dataset[1], dataset[2], color = "#FF4500")
limits = (-3, 3)
ax.set_xlim3d(*limits)
ax.set_ylim3d(*limits)
ax.set_zlim3d(*limits)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')


canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)



#------------------------------------------------------------------------------------------------------------------------------------

#graph

graph_canvas = Canvas(root, width=1000,height=650, bg="#0059aa" )
graph_canvas.place(x=700,y=50) 

# graph_canvas.config(highlightbackground="white")

#basınç 1
fig_plot1= Figure(figsize=(3,3), dpi=100)
plot1= fig_plot1.add_subplot(111)
plot1.set_title(u'Görev Yükü Basıncı (Pa)',fontsize=12)
plot1Canvas = FigureCanvasTkAgg(fig_plot1, master=graph_canvas)
plot1Canvas.get_tk_widget().grid(row=0,column=0,pady=5, padx=3)
plot1Canvas.draw()

#basınç 2
fig_plot2= Figure(figsize=(3,3), dpi=100)
plot2= fig_plot2.add_subplot(111)
plot2.set_title(u'Taşıyıcı Basıncı (Pa)',fontsize=12)
plot2Canvas = FigureCanvasTkAgg(fig_plot2, master=graph_canvas)
plot2Canvas.get_tk_widget().grid(row=1,column=0,pady=5, padx=3)
plot2Canvas.draw()

#yükseklik 1
fig_plot3= Figure(figsize=(3,3), dpi=100)
plot3= fig_plot3.add_subplot(111)
plot3.set_title(u'Görev Yükü Yüksekliği (m)',fontsize=12)
plot3Canvas = FigureCanvasTkAgg(fig_plot3, master=graph_canvas)
plot3Canvas.get_tk_widget().grid(row=0,column=1,pady=5, padx=2)
plot3Canvas.draw()

#yükseklik 2
fig_plot4= Figure(figsize=(3,3), dpi=100)
plot4= fig_plot4.add_subplot(111)
plot4.set_title(u'Taşıyıcı Yüksekliği (m)',fontsize=12)
plot4Canvas = FigureCanvasTkAgg(fig_plot4, master=graph_canvas)
plot4Canvas.get_tk_widget().grid(row=1,column=1,pady=5, padx=2)
plot4Canvas.draw()

#işlemci sıcaklığı özgün görev
fig_plot5= Figure(figsize=(3,3), dpi=100)
plot5= fig_plot5.add_subplot(111)
plot5.set_title('İşlemci Sıcaklığı (°C)',fontsize=12)
plot5Canvas = FigureCanvasTkAgg(fig_plot5, master=graph_canvas)
plot5Canvas.get_tk_widget().grid(row=0,column=2,pady=5, padx=2)
plot5Canvas.draw()

#sıcaklık
fig_plot6= Figure(figsize=(3,3), dpi=100)
plot6= fig_plot6.add_subplot(111)
plot6.set_title(u'Sıcaklık (°C)',fontsize=12)
plot6Canvas = FigureCanvasTkAgg(fig_plot6, master=graph_canvas)
plot6Canvas.get_tk_widget().grid(row=1,column=2,pady=5, padx=2)
plot6Canvas.draw()

#pil
fig_plot7= Figure(figsize=(3,3), dpi=100)
plot7= fig_plot7.add_subplot(111)
plot7.set_title('Pil Gerilimi (V)',fontsize=12)
plot7Canvas = FigureCanvasTkAgg(fig_plot7, master=graph_canvas)
plot7Canvas.get_tk_widget().grid(row=0,column=3,pady=5, padx=2)
plot7Canvas.draw()

#hız
fig_plot8= Figure(figsize=(3,3), dpi=100)
plot8= fig_plot8.add_subplot(111)
plot8.set_title(u'İniş Hızı (m/sn)',fontsize=12)
plot8Canvas = FigureCanvasTkAgg(fig_plot8, master=graph_canvas)
plot8Canvas.get_tk_widget().grid(row=1,column=3,pady=5, padx=2)
plot8Canvas.draw()


def GraphIt(myplot,xindex, yindex, canvas):
    global datas
    global old_datas
    x1 = xindex
    y1 = datas[yindex]
    
    if old_datas:
        x0 = x1-1
        y0 = old_datas[yindex]
        myplot.plot( [x0,x1],[y0,y1], color='#0059aa', linestyle= '-') 

    canvas.draw()

    

#threadGraphItGYP = threading.Thread(target= GraphIt, args=(plot1,x,3,plot1Canvas,) )
#threadGraphItTP = threading.Thread(target= GraphIt, args=(plot2,x,4,plot2Canvas,) )
#threadGraphItGYY = threading.Thread(target= GraphIt, args=(plot3,x,5,plot3Canvas,) )
#threadGraphItTY = threading.Thread(target= GraphIt, args=(plot4,x,6,plot4Canvas,) )
#threadGraphItIS = threading.Thread(target= GraphIt, args=(plot5,x,23,plot5Canvas,) )
#threadGraphItS = threading.Thread(target= GraphIt, args=(plot6,x,9,plot6Canvas) )
#threadGraphItP = threading.Thread(target= GraphIt, args=(plot7,x,10,plot7Canvas) )
#threadGraphItH = threading.Thread(target= GraphIt, args=(plot8,x,8,plot8Canvas) )

#------------------------------------------------------------------------------------------------------------------------------------

#telemetri

# creating notebook
telemetry = ttk.Notebook(root, width=1213, height=280)
telemetry.place(x=700, y=675)



dotTelemetry = Frame(telemetry)
dotTelemetry.pack(fill="both", expand = 1)




# creating alltelemetry tab
allTelemetryTabFrame = Frame(telemetry)
allTelemetryTabFrame.pack(fill="both", expand = 1)

# creating canvas for scrollbar 
allTelemetryCanvas = Canvas(allTelemetryTabFrame)
allTelemetryCanvas.pack(side="left", fill="both", expand=True)

# creating frame for content
allTelemetry = Frame(allTelemetryCanvas)
# allTelemetry.pack(fill="both", expand = 1)
allTelemetryCanvas.create_window((0, 0), window=allTelemetry, anchor="nw")

allTelemetry.bind(
    "<Configure>",
    lambda e: allTelemetryCanvas.configure(
        scrollregion=allTelemetryCanvas.bbox("all")
      )
)



telemetry.add(dotTelemetry, text= u"Anlık Telemetri")
telemetry.add(allTelemetryTabFrame, text= u"Hepsini Göster")



def OnMouseWheel(event):
    scrollbar.yview("scroll",event.delta,"units")
    return "break"

#------------------------------------------------------------

teleTitle_f_tab1 = [" ", "Takımno","Paketno","Zaman",
        "1Basınç","2Basınç",
        "1Yükseklik","2Yükseklik",
        "İrtifaFarkı","İnişHızı",
        "Sıcaklık",
        "PilGerilimi",
        "La1","Lo1","Al1",
        "La2","Lo2","Al2",
        "Durum",
        "Pitch","Roll","Yaw",
        "DönüşSayısı","Video",
        "İşlemci Sıcaklığı"]

for i in range(0,25):
    teleTitle_f_tab1[i] = teleTitle_f_tab1[i].encode('UTF-8')

# başlığın başında bir boşluk
empty = Label(allTelemetry, text="",width=3)
empty.grid(row=0,column=0,padx=1, pady=1)

# başlıklar
for j in range(1,25):
    entry = Label(allTelemetry,text=teleTitle_f_tab1[j].decode(),  font=("Helvetica",10), anchor='w', width=5, bd=2)
    entry.grid(row=0, column=j,padx=1, pady=0.5)

global packet
packet = 1
def TeleTableListing():

    global packet 
    global datas
    packetNum = Label(allTelemetry, text = packet, anchor="w",width=3)
    packetNum.grid(row=packet, column=0,pady=0.5)

    for item in range(1,25):
        takenData = Label(allTelemetry,text= datas[item-1], anchor='w', width=5, borderwidth=2, relief="groove")  # 23
        takenData.grid(row=packet, column=item,pady=0.5)

    packet += 1


# threadTeleTableListing = threading.Thread(target= TeleTableListing)


scrollbar1 = ttk.Scrollbar(allTelemetryTabFrame, orient='vertical', command=allTelemetryCanvas.yview)

allTelemetryTabFrame.bind("<MouseWheel>", OnMouseWheel) 
# scrollbar.focus_set()

scrollbar1.pack(side=RIGHT, fill="y")
allTelemetryCanvas.configure(yscrollcommand=scrollbar1.set)


# ------------------------------------------------------------------


# dot telemetry


teleTitle_f_tab2 = ["Takım no: ","Paket no: ","Zaman: ",
        "G.Y. Basıncı: ","T. Basıncı: ",
        "G.Y. Yüksekliği: ","T. Yüksekliği: ",
        "İrtifa Farkı: ","İniş Hızı: ",
        "Sıcaklık: ",
        "Pil Gerilimi: ",
        "G.Y. Latitude: ","G.Y. Longitude: ","G.Y. Altitude: ",
        "T. Latitude: ","T. Longitude: ","T. Altitude: ",
        "Durum: ",
        "Pitch: ","Roll: ","Yaw: ",
        "Dönüş Sayısı: ","Video Aktarım Bilgisi: ",
        "İşlemci Sıcaklığı: "," "]

birim = [ "", "", "",
            " Pa"," Pa",
            " m"," m",
            " m"," m/s",
            " °C", 
            " V", 
            " m", " m", " m", 
            " m", " m", " m",
            "",
            "°","°","°",
            "","",
           " °C",""]

for i in range(0,25):
    teleTitle_f_tab2[i] = teleTitle_f_tab2[i].encode('UTF-8')

dataIndex = 0
for col in range(5):
    for rw in range(5):
        # teleTitle[data] = teleTitle[data].encode('UTF-8')
        textData = Label(dotTelemetry, anchor = "w",width= 25,  font=("Helvetica",11), text= teleTitle_f_tab2[dataIndex].decode()+
                                                                        birim[dataIndex])
        textData.grid(row=rw, column=col, padx=4, pady=15)
        dataIndex = dataIndex +1 


def DotTelemetryListing():

    dataIndex = 0
    global datas 

    for col in range(5):
        for rw in range(5):
            # teleTitle[data] = teleTitle[data].encode('UTF-8')
            textData = Label(dotTelemetry, anchor = "w",width= 25, font=("Helvetica",11), text= teleTitle_f_tab2[dataIndex].decode()+
                                                                         str(datas[dataIndex])+
                                                                         birim[dataIndex])
            textData.grid(row=rw, column=col, padx=4, pady=15)
            dataIndex = dataIndex +1 


# threadDotTelemetryListing = threading.Thread(target= DotTelemetryListing)

root.mainloop()

