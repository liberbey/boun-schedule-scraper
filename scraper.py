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

semt_courses = {}
for semester in semesters:
    dept_courses = {}
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

        courses = {}
        for index, row in data.iterrows():    # Iterate over the rows of the dataframe read from html source code.
            try:
                course_code = row[0][:-3]     # Delete the section part. CMPE150.01 -> CMPE150
                if course_code in courses:
                    if row[5] not in courses[course_code][3]:
                        courses[course_code][3].append(row[5])    # Add the distinct instructor.
                else:
                    courses[course_code] = [dept, row[2], semester, [row[5]]]
            except TypeError:       # If the course code is NaN, which means the row indicates Lab or Ps.
                continue
        dept_courses[dept] = courses
    semt_courses[semester] = dept_courses


end = time.time()
print(end - start)

df = pd.DataFrame(columns=["Department/Program", "Course Code", "Course Name"])

for semester in semesters:
    semester_name = str(semester[0])+"-"+str(semester[2])
    df[semester_name] = []
df["total offerings"] = []

for semester in semt_courses:
    current_semester = semt_courses[semester]

    for dept in current_semester:
        current_course_list = current_semester[dept]
        new_row = {"Department/Program":dept[0] ,"Course Code":"U4 U2","Course Name":""}

        for semester in semesters:
            semester_name = str(semester[0])+"-"+str(semester[2])
            new_row[semester_name] = "U1 G1"

        new_row["total offerings"] = "U2 G2"
        df = df.append(new_row, ignore_index=True)

        for course_key in current_course_list:
            course = current_course_list[course_key]
            semester_name = str(course[2][0])+"-"+str(course[2][2])
            if len(df.loc[df["Course Code"] == course_key]) == 0:
                new_row = {"Department/Program":"" ,"Course Code":course_key,"Course Name":course[1]}
                new_row[semester_name] = "x"
                df = df.append(new_row, ignore_index=True)
            else:
                df.loc[df["Course Code"] == course_key, semester_name] = "x"

df.to_csv("output.csv")
print(df)





def course_statistics(semt_courses):
    # semt_courses = {(2017,2018,1): {("CMPE", "COMPUTER+ENGINEERING"): {"CMPE150": [dept_name, coursename, semester, instructors]}} }
    """
    This function takes semt_courses dictionary and calculates grad, undergrad and distinct instructors for each semester.
    """
    pass
