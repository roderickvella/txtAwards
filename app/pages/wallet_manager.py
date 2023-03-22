from tkinter import StringVar
import tkinter.messagebox
import customtkinter
import common.wallet
import common.file_manager
from common.preferences import font_type
import json



class PageWalletManager(customtkinter.CTkFrame):
    """
    Wallet Manager Page
    """

    def __init__(self, parent, controller):
        customtkinter.CTkFrame.__init__(self, parent)
        self.controller = controller

        self.menu_state = {1: "Wallet", 2: "Create Wallet",3:"Unlock Wallet",4:"Unlocked Wallet"}
        self.menu_state_index = 1

        self.img_back = controller.load_image(
            "/images/arrow-left-s-line.png", 20)
       
        self.wallet_unlocked = False
        self.show_private_key = False
        self.wallet_created = False
       
    #called when page is mounted
    def page_did_mount(self):
        self.frame_1 = customtkinter.CTkFrame(master=self,fg_color="#2a2d2e")
        self.frame_1.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.frame_1.grid_columnconfigure(0, weight=1) 
        
        self.reset()
        self.render()
        
    #called when page is unmounted
    def page_did_unmount(self):       
        #clear widgets
        for widgets in self.winfo_children():
            widgets.destroy()

    def render_header(self,back_button=True): 
        title_text = self.menu_state[self.menu_state_index]
        self.title_label = customtkinter.CTkLabel(master=self.frame_1,  height=65,
                                            fg_color="#3E6E8C", text=title_text, text_font=(font_type, 20),corner_radius=5)
        self.title_label.grid(row=0,column=0,columnspan=1, padx=(20, 20), pady=10, sticky="ew" )

        if(self.menu_state_index != 1 and back_button):
            self.btn_back = customtkinter.CTkButton(master=self.frame_1, image=self.img_back, text="", height=15,                                                    
                                                    command=lambda: self.button_menu_back())
            self.btn_back.grid(row=1, column=0, columnspan=1,  padx=(20, 20), pady=5, sticky="ew")        

    def render(self):
        self.clear_frame()
        if (self.menu_state_index == 1):
            self.main_wallet_menu_window()
        elif (self.menu_state_index == 2):
            self.create_wallet_window()
        elif (self.menu_state_index == 3):
            self.unlock_wallet_window()
        elif(self.menu_state_index==4):
            self.unlocked_wallet_window()

  
    def button_menu_back(self):
        if(self.menu_state_index ==2):
            self.menu_state_index = 1
        elif(self.menu_state_index==3):
            self.menu_state_index = 1
        elif(self.menu_state_index==4):
            self.menu_state_index = 4
            
        self.render()
    

    def main_wallet_menu_window(self):
        #top header
        self.render_header()                

        # render main body
        customtkinter.CTkButton(master=self.frame_1, text="Create Wallet", width=200, height=40,
                                                corner_radius=10,
                                                command=lambda:self.change_window(2)).grid(row=2, column=0, columnspan=1, padx=20, pady=10)

        customtkinter.CTkButton(master=self.frame_1, text="Unlock Wallet", width=200, height=40,
                                                corner_radius=10,
                                                command=lambda:self.change_window(3)).grid(row=3, column=0, columnspan=1, padx=20, pady=10)
    

    def create_wallet_window(self):
        self.render_header()
        self.wallet_created =False
        self.wallet_gui()
        

    def unlock_wallet_window(self):
        self.render_header()
        self.wallet_created =True
        self.wallet_gui()
        

    def unlocked_wallet_window(self):
        self.render_header(False)   
        self.wallet_unlocked = True
        self.wallet_gui()


    def wallet_gui(self):
        if (not self.wallet_unlocked):  

            self.label_password = customtkinter.CTkLabel(master=self.frame_1,
                                                            text="Enter Password")
            self.label_password.grid(
                row=2, column=0, columnspan=1,  sticky="w")

            self.entry_password = customtkinter.CTkEntry(master=self.frame_1,
                                                            width=120,
                                                            placeholder_text="password", show="*")
            self.entry_password.grid(
                row=3, column=0, columnspan=1, pady=5, padx=20, sticky="we")

            if not self.wallet_created:
                self.label_pk = customtkinter.CTkLabel(master=self.frame_1,
                                                        text="Enter Same Password")
                self.label_pk.grid(
                    row=4, column=0, columnspan=1, padx=20,  sticky="w")

                self.entry_valid_pass = customtkinter.CTkEntry(master=self.frame_1,
                                                                width=120,
                                                                placeholder_text="password", show="*")
                self.entry_valid_pass.grid(
                    row=5, column=0, columnspan=1, pady=5, padx=20, sticky="we")

            self.button_import = customtkinter.CTkButton(master=self.frame_1, text="Unlock" if self.wallet_created else "Create",
                                                            command=self.btn_create_unlock)
            self.button_import.grid(
                row=6, column=0, columnspan=1, padx=20, pady=10, sticky="w")
        else: #wallet unlocked
            self.label_title = customtkinter.CTkLabel(master=self.frame_1,
                                                      text="My Account", text_color="#92c0d3", text_font=(font_type, 15))
            self.label_title.grid(
                row=1, column=0, columnspan=1, pady=20, padx=20, sticky="we")

            self.label_publickey = customtkinter.CTkLabel(master=self.frame_1,
                                                          text="Address")
            self.label_publickey.grid(
                row=2, column=0, columnspan=1,  sticky="we")

            data_public_address = StringVar()
            data_public_address.set(common.wallet.local_account.address)

            self.entry_publicaddress = customtkinter.CTkEntry(master=self.frame_1,
                                                              width=120,
                                                              textvariable=data_public_address)
            self.entry_publicaddress.grid(
                row=3, column=0, columnspan=1, pady=5, padx=20, sticky="we")

            self.label_balance = customtkinter.CTkLabel(master=self.frame_1,
                                                        text="Balance")
            self.label_balance.grid(
                row=4, column=0, columnspan=1,  sticky="we")

            data_balance = StringVar()
            data_balance.set(str(common.wallet.get_balance_address())+" Matic")

            self.entry_balance = customtkinter.CTkEntry(master=self.frame_1,
                                                        textvariable=data_balance)
            self.entry_balance.grid(
                row=5, column=0, columnspan=1, pady=5, padx=20, sticky="we")

            if (self.show_private_key):
                self.label_privatekey = customtkinter.CTkLabel(master=self.frame_1,
                                                               text="Private Key")
                self.label_privatekey.grid(
                    row=6, column=0, columnspan=1,  sticky="we")

                data_privatekey = StringVar()
                data_privatekey.set(common.wallet.get_decoded_privatekey())

                self.entry_privatekey = customtkinter.CTkEntry(master=self.frame_1,
                                                               width=120,
                                                               textvariable=data_privatekey)
                self.entry_privatekey.grid(
                    row=7, column=0, columnspan=1, pady=5, padx=20, sticky="we")
            else:
                self.button_show_privatekey = customtkinter.CTkButton(master=self.frame_1, text="Show Private Key",
                                                                        command=self.btn_show_privatekey)
                self.button_show_privatekey.grid(
                    row=8, column=0, columnspan=1, padx=20, pady=10, sticky="w")


    def load_wallet(self, json_keyfile=None):
        input_password = self.entry_password.get()
        if (json_keyfile == None):
            json_keyfile = common.file_manager.file_load()

        if (json_keyfile is not None):
            self.wallet_unlocked = common.wallet.unlock_wallet(
                json_keyfile, input_password)
            if(self.wallet_unlocked):
                self.change_window(4)


    def btn_show_privatekey(self):
        self.show_private_key = True
        self.render()

    def btn_create_unlock(self):
        input_password = self.entry_password.get()

        if not self.wallet_created:
            # check that passwords match
            input_valid_password = self.entry_valid_pass.get()
            if (input_password != input_valid_password):
                tkinter.messagebox.showerror(
                    title="Validation Password", message="Passwords do not match")
                return

            # create account
            keyfile = common.wallet.create_wallet(input_password)
            json_keyfile = json.dumps(keyfile)
            # ask user to save file
            file_saved = common.file_manager.file_save(
                json_keyfile, "keyfile-txtawards.json", ".json")
            if (file_saved):                
                self.load_wallet(keyfile)

        else:
            self.load_wallet()

      
    def reset(self):
        if (self.show_private_key or self.wallet_unlocked):
            self.show_private_key = False  # hide private key if user re-enters wallet_manager
            self.render()
    
    def clear_frame(self):        
        for widgets in self.frame_1.winfo_children():
            widgets.destroy()
            
    def change_window(self,menu_state_index):
        self.menu_state_index = menu_state_index
        self.render()