import customtkinter
def render_header(self, controller,title_text):   
    self.title_label = customtkinter.CTkLabel(master=self.frame_1,  height=65,
                                        fg_color="#336B5D", text=title_text, text_font=("Roboto Medium", 20),corner_radius=5)
    self.title_label.grid(row=0,column=0,columnspan=1, padx=(20, 20), pady=10, sticky="ew" )

    self.btn_back = customtkinter.CTkButton(master=self.frame_1, image=self.img_back, text="", width=20, height=30,
                                            corner_radius=0, fg_color="#336B5D", hover_color="#2D6154", 
                                            command=lambda: controller.show_back_menu())
    self.btn_back.grid(row=0, column=0, columnspan=1,  padx=(30, 0), pady=10, sticky="W")

    