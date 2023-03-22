from tkinter import *
from tkinter import messagebox
from tkinter.tix import COLUMN
from common.preferences import font_type
import threading
import time
import customtkinter
import common.wallet
import pages.progress_bar

class TransactionWindow(customtkinter.CTkToplevel):
     
    def __init__(self, master,transaction_type,**kwargs):         
        super().__init__(master = master)
        self.master = master
        #close window if wallet is not unlocked
        if(not common.wallet.wallet_unlocked()):
            messagebox.showerror('Transaction Error', 'Error: Wallet is not unlocked')
            self.destroy()
            return

        self.transaction_type = transaction_type
        self.data = kwargs.get('data', None)

        self.title("Transaction")
        self.geometry("500x500") 
        self.grab_set() #make popup only active

        self.frame_1 = customtkinter.CTkFrame(self)
        self.frame_1.pack(pady=20, padx=30, fill="both", expand=True)
        
        self.load("Standard")  

        
    


    def load(self,gas_fee_priority):        
        pages.progress_bar.pb_setup(self)
        self.t1 = threading.Thread(target=lambda:pages.progress_bar.pb_animation(self))
        self.t2 = threading.Thread(target=lambda:self.render_widgets(gas_fee_priority))

        self.t1.start()
        self.t2.start()
        


    def render_widgets(self,gas_fee_priority):
    
        #b.grab_release() # to return to normal
        data = common.wallet.build_transaction(gas_fee_priority.lower(),self.transaction_type,data=self.data)
        estimate_gas_fee = data["total_gas_fee"]
        unsigned_txn = data["unsigned_txn"]
               
        label_title = customtkinter.CTkLabel(master=self.frame_1, text=common.wallet.get_transaction_title(self.transaction_type), text_font=(font_type, 15))
    
        label_select_gas_fee =customtkinter.CTkLabel(master=self.frame_1, text="Select Gas Fee", text_font=(font_type, 13),anchor="w")
      
        option_gas_menu_var = customtkinter.StringVar(value=gas_fee_priority)  # set initial value
        self.option_gas = customtkinter.CTkOptionMenu(master=self.frame_1, values=["Safe Low", "Standard", "Fast"], command=self.option_gas_selection_event,variable=option_gas_menu_var)
        
        
        
        label_gas_fees =customtkinter.CTkLabel(master=self.frame_1, text="Estimated Gas Fee", text_font=(font_type, 13),anchor="w")
        label_gas_value =customtkinter.CTkLabel(master=self.frame_1, text=str(estimate_gas_fee) +" Matic", anchor="w")

        self.btn_submit = customtkinter.CTkButton(master=self.frame_1,  text="Submit", command=lambda: self.button_submit_transaction(unsigned_txn))

        self.frame_1.columnconfigure(0, weight=1)
        label_title.grid(row=0, pady=5, sticky="ew")

        label_select_gas_fee.grid(row=2,column=0, padx=5, pady = 4,sticky="w")
        self.option_gas.grid(row=3, column=0, padx=15, pady = 2,sticky="w")

        label_gas_fees.grid(row=4,column=0, padx=5, pady = 4,sticky="w")
        label_gas_value.grid(row=5, column=0, padx=15, pady = 2,sticky="w")

        self.btn_submit.grid(row=6,column=0, padx=15, pady = 2,sticky="w")

        #remove loading widget       
        pages.progress_bar.pb_hide(self)
     

    def clear_frame(self):
        for widgets in self.frame_1.winfo_children():
            widgets.destroy()

    def option_gas_selection_event(self,choice):
        self.clear_frame()
        #we have to re-build transaction on change
        self.load(choice)
    
    def add_widget_txn_hash(self,txn_hash_hex):
        data_txn_hash = StringVar()
        data_txn_hash.set(txn_hash_hex)

        label_txn_hash =customtkinter.CTkLabel(master=self.frame_1, text="Transaction Hash", text_font=(font_type, 13),anchor="w")
        entry_txn_hash = customtkinter.CTkEntry(master=self.frame_1,textvariable=data_txn_hash,width=400)

        label_txn_hash.grid(row=7,column=0, padx=5, pady = 4,sticky="w")
        entry_txn_hash.grid(row=8, column=0, padx=15, pady = 2,sticky="w")

    def add_widget_contract_address(self,contractAddress):
        data_contract_address = StringVar()
        data_contract_address.set(contractAddress)
        
        label_contract =customtkinter.CTkLabel(master=self.frame_1, text="Contract Address", text_font=(font_type, 13),anchor="w")
        entry_contract = customtkinter.CTkEntry(master=self.frame_1,textvariable=data_contract_address,width=400)

        label_contract.grid(row=9,column=0, padx=5, pady = 4,sticky="w")
        entry_contract.grid(row=10, column=0, padx=15, pady = 2,sticky="w")

    def add_widget_bottom_message(self,message):
        self.label_message =customtkinter.CTkLabel(master=self.frame_1, text=message, fg_color="#FF0000",width=400, text_font=(font_type, 11),anchor="w")
        self.label_message.grid(row=12,column=0, padx=10, pady = 10,sticky="w")

    def send_transaction(self,built_txn):
        self.add_widget_bottom_message("Processing Transaction. Do not close this window.") 

        #send transaction on blockchain
        tx_hash_data = common.wallet.sign_sendtransaction(built_txn)

        self.add_widget_txn_hash(tx_hash_data["hex_txn_hash"])
        #wait for transaction to complete 
        tx_receipt =common.wallet.get_transaction_receipt(tx_hash_data["txn_hash"])
       
        contract_address = tx_receipt.contractAddress if tx_receipt.contractAddress is not None else tx_receipt.to
        self.add_widget_contract_address(contract_address)

        #remove loading widget       
        pages.progress_bar.pb_hide(self)        

        self.add_widget_bottom_message("Transaction Complete. You can close this window.") 

        #inform master window that transaction was succesfully executed
        self.master.callback_from_txn_window(tx_receipt,self.transaction_type)

   
    def button_submit_transaction(self,built_txn):
        #disable submit button & gas dropdown
        self.btn_submit.configure(state=DISABLED)
        self.option_gas.configure(state=DISABLED)

        #setup progress bar
        pages.progress_bar.pb_setup(self)
        
        #create threads
        self.t1 = threading.Thread(target=lambda:pages.progress_bar.pb_animation(self))
        self.t2 = threading.Thread(target=lambda:self.send_transaction(built_txn))

        #start threads
        self.t1.start()
        self.t2.start()
        
        