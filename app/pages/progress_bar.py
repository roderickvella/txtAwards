import customtkinter
import time

def pb_setup(self):
    self.pb = customtkinter.CTkProgressBar(master=self)
    self.pb_visible =True

def pb_animation(self):        
    self.pb.pack(pady=12,padx=10)

    xs = (x * 0.01 for x in range(0, 9))
    for x in xs:                            
        if(self.pb_visible):                
            self.pb.set(x)
            time.sleep(0.5)
    

def pb_hide(self):
    self.pb_visible = False
    self.pb.destroy()