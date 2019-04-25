import pandas as pd
import numpy as np
import time



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
             ("CET", "EDUCATIONAL+TECHNOLOGY"), ("EE", "ELECTRICAL+%26+ELECTRONICS+ENGINEERING"),
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
for i in range(21):
    for a in range(1, 4):
        semesters += [(n, n + 1, a)]
    n += 1

semesters = semesters[:-1]


start = time.time()


semesters = [(2017,2018,1),(2018,2019,1)]   # Just for two semester for now. We will iterate over the semesters.

all_courses = {}

for semester in semesters:
    for dept in dept_list:
        url = "https://registration.boun.edu.tr/scripts/sch.asp?donem={}/{}-{}&kisaadi={}&bolum={}".format(semester[0],
                                                                                                           semester[1],
                                                                                                           semester[2],
                                                                                                           dept[0],
                                                                                                           dept[1])

        try :
            data = pd.read_html(url)[3].iloc[1:,:]
        except ValueError:    # If table does not exist
            continue

        if dept not in all_courses:
            all_courses[dept] = {}
        for index, row in data.iterrows():    # Iterate over the rows of the dataframe read from html source code.
            try:
                course_code = row[0][:-3]     # Delete the section part. CMPE150.01 -> CMPE150
                if course_code in all_courses[dept]:
                    if semester not in all_courses[dept][course_code][2]:  ## BUG
                        all_courses[dept][course_code][2][semester] = [row[5]]
                else:
                    all_courses[dept][course_code] = [dept, row[2], {semester: [row[5]]}, {"total_offering":1}]
            except TypeError:       # If the course code is NaN, which means the row indicates Lab or Ps.
                continue



sorted_dept = sorted(all_courses.keys())


df = pd.DataFrame(columns=["Department/Program", "Course Code", "Course Name"])

for semester in semesters:
    semester_name = str(semester[0])+"-"+str(semester[2])
    df[semester_name] = []
df["total offerings"] = []

for dept in sorted_dept:
    current_course_list = all_courses[dept]
    sorted_courses = sorted(current_course_list.keys())
    new_row = {"Department/Program":dept[0] ,"Course Code":"U4 U2","Course Name":""}    ###

    for semester in semesters:
        semester_name = str(semester[0])+"-"+str(semester[2])
        new_row[semester_name] = course_statistics(dept, semester)            ###
    new_row["total offerings"] = course_statistics_total(dept)            ###
    df = df.append(new_row, ignore_index=True)

    for course_key in sorted_courses:
        course = current_course_list[course_key]
        for semester in course[2]:
            semester_name = str(semester[0])+"-"+str(semester[2])
            if len(df.loc[df["Course Code"] == course_key]) == 0:
                new_row = {"Department/Program":"" ,"Course Code":course_key,"Course Name":course[1]}
                new_row[semester_name] = "x"
                df = df.append(new_row, ignore_index=True)
            else:
                df.loc[df["Course Code"] == course_key, semester_name] = "x"

df.to_csv("output.csv")
print(df)


end = time.time()
print(end - start)



def course_statistics_total(dept):
    # semt_courses = {(2017,2018,1): {("CMPE", "COMPUTER+ENGINEERING"): {"CMPE150": [dept_name, coursename, semester, instructors]}} }
    """
    This function takes semt_courses dictionary and calculates grad, undergrad and distinct instructors for each semester and total offerings.
    """
    this_course_list = all_courses[dept]
    grad = 0
    undergrad = 0
    instr_num = 0
    instr_list = []
    for course_key in this_course_list:
        try:
            if int(course_key[-3]) > 4:
                grad += 1
            else:
                undergrad += 1
        except ValueError or TypeError:
            undergrad += 1 #buraya bak
        for semester in course_key[2]:
            instr_list.append(course_key[2][semester])
        instr_num = len(set(instr_list))

    answer = [grad, undergrad, instr_num]

    return answer
