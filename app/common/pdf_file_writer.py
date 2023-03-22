from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle,getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, Spacer,TableStyle
from tkinter.filedialog import askdirectory
from datetime import datetime


def export_awards(data):
    folder_selected = askdirectory()
    doc = SimpleDocTemplate(
            folder_selected+"/txtAwards.pdf",
            pagesize=A4,
            title="txtAwards-Institution Awards"
            )
    styles = getSampleStyleSheet()
  
    flowables = []
    spacer = Spacer(1, 0.5*inch)
    spacer2 = Spacer(1, 0.1*inch)
    spacer3 = Spacer(1, 0.05*inch)
    para_title1 = Paragraph("txtAwards", styles["Title"]) #or Heading1
    flowables.append(para_title1)
    flowables.append(spacer)

    para_title2 = Paragraph("ChainId:"+str(data["chain_id"]), styles["Heading3"]) 
    flowables.append(para_title2)
    flowables.append(spacer2)

    for institution in data["institutions"]:
        para_title3 = Paragraph("Institution's Contract: "+institution["contract"], styles["Heading3"]) 
        flowables.append(para_title3)

        flowables.append(spacer2)

        for student_awards in institution["students_awards"]:
            para_title4 = Paragraph("Student Address: "+student_awards["student_address"], styles["Heading3"]) 
            flowables.append(para_title4)

            for student_award in student_awards["student_awards"]:        
                styleN = styles["BodyText"]
                award_title = Paragraph(student_award[0], styleN)
                award_date = datetime.utcfromtimestamp(student_award[1]).strftime('%d/%m/%Y') 

                award_data = [
                            ["Award Title",award_title],
                            ["Award Date",award_date],
                        ]

                tblstyle = TableStyle([
                ('GRID', (0,0), (-1,-1), 1, colors.black),
                ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
                ('VALIGN',(0,0), (-1,-1),'TOP')
                    ])

                tbl = Table(award_data,colWidths=[100,340],hAlign="LEFT")
                tbl.setStyle(tblstyle)
                flowables.append(tbl)
                flowables.append(spacer3)

        flowables.append(spacer)

    doc.build(flowables)


