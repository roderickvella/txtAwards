from tkinter import Message, StringVar
import tkinter.messagebox
import customtkinter
import common.wallet
from common.preferences import font_type
import common.file_manager
import common.contracts
import common.txt_file_writer
import pages.transaction
import pages.header
import json
from datetime import datetime
import base64



class PageReceiveAwards(customtkinter.CTkFrame):
    """
    Page Receive Awards
    """
    
    def __init__(self, parent, controller):
        customtkinter.CTkFrame.__init__(self, parent)
        self.controller = controller

        self.menu_state = {1: "Awards", 2: "Sign Award",3:"Export Awards For Employer"}
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
            self.main_awards_menu_window()
        elif (self.menu_state_index == 2):
            self.sign_award_window()
        elif (self.menu_state_index == 3):
            self.export_awards_window()

       


    def button_menu_back(self):
        if(self.menu_state_index ==2):
            self.menu_state_index = 1
        elif(self.menu_state_index==3):
            self.menu_state_index = 1

            
        self.render()
    


    def reset(self):
        pass

    def clear_frame(self):        
        for widgets in self.frame_1.winfo_children():
            widgets.destroy()

    def main_awards_menu_window(self):
        #top header
        self.render_header()

        self.institutions_export = []
                
        # render main body
        customtkinter.CTkButton(master=self.frame_1, text="Sign Award", width=200, height=40,
                                                  corner_radius=10,
                                                   command=lambda:self.change_window(2)).grid(row=2, column=0, columnspan=1, padx=20, pady=10)

        customtkinter.CTkButton(master=self.frame_1, text="Export Awards For Employer", width=200, height=40,
                                                corner_radius=10,
                                                 command=lambda:self.change_window(3)).grid(row=3, column=0, columnspan=1, padx=20, pady=10)


    def sign_award_window(self):
        self.render_header()        
        award =json.loads(common.file_manager.file_load())
        
        self.label_student_address1 = customtkinter.CTkLabel(master=self.frame_1,text="Student Address", text_font=(font_type, 12))
        self.label_student_address1.grid(row=2, column=0, columnspan=1,  sticky="we")      
        self.label_student_address2 = customtkinter.CTkLabel(master=self.frame_1,text=award["student_address"])
        self.label_student_address2.grid(row=3, column=0, columnspan=1, pady=5, padx=20, sticky="we")

        self.label_award_title1 = customtkinter.CTkLabel(master=self.frame_1,text="Award Title", text_font=(font_type, 12))
        self.label_award_title1.grid(row=5, column=0, columnspan=1,  sticky="we")
        self.label_award_title2 = customtkinter.CTkLabel(master=self.frame_1,text=award["award_title"])
        self.label_award_title2.grid(row=6, column=0, columnspan=1, pady=5, padx=20, sticky="we")

        self.label_award_date1 = customtkinter.CTkLabel(master=self.frame_1,text="Award Date", text_font=(font_type, 12))
        self.label_award_date1.grid(row=8, column=0, columnspan=1,  sticky="we")
        award_date =  datetime.utcfromtimestamp(award["award_date"]).strftime('%d/%m/%Y')          
        self.label_award_date2 = customtkinter.CTkLabel(master=self.frame_1,text=award_date)
        self.label_award_date2.grid(row=9, column=0, columnspan=1, pady=5, padx=20, sticky="we")

        self.label_award_institution1 = customtkinter.CTkLabel(master=self.frame_1,text="Institution Address", text_font=(font_type, 12))
        self.label_award_institution1.grid(row=10, column=0, columnspan=1,  sticky="we")            
        self.label_award_institution2 = customtkinter.CTkLabel(master=self.frame_1,text=award["institution_contract"])
        self.label_award_institution2.grid(row=11, column=0, columnspan=1, pady=5, padx=20, sticky="we")

        self.btn_submit = customtkinter.CTkButton(master=self.frame_1, text="Sign Award", command=lambda:self.sign_award(award))
        self.btn_submit.grid(row=12, column=0, columnspan=1, padx=20, pady=10) 

    def sign_award(self,award):        
        signed_award = common.wallet.sign_award(award)      
        signed_awardb64= base64.b64encode(signed_award) 
        award["signed_data"] =signed_awardb64.decode('utf8')        
        data_json = json.dumps(award)
        common.file_manager.file_save(data_json,"signed-student-award-{0}".format(award["student_address"]),".json")
        tkinter.messagebox.showinfo(title="File Saved",message="Share file with institution to publish your award.")


    def export_awards_window(self):
        self.render_header()

        self.label_inst_contract = customtkinter.CTkLabel(master=self.frame_1,text="Institution's Contract", text_font=(font_type, 12))
        self.label_inst_contract.grid(row=2, column=0, columnspan=1,  sticky="we")
        self.entry_inst_contract = customtkinter.CTkEntry(master=self.frame_1,placeholder_text="Example: 0x1458E37f0D1A9e47CDF10e7635854bE6569c6878")
        self.entry_inst_contract.grid(row=3, column=0, columnspan=1, pady=5, padx=20, sticky="we")

        self.label_inst_website = customtkinter.CTkLabel(master=self.frame_1,text="Institution's Website", text_font=(font_type, 12))
        self.label_inst_website.grid(row=5, column=0, columnspan=1,  sticky="we")      
        self.entry_inst_website  = customtkinter.CTkEntry(master=self.frame_1,placeholder_text="Example: http://www.institution.com/")
        self.entry_inst_website.grid(row=6, column=0, columnspan=1, pady=5, padx=20, sticky="we")

        self.btn_add = customtkinter.CTkButton(master=self.frame_1, text="Step 1: Add Institution", command=lambda:self.add_institution())
        self.btn_add.grid(row=8, column=0, columnspan=1, padx=20, pady=10) 

        self.label_inst_added = customtkinter.CTkLabel(master=self.frame_1,text="Institution/s to Export", text_font=(font_type, 12))
        self.label_inst_added.grid(row=9, column=0, columnspan=1,  sticky="we")
        text =str(self.institutions_export).replace("[", "").replace("]", "").replace("{", "").replace("}", "")
        self.textbox_inst = customtkinter.CTkTextbox(master=self.frame_1, height=150)
        self.textbox_inst.insert(0.0,text)
        self.textbox_inst.grid(row=10, column=0, padx=20,pady=5, sticky="we")

        self.label_message = customtkinter.CTkLabel(master=self.frame_1,text="Message to Sign for Employer", text_font=(font_type, 12))
        self.label_message.grid(row=12, column=0, columnspan=1,  sticky="we")       
        self.entry_message_sign = customtkinter.CTkEntry(master=self.frame_1,placeholder_text="Example: My name is John Doe with ID Card:XXXXXX. I hereby declare that I am the owner of the listed awards.")
        self.entry_message_sign.grid(row=13, column=0, columnspan=1, pady=5, padx=20, sticky="we")

        self.btn_export = customtkinter.CTkButton(master=self.frame_1, text="Step 2: Export Awards", command=lambda:self.export_awards_by_student())
        self.btn_export.grid(row=15, column=0, columnspan=1, padx=20, pady=10) 

    def add_institution(self):
        if(self.entry_inst_contract.get() == "" or self.entry_inst_website.get() == ""):
            tkinter.messagebox.showwarning(title="Warning",message="You have to input the institution's contract and website")
        else:
            self.institutions_export.append({"Contract":self.entry_inst_contract.get(),"Website":self.entry_inst_website.get()})
        self.export_awards_window()

    def export_awards_by_student(self):
        message = self.entry_message_sign.get()
        signed_message = common.wallet.sign_message(message)
        chain_id = common.wallet.get_chain_id()
        student_address = common.wallet.get_address()

        institutions = []
        for institution in self.institutions_export:           
            institution_contract = institution["Contract"]
            institution_website = institution["Website"]
            storage_address = common.contracts.get_storage_address(institution_contract)
            student_awards = common.contracts.get_student_awards(storage_address,student_address)

            data = { 
                 "student_address": student_address,
                 "student_awards":student_awards
            }          

            institution = {
                "contract":institution_contract,
                "students_awards":[data],
                "website": institution_website
            }

            institutions.append(institution)
    
        data = {
            "student_flag":True,
            "student_address": student_address,
            "message":message,
            "signed_message": signed_message,         
            "chain_id":chain_id,
            "institutions":institutions
        }

        common.txt_file_writer.export_awards(data,file_name="txtAwards.txt")
        tkinter.messagebox.showinfo(title="File Saved",message="File successfully exported") 


    def change_window(self,menu_state_index):
        self.menu_state_index = menu_state_index
        self.render()
    


                                                      
                                                               
