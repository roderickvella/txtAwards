import tkinter as tk
import tkinter.messagebox
import customtkinter
from PIL import Image, ImageTk
import os
from pages.receive_awards import PageReceiveAwards
from pages.wallet_manager import PageWalletManager
from pages.institution import PageInstitution
from pages.welcome_screen import PageWelcomeScreen
from pages.verify_awards import PageVerifyAwards
import common.wallet

PATH = os.path.dirname(os.path.realpath(__file__))

# Modes: "System" (standard), "Dark", "Light"
customtkinter.set_appearance_mode("Dark")
# Themes: "blue" (standard), "green", "dark-blue"
customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):
    """
    general setup
    """
    WIDTH = 1000
    HEIGHT = 720

    def __init__(self):

        super().__init__()

        self.title("txtAwards")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")

        # ============ create two frames ============

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=180,
                                                 corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # ============ frame_left ============

        # load images
        self.img_award_receiver = self.load_image("/images/user-line.png", 20)
        self.img_award_add = self.load_image("/images/award-add-line.png", 20)
        self.img_award_verify = self.load_image("/images/shield-check-line.png", 20)
        self.img_wallet = self.load_image("/images/wallet-3-line.png", 20)

        self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="txtAwards",
                                              text_font=("Roboto Medium", -25))  # font name and size in px

        self.button_1 = customtkinter.CTkButton(master=self.frame_left,
                                                image=self.img_wallet,
                                                text="Wallet",
                                                height=40,
                                                command=lambda: self.show_page(PageWalletManager))

        self.button_2 = customtkinter.CTkButton(master=self.frame_left,
                                                image=self.img_award_receiver,
                                                text="My Awards",
                                                height=40,
                                                command=lambda: self.show_page(PageReceiveAwards))

        self.button_3 = customtkinter.CTkButton(master=self.frame_left,
                                                image=self.img_award_add,
                                                text="Institution",
                                                height=40,
                                                command=lambda: self.show_page(PageInstitution))

        self.button_4 = customtkinter.CTkButton(master=self.frame_left,
                                                image=self.img_award_verify,
                                                text="Verify Awards",
                                                height=40,
                                                command=lambda:self.show_page(PageVerifyAwards))

        # configure grid layout (1x11)

        # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(0, minsize=10)
        # empty row as spacing
        self.frame_left.grid_rowconfigure(6, weight=1)

        self.label_1.grid(row=1, column=0, pady=10, padx=10)
        self.button_1.grid(row=2, column=0, pady=10, padx=20)
        self.button_2.grid(row=3, column=0, pady=10, padx=20)
        self.button_3.grid(row=4, column=0, pady=10, padx=20)
        self.button_4.grid(row=5, column=0, pady=10, padx=20)

        # ============ frame_right ============

        container = customtkinter.CTkFrame(self.frame_right)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.pages = {}

        for page_class in (PageWelcomeScreen, PageWalletManager, PageReceiveAwards,PageInstitution,PageVerifyAwards):

            page = page_class(container, self)
            self.pages[page_class] = page

            page.grid(row=0, column=0, sticky="nsew")
            page.grid_columnconfigure(0, weight=1)
            page.grid_rowconfigure(0, weight=1)

        self.current_page = None
        self.show_page(PageWelcomeScreen)

    def show_page(self, cont):
        """
        Put specific frame on top
        """
        if (self.current_page is not None):
            self.current_page.page_did_unmount()

        page = self.pages[cont]
        
        errorMessage =""
        if not common.wallet.wallet_unlocked() and type(page) in [PageReceiveAwards, PageInstitution]:
            page = self.pages[PageWelcomeScreen]
            errorMessage ="You have to unlock wallet!"
        
        if not common.wallet.is_connected_node and type(page) in [PageWalletManager, PageReceiveAwards, PageInstitution,PageVerifyAwards]:
            page = self.pages[PageWelcomeScreen]
            errorMessage ="You are not connected to a Node!"

        self.current_page = page
        page.page_did_mount()
        page.tkraise()
        
        if(errorMessage != ""): tkinter.messagebox.showerror(title="Error", message=errorMessage)


    def button_event(self):
        pass

    def load_image(self, path, size):
        """ load rectangular image with path relative to PATH """
        return ImageTk.PhotoImage(Image.open(PATH + path).resize((size, size)))



if __name__ == "__main__":
    app = App()
    app.mainloop()
