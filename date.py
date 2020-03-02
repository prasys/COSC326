import datetime
import sys
def get_date(s_date):
    date_patterns = ["%d/%m/%y", "%Y-%m-%d"]

    for pattern in date_patterns:
        try:
            return datetime.datetime.strptime(s_date, pattern).date()
        except:
            pass

    print ("Date is not in expected format: %s" %(s_date))


get_date("05/5/92")