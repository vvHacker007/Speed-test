import win10toast
import speedtest
from tkinter import *
from tkinter.ttk import * 
from PIL import Image, ImageTk
import urllib.request


global anim
anim = None
global window
window = None
global connected
connected = None
global result
result = None
st = speedtest.Speedtest() 
global download
download = st.download()/1048576
global upload
upload = st.upload()/1048576
global ping
servernames =[]
names = st.get_servers(servernames)
ping = st.results.ping
data = [download,upload,ping]
formated_data = ['%.2f' % elem for elem in data]
global message
message = 'Download Speed: {}Mbps, \nUpload Speed: {}Mbps,\n Ping: {}ms'.format(*formated_data)

def network():
    try:
        urllib.request.urlopen('https://google.com')
        return True
    except:
        return False



class gif(Label):
    def __init__(self, master, filename):
        im = Image.open(filename)

        seq =  []
        try:
            while 1:
                seq.append(im.copy())
                im.seek(len(seq)) # skip to next frame
        except EOFError:
            pass # we're done

        try:
            self.delay = im.info['duration']
            if self.delay > 2000:
                self.delay = self.delay-2500
        except KeyError:
            self.delay = 100

        first = seq[0].convert('RGBA')
        self.frames = [ImageTk.PhotoImage(first)]

        Label.__init__(self, master, image=self.frames[0])

        temp = seq[0]
        for image in seq[1:]:
            temp.paste(image)
            frame = temp.convert('RGBA')
            self.frames.append(ImageTk.PhotoImage(frame))

        self.idx = 0

        self.cancel = self.after(self.delay, self.play)

    def play(self):
        self.config(image=self.frames[self.idx])
        self.idx += 1
        if self.idx == len(self.frames):
            self.idx = 0
        self.cancel = self.after(self.delay, self.play)

def restart():
    global window
    window = Tk()
    window.title('SpeedTest')
    window.wm_iconbitmap('speedtest_icon.ico')
    window.geometry("600x400")





    style = Style()
    style.configure('TButton', font = ('calibri', 20, 'bold'), borderwidth = '4', background = 'deep sky blue')
    style.map('TButton', foreground = [('active', '!disabled', 'green')], background = [('active', 'blue')])



    def connect():
        window.destroy()
        global connected
        connected = Tk()
        connected.title('SpeedTest-Connected')
        connected.wm_iconbitmap('speedtest_icon.ico')
        connected.geometry("800x720")
        

        style = Style()
        style.configure('TButton', font = ('calibri', 20, 'bold'), borderwidth = '4', background = 'deep sky blue')
        style.map('TButton', foreground = [('active', '!disabled', 'green')], background = [('active', 'blue')])


        def resume():
            
            global connected
            connected.destroy()
            
            global result   
            result = Tk()
            result.title('SpeedTest-Connected-Results')
            result.wm_iconbitmap('speedtest_icon.ico')
            result.geometry("200x250")
            
            global anim            
            anim = gif(result, 'pillow_imagedraw.gif')
            anim.pack()
            

            def results():
                global download
                global upload
                global ping
                global message
                global result
                result.destroy()
                
                final = Tk()
                final.title('SpeedTest-Connected-Results')
                final.wm_iconbitmap('speedtest_icon.ico')
                final.geometry("400x400")
                               
               
                L1 = Label(final, text="Download Speed:")
                L1.grid(row=0,column=0,padx=10,pady=10)
                
                L2 = Label(final, text="Upload Speed:")
                L2.grid(row=1,column=0,padx=10,pady=10)   
                
                L3 = Label(final, text="Ping:")
                L3.grid(row=2,column=0,padx=10,pady=10)

                download_label= Label(final, text=download).grid(row=0,column=1,padx=10,pady=10)

                upload_label = Label(final,text=upload).grid(row=1,column=1,padx=10,pady=10)

                ping_label = Label(final,text=ping).grid(row=2,column=1,padx=10,pady=10)
                              
               
                if network():
                    toaster = win10toast.ToastNotifier()
                    toaster.show_toast('Wifi Speedtest Successfull!', message, icon_path = 'speedtest_icon.ico', duration=60)
                else:
                    toaster = win10toast.ToastNotifier()
                    toaster.show_toast('Wifi Speedtest Failed!', 'Cannot connect to the internet\nPlease check your Internet Connection!!!', icon_2path = 'speedtest_icon.ico', duration=60)                                                         
            
            button_click = Button(result, text='√ RESULTS √', command=results).pack(side=BOTTOM)


        def disconnect():
            def quit():
                connected.destroy()
            anim.after_cancel(anim.cancel)
            button_quit = Button(connected, text='Quit', command=quit).pack()
            button_res = Button(connected, text='Resume', command=resume).pack()
        
        
        button_d = Button(connected, text='Disconnect', command=disconnect).pack()
        button_r = Button(connected, text='Refresh', command=refresh).pack()
        button_re = Button(connected, text='Result', command=resume).pack()
        
        global anim
        anim = gif(connected, 'connect_btn.gif')
        anim.pack(side=TOP)





    
    anim = gif(window, 'speedtest_start.gif')
    anim.pack(side = TOP)


    button_c = Button(window, text="Connect", command=connect).pack(side=BOTTOM)



    window.mainloop()

if __name__ == '__main__':
    def refresh():
        connected.destroy()
        restart()
    restart()