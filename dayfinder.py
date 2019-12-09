# delete your account with Enterprise Car Share
# dayfinderpy
date_one = [2015, 1, 4]
date_two = [2015, 1, 7]
months = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
def findDay(firstDate,secondDate,months):
        year_diff = secondDate[0] - firstDate[0]
        days = 0
        if(year_diff!=0):
            days = 365 * (year_diff - 1)
            if(firstDate[1]>secondDate[1]):
                for i in range(firstDate[1],12):
                    days = days + months[i]
                for i in range(1,secondDate[1]):
                    days = days + months[i]
                days = days + months[firstDate[1]]-firstDate[2] + secondDate[2]
            elif(firstDate[1]<secondDate[1]):
                days = days + 365
                if(firstDate[1]+1 < secondDate[1]-1):
                    for i in range(firstDate[1]+1,secondDate[1]-1):
                        days = days + months[i]
                        # print(i + "," + days)
                days = days + months[firstDate[1]]-firstDate[2] + secondDate[2]
            elif(firstDate[1]==secondDate[1]):
                days = days + 365 + secondDate[2]-firstDate[2]
        elif(year_diff==0):
            if(firstDate[1]<secondDate[1]):
                if(firstDate[1]+1 < secondDate[1]-1):
                    for i in range(firstDate[1]+1,secondDate[1]-1):
                        days = days + months[i]
                        # print(i + "," + days)
                days = days + months[firstDate[1]]-firstDate[2] + secondDate[2]
            elif(firstDate[1]==secondDate[1]):
                days = days + secondDate[2]-firstDate[2]
        return days
if (__name__ == '__main__'):
    which_day = findDay(date_one, date_two, months)
    print(which_day)