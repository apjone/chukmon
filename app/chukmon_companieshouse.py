#!/usr/bin/env python3
import sys, os, sqlite3, datetime, requests as r, csv, codecs


from dotenv import load_dotenv

load_dotenv()
DB_FILE = os.getenv('DB_FILE')


def chukmon_chinfo():
    try:
        connection = sqlite3.connect(DB_FILE)
    except Exception as e:
        #print("Error:" + str(e))
        exit(1)
    c = connection.cursor()
    results = c.execute("select term from searchcompanies")
    terms = []

    for res in results:
        terms.append(res)

    for t in terms:
        term = t[0]
        #print("Getting:" + term)
        chresponse = r.get("https://find-and-update.company-information.service.gov.uk/advanced-search/download?companyNameIncludes=" + term)
        lines_iter = chresponse.iter_lines()
        data = csv.reader(codecs.iterdecode(lines_iter, encoding="utf-8"), delimiter=",")
        for index, row in enumerate(data):
            if row[0] != "company_name":
                print(row[0])
                companyname = row[0]
                company_number = row[1]
                company_status = row[2]
                company_type = row[3]
                company_subtype = row[4]
                dissolution_date = row[5]
                incorporation_date = row[6]
                removed_date = row[7]
                registered_date = row[8]
                nature_of_business = row[9]
                registered_office_address = row[10]
                #chuk_insertcompany(DB_FILE, companyname, company_number, company_status, company_type, company_subtype, dissolution_date, incorporation_date, removed_date, registered_date, nature_of_business, registered_office_address)
                sql = "insert or replace into companieshouse values(\"" + companyname+ "\",'" + company_number+ "','" + company_status+ "',\"" + company_type+ "\",'" + company_subtype+ "','" + dissolution_date+ "','" + incorporation_date+ "','" + removed_date+ "','" + registered_date+ "','" + nature_of_business+ "',\"" + registered_office_address +"\");"
                try:
                    c.execute(sql)
                except:
                    print("FAILED TO INSERET:" + sql)
    c = connection.cursor()
    now = datetime.datetime.now()
    c.execute("insert or replace into config values('last_refresh','" +  str(now) + "');")
    connection.commit()