import pandas as pd

dept_list = [("CMPE", "COMPUTER+ENGINEERING"), ("EC","ECONOMICS")...]   # Son seneye göre ders listesi
years = [(2016,2017,2), ... , (2018,2019,2)]

for year in years:
    for dept in dept_list:
        url = "https://registration.boun.edu.tr/scripts/sch.asp?donem={}/{}-{}&kisaadi={}&bolum={}".format(year[0], year[1], year[2], dept[0], dept[1])
        data = pd.read_html(url)[3]
        create_dict_from_html(data)

    #aynı yıl farklı departmanlar burada birleştirilecek.






def create_dict_from_html(html_df):
    """
    Obtain the distinct course names from html table.
    Returns dictionary containing courses info and dept name.
    """

    pass
