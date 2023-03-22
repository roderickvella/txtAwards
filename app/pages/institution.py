from tkinter import Message, StringVar
import tkinter.messagebox
import customtkinter
import common.wallet
from common.preferences import font_type
import common.file_manager
import common.contracts
import common.pdf_file_writer
import pages.transaction
import pages.header
import json
import base64
from datetime import datetime
import time




class PageInstitution(customtkinter.CTkFrame):
    """
    Institution Manager Page
    """
    
    def __init__(self, parent, controller):
        customtkinter.CTkFrame.__init__(self, parent)
        self.controller = controller

        self.menu_state = {1: "Institution", 2: "Create Institution", 3:"Load Institution",4:"Institution Awards",5:"Create Award for Student",6:"Publish Award for Student",7:"Export Published Awards"}
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
            self.main_institition_menu_window()
        elif(self.menu_state_index ==2):
            self.create_institution_window()
        elif (self.menu_state_index ==3):
            self.load_institution_window()
        elif(self.menu_state_index ==4):
            self.institution_award_window()
        elif(self.menu_state_index ==5):
            self.create_award_window()
        elif(self.menu_state_index ==6):
            self.publish_award_window()
        elif(self.menu_state_index ==7):
            self.export_published_window()


    def button_menu_back(self):
        if(self.menu_state_index ==2):
            self.menu_state_index = 1
        elif(self.menu_state_index==3):
            self.menu_state_index = 1
        elif(self.menu_state_index==4):
             self.menu_state_index = 3
        elif(self.menu_state_index==5):
            self.menu_state_index = 4
        elif(self.menu_state_index ==6):
            self.menu_state_index = 4
        elif(self.menu_state_index ==7):
            self.menu_state_index = 4
            
        self.render()
    


    def reset(self):
        pass

    def clear_frame(self):        
        for widgets in self.frame_1.winfo_children():
            widgets.destroy()

    def main_institition_menu_window(self):
        #top header
        self.render_header()
                
        # render main body
        customtkinter.CTkButton(master=self.frame_1, text="Create Institution", width=200, height=40,
                                                  corner_radius=10,
                                                   command=lambda:self.change_window(2)).grid(row=2, column=0, columnspan=1, padx=20, pady=10)

        customtkinter.CTkButton(master=self.frame_1, text="Load Institution", width=200, height=40,
                                                corner_radius=10,
                                                 command=lambda:self.change_window(3)).grid(row=3, column=0, columnspan=1, padx=20, pady=10)
            
    def change_window(self,menu_state_index):
        self.menu_state_index = menu_state_index
        self.render()
    
    def create_institution_window(self):      
        self.render_header()
        self.btn_create_txn = customtkinter.CTkButton(master=self.frame_1, text="Create", width=200, height=40,
                                                  corner_radius=10,
                                                  command=lambda:self.create_institution())
        self.btn_create_txn.grid(row=2, column=0, columnspan=1, padx=20, pady=10)
        
   

    def load_institution_window(self):
        self.render_header()

        self.entry_inst_contract = customtkinter.CTkEntry(master=self.frame_1, placeholder_text="Enter Institution Contract Address")  
        self.entry_inst_contract.grid(row=4, column=0, columnspan=1, pady=20, padx=20, sticky="we")  

        self.btn_load = customtkinter.CTkButton(master=self.frame_1, text="Submit", width=200, height=40,
                                                  corner_radius=10,
                                                  command=lambda:self.load_institution_contract())
        self.btn_load.grid(row=5, column=0, columnspan=1, padx=20, pady=10) 

    
    
    def load_institution_contract(self):
        self.institution_contract = self.entry_inst_contract.get()
        self.change_window(4)

    def institution_award_window(self):
        self.render_header()

        self.label_title = customtkinter.CTkLabel(master=self.frame_1,
                                                      text="Contract - {0}".format(self.institution_contract), text_color="#92c0d3", text_font=(font_type, 15))
        self.label_title.grid(row=2, column=0, columnspan=1, pady=20, padx=20, sticky="we")

        self.btn_create_award = customtkinter.CTkButton(master=self.frame_1, text="Create Award for Student", width=200, height=40,
                                                  corner_radius=10,
                                                  command=lambda:self.change_window(5))
        self.btn_create_award.grid(row=3, column=0, columnspan=1, padx=20, pady=10) 

        self.btn_publish_award = customtkinter.CTkButton(master=self.frame_1, text="Publish Student Award", width=200, height=40,
                                                  corner_radius=10,
                                                  command=lambda:self.change_window(6))
        self.btn_publish_award.grid(row=4, column=0, columnspan=1, padx=20, pady=10) 

        self.btn_publish_award = customtkinter.CTkButton(master=self.frame_1, text="Export Published Awards", width=200, height=40,
                                                  corner_radius=10,
                                                  command=lambda:self.change_window(7))
        self.btn_publish_award.grid(row=5, column=0, columnspan=1, padx=20, pady=10) 

    def create_award_window(self):
        self.render_header()
        self.label_student_address = customtkinter.CTkLabel(master=self.frame_1,text="Student Address")
        self.label_student_address.grid(row=2, column=0, columnspan=1,  sticky="we")

        student_address = StringVar()
        self.entry_student_address = customtkinter.CTkEntry(master=self.frame_1,textvariable=student_address)
        self.entry_student_address.grid(row=3, column=0, columnspan=1, pady=5, padx=20, sticky="we")

        self.label_award_title = customtkinter.CTkLabel(master=self.frame_1,text="Award Title")
        self.label_award_title.grid(row=5, column=0, columnspan=1,  sticky="we")

        award_title = StringVar()
        self.entry_award_title = customtkinter.CTkEntry(master=self.frame_1,textvariable=award_title)
        self.entry_award_title.grid(row=6, column=0, columnspan=1, pady=5, padx=20, sticky="we")

        self.label_award_date = customtkinter.CTkLabel(master=self.frame_1,text="Award Date")
        self.label_award_date.grid(row=8, column=0, columnspan=1,  sticky="we")
        
        award_date = StringVar()                 
        award_date.set(datetime.now().strftime("%d/%m/%Y"))
        self.entry_award_date = customtkinter.CTkEntry(master=self.frame_1,textvariable=award_date)
        self.entry_award_date.grid(row=9, column=0, columnspan=1, pady=5, padx=20, sticky="we")

        self.btn_submit = customtkinter.CTkButton(master=self.frame_1, text="Create File for Signing", command=lambda:self.create_award_for_signing())
        self.btn_submit.grid(row=11, column=0, columnspan=1, padx=20, pady=10) 

    def create_award_for_signing(self):
        #the file must contain the following data for signing: awardTitle,awardDate,nonce_sign,chainid,tx_receipt.contractAddress     
        student_address = common.wallet.get_checksum_address(self.entry_student_address.get())     
        award_date_unix = int(time.time())
        data = {
            "award_title": self.entry_award_title.get(),
            "award_date": award_date_unix,
            "student_address": student_address,
            "institution_contract":self.institution_contract,
            "nonce_award_student":common.contracts.get_nonce_award_student(self.institution_contract,student_address),
            "chain_id": common.wallet.get_chain_id(),
            "signed_data":None
        }

        data_json = json.dumps(data)
        common.file_manager.file_save(data_json,"student-award-{0}".format(student_address),".json")
        tkinter.messagebox.showinfo(title="File Saved",message="Share file with student. Student has to sign award.")

    
    def publish_award_window(self):
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

        self.btn_publish_txn = customtkinter.CTkButton(master=self.frame_1, text="Publish Award", width=200, height=40,
                                            corner_radius=10,
                                            command=lambda:self.publish_award(award))
        self.btn_publish_txn.grid(row=11, column=0, columnspan=1, padx=20, pady=10)


    def publish_award(self,award):
        signed_data = award["signed_data"].encode('utf8')
        signed_data = base64.b64decode(signed_data)
        award["signed_data"] = signed_data
    
        pages.transaction.TransactionWindow(self,common.wallet.TransactionType.Publish_Award,data=award)
        
    def export_published_window(self):
        self.render_header()
        self.btn_export = customtkinter.CTkButton(master=self.frame_1, text="Export", width=200, height=40,
                                            corner_radius=10,
                                            command=lambda:self.export_published_awards())
        self.btn_export.grid(row=2, column=0, columnspan=1, padx=20, pady=10)   

    def export_published_awards(self):
        storage_address = common.contracts.get_storage_address(self.institution_contract)
        students = common.contracts.get_all_students(storage_address)
        chain_id = common.wallet.get_chain_id()
        
        students_awards = []
        for student in students:
            student_awards = common.contracts.get_student_awards(storage_address,student)
            data = { 
                 "student_address": student,
                 "student_awards":student_awards
            }
            students_awards.append(data)
        
        institution = {
            "contract":self.institution_contract,
            "students_awards":students_awards
        }

        data = {            
            "chain_id":chain_id,
            "institutions":[institution]
        }

        common.pdf_file_writer.export_awards(data)
        tkinter.messagebox.showinfo(title="File Saved",message="Succesfully exported to file.")


    def create_institution(self):       
        #open transaction window
        pages.transaction.TransactionWindow(self,common.wallet.TransactionType.Deploy_Institution_Contract)
    


    #automatically called from transaction window, when transaction is processed succesfully
    def callback_from_txn_window(self,txn_receipt,txn_type):
        if(txn_type == common.wallet.TransactionType.Deploy_Institution_Contract):         
            self.btn_create_txn.destroy()
            self.label_title = customtkinter.CTkLabel(master=self.frame_1,
                                                      text="New Institution Contract", text_color="#92c0d3", text_font=(font_type, 12))
            self.label_title.grid(row=2, column=0, columnspan=1, pady=20, padx=20, sticky="we")

            self.label_subtitle= customtkinter.CTkLabel(master=self.frame_1,
                                                      text="Make sure you save your institution contract address for future use.", text_color="#92c0d3", text_font=(font_type, 11))

            self.label_subtitle.grid(row=3, column=0, columnspan=1, pady=20, padx=20, sticky="we")

            message = StringVar()
            message.set("Contract address: {0}".format(txn_receipt.contractAddress))
            self.entry_inst_contract = customtkinter.CTkEntry(master=self.frame_1, textvariable=message)  
            self.entry_inst_contract.grid(row=4, column=0, columnspan=1, pady=20, padx=20, sticky="we")
        elif(txn_type == common.wallet.TransactionType.Publish_Award)                                                        :
            tkinter.messagebox.showinfo(title="Award Publish",message="Award was successfully published!")
            self.change_window(4)
            

      
      
