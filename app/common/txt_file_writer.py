import json
from datetime import datetime
from tkinter.filedialog import askdirectory

def export_awards(data,file_name):
    folder_selected = askdirectory()
    filename = folder_selected + "/"+file_name
    with open(filename, "w") as f:
        art = '''        

  _        _      _                        _     
 | |___  _| |_   / \__      ____ _ _ __ __| |___ 
 | __\ \/ / __| / _ \ \ /\ / / _` | '__/ _` / __|
 | |_ >  <| |_ / ___ \ V  V / (_| | | | (_| \__ \\
  \__/_/\_\\\\__/_/   \_\_/\_/ \__,_|_|  \__,_|___/
              
                                                                              
        '''
        f.write(art)
        f.write("\n")

        if "student_flag" in data and data["student_flag"] is not None and data["student_flag"] == True:
            
            if "valid_signature" in data and data["valid_signature"] is not None:
                if(data["valid_signature"])==True:
                    f.write("Signature is Valid."+ "\n\n")
            else:
                f.write("To verify the below signature you can either make use of txtAwards or https://etherscan.io/verifiedSignatures"+ "\n\n")

            data_sig = {
                "Student Address": data["student_address"],
                "Message": data["message"],
                "Signature Hash": data["signed_message"]
            }

    
            data_json = json.dumps(data_sig, indent=4)
            f.write(data_json)

            f.write("\n\n")
            f.write("The following data was generated from ChainId: " + str(data["chain_id"]) + "\n\n")

            for institution in data["institutions"]:
                f.write("+" + "-" * 80 + "+\n\n")
                f.write("Institution's Contract: " + institution["contract"] + "\n")
                if "website" in institution and institution["website"] is not None:
                    f.write("Institution's Website: " + institution["website"] + "\n")
                
                f.write("\n")
                for student_awards in institution["students_awards"]:                  
                    for student_award in student_awards["student_awards"]:
                        award_title = student_award[0]
                        award_date = datetime.utcfromtimestamp(student_award[1]).strftime('%d/%m/%Y') 
                        f.write(" " *10 + "-Award Title: " + award_title + "\n")
                        f.write(" " * 10 + "-Award Date:  " + award_date + "\n")
                        f.write("\n")
                
                f.write("+" + "-" * 80 + "+\n")                
                f.write("\n\n")