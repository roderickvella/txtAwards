from tkinter.filedialog import asksaveasfile, askopenfilename


def file_save(save_text, file_name, file_extension):
    f = asksaveasfile(mode='w', initialfile = file_name, defaultextension=file_extension)
    if f is None: #return `None` if dialog closed with "cancel".
        return False

    f.write(save_text)
    f.close()

    return True

def file_load():
    f = askopenfilename()
    if f is None:  #return `None` if dialog closed with "cancel".
        return False
    
    fr=open(f)
    data = fr.read()
    fr.close()

    return data



