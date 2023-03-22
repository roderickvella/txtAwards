import tkinter as tk
import customtkinter
import common.wallet
from common.preferences import font_type

class PageWelcomeScreen(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        customtkinter.CTkFrame.__init__(self, parent)
        self.controller = controller
  
    
    #called when page is mounted
    def page_did_mount(self):
        # create frame to hold GUI components
        self.main_frame = customtkinter.CTkFrame(master=self,fg_color="#2a2d2e")
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1) 

        connection_status = "Successfully connected to Node" if common.wallet.is_connected_node else "Error: Not Connected to Node"

        #top header
        self.title_label = customtkinter.CTkLabel(master=self.main_frame,  height=65,
                                        fg_color="#3E6E8C", text="Welcome", text_font=(font_type, 20),corner_radius=5)   
        self.title_label.grid(row=0,column=0, padx=(20, 20), pady=10, sticky="ew" )

        self.label_message = customtkinter.CTkLabel(master=self.main_frame,text=connection_status, text_font=(font_type, 12))
        self.label_message.grid(row=2, column=0, columnspan=1,  sticky="we")  
        
    #called when page is unmounted
    def page_did_unmount(self):       
        #clear widgets
        for widgets in self.winfo_children():
            widgets.destroy()