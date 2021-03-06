import re
import operator
import csv

error = r"ERROR"
info = r"INFO"

file = open("syslog.log","r")
file2 = open("errorlogs.log","w+") # create a file for error logs
file3 = open("infologs.log","w+")  # create a file for info logs

for line in file:
    if re.search(error, line):
        file2.write(line)
    elif re.search(info, line):
        file3.write(line)
file.close()
file2.close()
file3.close()

file2 = open("C:\\Users\\Vansh Arora\\Desktop\\FinalProject\\errorlogs.log","r")

errorPattern = r"^.*(ERROR) (.*) (\(.*\))$"
errorDict = {}                      # Dictionary for error type and count
namepattern = r"^.*(\(.*\))$"   
userlogin_error = {}                # Dictionary for no. of errorlogs corresponding to a username

for line in file2:
    name = re.search(namepattern,line)
    userName = name[1][1:-1]
    if userName not in userlogin_error:
        userlogin_error[userName] = 1
    else:
        userlogin_error[userName] += 1

    errorSearch = re.search(errorPattern,line)
    error = errorSearch[2]
    if error not in errorDict:
        errorDict[error] = 1
    else:
        errorDict[error] += 1

file2.close()

file3 = open("infologs.log","r")

userlogin_info = {}

for line in file3:
    name = re.search(namepattern,line)
    userName = name[1][1:-1]
    if userName not in userlogin_info:
        userlogin2[userName]= 1
    else:
        userlogin_info[userName] += 1

file3.close()

# sort the error-count dictionary
errorDict = sorted(errorDict.items(), key = operator.itemgetter(1),reverse = True)

info_error = []               # list of dictionaries of error and info
for key in userlogin_error.keys():
    dic = {}
    dic["Username"] = key
    dic["ERROR"] = userlogin_error[key]
    if key in userlogin_info:
        dic["INFO"] = userlogin_info[key]
    else:
        dic["INFO"] = 0
    info_error.append(dic)

# Now add any user in list which is present in info-dictionary but not in error-dictionary
for key in userlogin_info.keys():
    if key not in userlogin_error:
        dic = {}
        dic["Username"] = key
        dic["ERROR"] = 0
        dic["INFO"] = userlogin_info[key]
        info_error.append(dic)

info_error = sorted(info_error, key = lambda i: i['Username'])

# Writting CSVs

# user_statistics
keys = ['Username','INFO','ERROR']
with open("user_statistics.csv", "w") as us:
    writer = csv.DictWriter(us, fieldnames = keys)
    writer.writeheader()
    writer.writerows(info_error)

# error_message
with open("error_message.csv",'w') as er:
    err_writer=csv.writer(er)
    err_writer.writerow(['Error','Count'])
    for row in errorDict:
        err_writer.writerow(row)