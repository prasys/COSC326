import re 
import fileinput

def preprocessemail(email):
    # print(email)
    if ' ' in email:
        return -1
    email = email.strip()
    email = email.lower()
    email = email.replace("_at_",'@')
    # email = email.replace("_dot_",'.')
    email = domainExtensionFixer(email)
    mymatch = re.search(r'^\w+([\.-]?\w+)*@', email)
    if mymatch:
        return email
    else:
        if email.find('@') is not -1:
            return -2 # @ is not found
        else:
            return -1 # mailbox name error 

    return email



def domainExtensionFixer(email):
    results = email.count('@')
    if results is 1: #great there is only one instance , now we will find the index and get it replace
        indexForReplace = email.index('@')
        list_of_stuff = email.split('@')

        if list_of_stuff[1].find("_dot_co") is not -1:
            fixedDomain = list_of_stuff[1].replace("_dot_co",".co")
            email = list_of_stuff[0] + "@" + fixedDomain
            return email
        if list_of_stuff[1].find("_dot_com") is not -1:
            fixedDomain = list_of_stuff[1].replace("_dot_co",".co")
            email = list_of_stuff[0] + "@" + fixedDomain
            return email
        
        return email
    else:
        return email
    # print(email.find('@'))
    # email = email.replace("_dot_co",'.co')
    # email = email.replace("_dot_com",'.com')


def find_ip(str):
    str = str.strip()
    mymatch = re.search(r'\[(.*?)\]$', str) #check do we have ip or not
    if mymatch:
        str = mymatch.group(1)
    else:
        return -1
    ip_pattern = re.compile('(?:^|\b(?<!\.))(?:1?\d?\d|2[0-4]\d|25[0-5])(?:\.(?:1?\d?\d|2[0-4]\d|25[0-5])){3}(?=$|[^\w.])') # need to strengthen the regex here / check the 255.255.255.0
    ip = re.findall(ip_pattern, str)
    if ip:
        return ip
    else:
        return -2 #well we did not get the IP address

def checkDomainName(str):
    str = str.lower()
    mymatch = re.search(r'^(\S+)@(\S+)', str)
    if mymatch:
        str = mymatch.group(2)
        str = str.split('@')[0]
    else:
        return -1 #forget about it , the email address is not even valid - this shouldn't even happen in the first place , the earlier one takes care of it
    
    if str.find('co.nz') is not -1: 
        return 1
    elif str.find('com.au') is not -1:
        return 1
    elif str.find('co.ca') is not -1:
        return 1
    elif str.find('.com') is not -1:
        if str.endswith('.com'):
            return 1
        else:
            return -1
    elif str.find('co.us') is not -1:
        return 1
    elif str.find('co.uk') is not -1:
        return 1
    else:
        return -1


def processEverything(email):
    processedResult = preprocessemail(email)
    if processedResult is -1:
        print(email.strip() + " <- " + "Missing @ symbol")
        return -1
    if processedResult is -2:
        print(email.strip() + " <- " + "Invalid extension")
        return -1
    if find_ip(processedResult) is -1: # that means likely we have a domain name - we are not sure , it could also mean that we have a crap IP
        if checkDomainName(processedResult) is -1: # if it is not
             print(email.strip() + " <- " + "Invalid extension")
             return -1
        else:
            if finalCheck(processedResult) is 0:
                print(processedResult.strip())
                return 0
            else:
                print(email.strip() + " <- " + "Invalid extension")
                return -1
    elif find_ip(processedResult) is -2:
        print(email.strip() + " <- " + "Invalid extension")
        return -1
    else:
        print(processedResult.strip())
        return 0

      
def finalCheck(email): # final check our email against the https://emailregex.com/ which claims 99.99% it works - so it better worK
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'  
    if(re.search(regex,email)):  
        return 0 
    else:  
        return -1

if __name__== "__main__":
    for line in fileinput.input():
        processEverything(line)
