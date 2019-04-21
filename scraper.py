import pandas as pd
import numpy as np

dept_list = [("ASIA", "ASIAN+STUDIES"), ("ASIA", "ASIAN+STUDIES+WITH+THESIS"),
             ("ATA", "ATATURK+INSTITUTE+FOR+MODERN+TURKISH+HISTORY"),
             ("AUTO", "AUTOMOTIVE+ENGINEERING"), ("BM", "BIOMEDICAL+ENGINEERING"),
             ("BIS", "BUSINESS+INFORMATION+SYSTEMS"),
             ("CHE", "CHEMICAL+ENGINEERING"), ("CHEM", "CHEMISTRY"), ("CE", "CIVIL+ENGINEERING"),
             ("COGS", "COGNITIVE+SCIENCE"),
             ("CSE", "COMPUTATIONAL+SCIENCE+%26+ENGINEERING"), ("CET", "COMPUTER+EDUCATION+%26+EDUCATIONAL+TECHNOLOGY"),
             ("CMPE", "COMPUTER+ENGINEERING"),
             ("INT", "CONFERENCE+INTERPRETING"), ("CEM", "CONSTRUCTION+ENGINEERING+AND+MANAGEMENT"),
             ("CCS", "CRITICAL+AND+CULTURAL+STUDIES"),
             ("EQE", "EARTHQUAKE+ENGINEERING"), ("EC", "ECONOMICS"), ("EF", "ECONOMICS+AND+FINANCE"),
             ("ED", "EDUCATIONAL+SCIENCES"),
             ("CET", " EDUCATIONAL+TECHNOLOGY"), ("EE", "ELECTRICAL+%26+ELECTRONICS+ENGINEERING"),
             ("ETM", "ENGINEERING+AND+TECHNOLOGY+MANAGEMENT"),
             ("ENV", "ENVIRONMENTAL+SCIENCES"), ("ENVT", "ENVIRONMENTAL+TECHNOLOGY"), ("XMB", "EXECUTIVE+MBA"),
             ("FE", "FINANCIAL+ENGINEERING"),
             ("PA", "FINE+ARTS"), ("FLED", "FOREIGN+LANGUAGE+EDUCATION"), ("GED", "GEODESY"), ("GPH", "GEOPHYSICS"),
             ("GUID", "GUIDANCE+%26+PSYCHOLOGICAL+COUNSELING"),
             ("HIST", "HISTORY"), ("HUM", "HUMANITIES+COURSES+COORDINATOR"), ("IE", "INDUSTRIAL+ENGINEERING"),
             ("INCT", "INTERNATIONAL+COMPETITION+AND+TRADE"),
             ("MIR", "INTERNATIONAL+RELATIONS%3aTURKEY%2cEUROPE+AND+THE+MIDDLE+EAST"),
             ("MIR", "INTERNATIONAL+RELATIONS%3aTURKEY%2cEUROPE+AND+THE+MIDDLE+EAST+WITH+THESIS"),
             ("INTT", "INTERNATIONAL+TRADE"), ("INTT", "INTERNATIONAL+TRADE+MANAGEMENT"), ("LS", "LEARNING+SCIENCES"),
             ("LING", "LINGUISTICS"),
             ("AD", "MANAGEMENT"), ("MIS", "MANAGEMENT+INFORMATION+SYSTEMS"), ("MATH", "MATHEMATICS"),
             ("SCED", "MATHEMATICS+AND+SCIENCE+EDUCATION"),
             ("ME", "MECHANICAL+ENGINEERING"), ("MECA", "MECHATRONICS+ENGINEERING"),
             ("BIO", "MOLECULAR+BIOLOGY+%26+GENETICS"), ("PHIL", "PHILOSOPHY"),
             ("PE", "PHYSICAL+EDUCATION"), ("PHYS", "PHYSICS"), ("POLS", "POLITICAL+SCIENCE%26INTERNATIONAL+RELATIONS"),
             ("PRED", "PRIMARY+EDUCATION"),
             ("PSY", "PSYCHOLOGY"), ("YADYOK", "SCHOOL+OF+FOREIGN+LANGUAGES"),
             ("SCED", "SECONDARY+SCHOOL+SCIENCE+AND+MATHEMATICS+EDUCATION"),
             ("SPL", "SOCIAL+POLICY+WITH+THESIS"), ("SOC", "SOCIOLOGY"), ("SWE", "SOFTWARE+ENGINEERING"),
             ("SWE", "SOFTWARE+ENGINEERING+WITH+THESIS"),
             ("TRM", "SUSTAINABLE+TOURISM+MANAGEMENT"), ("SCO", "SYSTEMS+%26+CONTROL+ENGINEERING"),
             ("TRM", "TOURISM+ADMINISTRATION"), ("WTR", "TRANSLATION"),
             ("TR", "TRANSLATION+AND+INTERPRETING+STUDIES"), ("TK", "TURKISH+COURSES+COORDINATOR"),
             ("LL", "WESTERN+LANGUAGES+%26+LITERATURES")]

n = 1998  # create the list for years and semesters
semesters = []
for i in range(20, 21):
    for a in range(1, 4):
        semesters += [(n, n + 1, a)]
    n += 1

semesters = semesters[:-1]
all_semesters_dicts = {}  # list that contains lists of department dictionaries of each semester


def create_dict_from_html(html_df):
    """
    Obtain the distinct course names from html table.
    Returns dictionary containing courses info and dept name.
    """
    dept_data = pd.DataFrame({'Code': html_df.iloc[:, 0],  # course code, course name, course instructor
                              'Name': html_df.iloc[:, 2],
                              'Instructor': html_df.iloc[:, 5]})

    return dept_data


for semester in semesters:

    this_semester_dicts = {}  # list that contains dictionaries of departments for 'this' semester

    for dept in dept_list:
        url = "https://registration.boun.edu.tr/scripts/sch.asp?donem={}/{}-{}&kisaadi={}&bolum={}".format(semester[0],
                                                                                                           semester[1],
                                                                                                           semester[2],
                                                                                                           dept[0],
                                                                                                           dept[1])
        try:
            data = pd.read_html(url)[3]
            data = data.loc[1:, :]
            deptData = create_dict_from_html(data)
            this_semester_dicts.update({dept: deptData})
        except ValueError:
            print("error")

    # aynı yıl farklı departmanlar burada birleştirilecek.

    all_semesters_dicts.update(this_semester_dicts)
    
print(all_semesters_dicts)
