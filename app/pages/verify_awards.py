from tkinter import Message, StringVar
import tkinter.messagebox
import customtkinter
import common.wallet
from common.preferences import font_type
import common.file_manager
import common.contracts
import common.txt_file_writer
from datetime import datetime


class PageVerifyAwards(customtkinter.CTkFrame):
    """
    Page Verify Awards
    """
    
    def __init__(self, parent, controller):
        customtkinter.CTkFrame.__init__(self, parent)
        self.controller = controller

        self.menu_state = {1: "Verify Awards"}
        self.menu_state_index = 1

        self.institution_contract = None

        self.img_back = controller.load_image(
            "/images/arrow-left-s-line.png", 20)

    

    #called when page is mounted
    def page_did_mount(self):
        self.frame_1 = customtkinter.CTkFrame(master=self,fg_color="#2a2d2e")
        self.frame_1.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.frame_1.grid_columnconfigure(0, weight=1) 
        
        self.render()

        
    #called when page is unmounted
    def page_did_unmount(self):               
        #clear widgets
        for widgets in self.winfo_children():
            widgets.destroy()

    def render_header(self): 
        title_text = self.menu_state[self.menu_state_index]
        self.title_label = customtkinter.CTkLabel(master=self.frame_1,  height=65,
                                            fg_color="#3E6E8C", text=title_text, text_font=(font_type, 20),corner_radius=5)
        self.title_label.grid(row=0,column=0,columnspan=1, padx=(20, 20), pady=10, sticky="ew" )

        if(self.menu_state_index != 1):
            self.btn_back = customtkinter.CTkButton(master=self.frame_1, image=self.img_back, text="", height=15,                                                    
                                                    command=lambda: self.button_menu_back())
            self.btn_back.grid(row=1, column=0, columnspan=1,  padx=(20, 20), pady=5, sticky="ew")
            
    
    def render(self):
        self.clear_frame()
        if (self.menu_state_index == 1):
            self.institutions_export = []
            self.verify_awards_menu_window()

    def button_menu_back(self):            
        self.render()
    

    def reset(self):
        pass

    def clear_frame(self):        
        for widgets in self.frame_1.winfo_children():
            widgets.destroy()

    def verify_awards_menu_window(self):
        #top header
        self.render_header()

        self.label_inst_contract = customtkinter.CTkLabel(master=self.frame_1,text="Institution's Contract", text_font=(font_type, 12))
        self.label_inst_contract.grid(row=2, column=0, columnspan=1,  sticky="we")
        self.entry_inst_contract = customtkinter.CTkEntry(master=self.frame_1,placeholder_text="Example: 0x1458E37f0D1A9e47CDF10e7635854bE6569c6878")
        self.entry_inst_contract.grid(row=3, column=0, columnspan=1, pady=5, padx=20, sticky="we")

        self.btn_add = customtkinter.CTkButton(master=self.frame_1, text="Add Institution Contract", command=lambda:self.add_institution())
        self.btn_add.grid(row=8, column=0, columnspan=1, padx=20, pady=10) 

        self.label_inst_added = customtkinter.CTkLabel(master=self.frame_1,text="Institution/s to Export", text_font=(font_type, 12))
        self.label_inst_added.grid(row=9, column=0, columnspan=1,  sticky="we")
        text = ','.join(self.institutions_export)        
        self.textbox_inst = customtkinter.CTkTextbox(master=self.frame_1, height=150)
        self.textbox_inst.insert(0.0,text)
        self.textbox_inst.grid(row=10, column=0, padx=20,pady=5, sticky="we")

        self.label_student_address = customtkinter.CTkLabel(master=self.frame_1,text="Student's Address", text_font=(font_type, 12))
        self.label_student_address.grid(row=12, column=0, columnspan=1,  sticky="we")       
        self.entry_student_address = customtkinter.CTkEntry(master=self.frame_1,placeholder_text="Example: 0xc4C0df2E5Eec444F3d23b301208B1b42a59Da5Bd")
        self.entry_student_address.grid(row=13, column=0, columnspan=1, pady=5, padx=20, sticky="we")

        self.label_message = customtkinter.CTkLabel(master=self.frame_1,text="Message", text_font=(font_type, 12))
        self.label_message.grid(row=15, column=0, columnspan=1,  sticky="we")       
        self.entry_message = customtkinter.CTkEntry(master=self.frame_1,placeholder_text="The student's message")
        self.entry_message.grid(row=16, column=0, columnspan=1, pady=5, padx=20, sticky="we")

        self.label_sig_hash = customtkinter.CTkLabel(master=self.frame_1,text="Signature Hash", text_font=(font_type, 12))
        self.label_sig_hash.grid(row=18, column=0, columnspan=1,  sticky="we")       
        self.entry_sig_hash = customtkinter.CTkEntry(master=self.frame_1,placeholder_text="The signature hash (signed message)")
        self.entry_sig_hash.grid(row=19, column=0, columnspan=1, pady=5, padx=20, sticky="we")

        self.btn_export = customtkinter.CTkButton(master=self.frame_1, text="Check signature & Export Awards", command=lambda:self.export_awards_by_verifier())
        self.btn_export.grid(row=21, column=0, columnspan=1, padx=20, pady=10) 


    def add_institution(self):
        if(self.entry_inst_contract.get() == ""):
            tkinter.messagebox.showwarning(title="Warning",message="You have to input the institution's contract")
        else:
            self.institutions_export.append(self.entry_inst_contract.get())
        self.verify_awards_menu_window()


    def export_awards_by_verifier(self):
        if(len(self.institutions_export) == 0):
            tkinter.messagebox.showerror(title="No Institutions",message="No contracts were added. Make sure that you add at least one institution's contract")
            return

        message = self.entry_message.get()        
        signed_message = self.entry_sig_hash.get()
        chain_id = common.wallet.get_chain_id()
        student_address = self.entry_student_address.get()

        institutions = []
        for institution_contract in self.institutions_export:           
            storage_address = common.contracts.get_storage_address(institution_contract)
            student_awards = common.contracts.get_student_awards(storage_address,student_address)

            data = { 
                 "student_address": student_address,
                 "student_awards":student_awards
            }          

            institution = {
                "contract":institution_contract,
                "students_awards":[data]               
            }

            institutions.append(institution)
    
        valid_signature = common.wallet.verify_signed_message(message,student_address,signed_message)

        if(valid_signature):        
            data = {
                "student_flag":True,
                "student_address": student_address,
                "message":message,
                "signed_message": signed_message,         
                "chain_id":chain_id,
                "institutions":institutions,
                "valid_signature":True
            }
            
            common.txt_file_writer.export_awards(data,file_name="txtAwardsVerified.txt")
            tkinter.messagebox.showinfo(title="Valid Signature",message="Valid Signature. File successfully exported")
        else:
            tkinter.messagebox.showerror(title="Invalid Signature",message="It looks like the signature was not generated by the inputted address")

    def change_window(self,menu_state_index):
        self.menu_state_index = menu_state_index
        self.render()
    


                                                      
                                                               
