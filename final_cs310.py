from datetime import datetime

homepage = '''
============================================================
{title}
============================================================
Config Area Parking                                    [1]
Add Car                                                [2]
Remove Car                                             [3]
Renew Expire                                           [4]
Expire Car                                             [5]
Check Car In Data                                      [6]
Show All Car                                           [7]
Exit Program                                           [8]
============================================================
'''.format(title="CAR PARKING MANAGEMENT SYSTEM".center(60))

m_cfg_areaparking = '''
============================================================
{title}
============================================================
'''.format(title="CONFIG AMOUNT AREA".center(60))

m_add_car = '''
============================================================
{title}
============================================================
'''.format(title="ADD CAR TO DATABASE".center(60))

m_del_car = '''
============================================================
{title}
============================================================
'''.format(title="DELETE CAR IN DATABASE".center(60))

m_renew = '''
============================================================
{title}
============================================================
'''.format(title="RENEW CAR".center(60))

m_expirecar = '''
============================================================
{title}
============================================================
'''.format(title="EXPIRE CAR IN DATABASE".center(60))

m_check_car_in_data = '''
============================================================
{title}
============================================================
'''.format(title="FIND DATA BY PLATE".center(60))

m_show_all_car = '''
============================================================
{title}
============================================================
'''.format(title="ALL CAR IN DATABASE".center(60))

m_program_exit = '''
============================================================
{title}
{title2}
============================================================
'''.format(title="PROGRAM EXIT".center(60), title2="Good Luck!".center(60))

# functions 
def selectandinput() :
    print(homepage, end = "")
    select = int(input("Enter menu : "))
    if select in [1, 2, 3, 4, 5, 6, 7, 8] :
        if select == 1 :
            print(m_cfg_areaparking)
            cfg = getdata("cfg_area")
            amt_park = getdata("all_car")
            print(f"Amout area : {cfg[0]} Parking : {len(amt_park)}")
            amt = int(input("Enter amout of area : "))
            cfg_areaparking(amt)
            return select
        elif select == 2 :
            cfg = getdata("cfg_area")
            amt_park = getdata("all_car")
            if len(amt_park) < int(cfg[0]) :
                name = input("Enter Firstname Lastname (Ex. Koo Kiddee): ")
                phone = input("Enter phone number (Ex. 0999999999): ")
                while not (phone.isdigit() and len(phone) == 10):
                    print("Please enter a 10-digit phone number.")
                    phone = input("Enter phone number (Ex. 0999999999): ")
                cartype = input("Enter brand car (Ex. Toyota or Brabus or BMW or etc.) : ")
                plate = input("Enter plate (Ex. RXT215) : ")
                province_plate = input("Enter province plate (Ex. Bangkok or Loei or etc.) : ")
                add_car(name, phone, cartype, plate, province_plate)
                add_expire(plate)
            else :
                print("Car Parking Full! | Please check expire car and remove.")
            return select
        elif select == 3 :
            print(m_del_car)
            plate = input("Enter plate to delete : ")
            status = del_car(plate)
            print("-"*60)
            print(status)
            print("-"*60)
            return select
        elif select == 4 :
            print(m_renew)
            plate = input("Enter plate to renew : ")
            status = renew(plate)
            print("-"*60)
            print(status)
            print("-"*60)
            return select
        elif select == 5 :
            print(m_expirecar)
            expire = get_expirecar() 
            print(f"{' Plate':<30} {'Expire Date':<20}")
            for i in expire :
                plate, exp = i.split()
                print(f" {plate:<30} {exp:<20}")
            print("-"*60)
            return select
        elif select == 6 :
            print(m_check_car_in_data)
            plate = input("Enter plate to find : ")
            ad = findcar_by_plate(plate)
            print("-"*60)
            if ad[4] == plate :
                print("Found car plate number", plate)
                print("Name :",ad[0], ad[1])
                print("Contact :",ad[2])
                print("Brand :",ad[3])
                print("Plate :",ad[4])
                print("Province Plate :",ad[5])
                print("Register date :",ad[6])
                print("Expire :",get_expiredate(plate))
                print("-"*60)
            else :
                print("Not found plate in database.")
            return select
        elif select == 7 :
            print(m_show_all_car)
            showalldata()
            return select
        elif select == 8 :
            print(m_program_exit)
            return select
    else :
        print("Invalid menu!!!")
    
def getdata(filename):
    with open(f'data/{filename}.txt', "r") as file1 :
        data = file1.readlines()
    return data

def cfg_areaparking(amt) :
    with open("data/cfg_area.txt", "w") as area :       
        area.write(f"{amt}")
        print("-"*60)
        print(f"Set amout area to {amt} success!")
        print("-"*60)

def add_car(owner_name, contact, cartype, plate, province_plate) :
    with open("data/all_car.txt", "a") as cars :       
        cars.write(f"{owner_name:<25} {contact:<12} {cartype:<15} {plate:<10} {province_plate:<15} {datetime.now().date()}\n")
        print("-"*60)
        print(f"Add car plate {plate} to database success!")
        print("-"*60)

def del_car(plate_to_del) :
    found_plate = False
    lines = getdata("all_car")
    update_line = []
    for line in lines:
        if plate_to_del in line:
            db_plate = line.split()
            if len(db_plate) > 4 and db_plate[4] == plate_to_del:
                found_plate = True
                print(f"Found plate: {plate_to_del}. Deleting...")
            else:
                update_line.append(line)
        else:
            update_line.append(line)

    if found_plate:
        with open("data/all_car.txt", 'w') as f2:
            f2.writelines(update_line)
        return f"Plate {plate_to_del} delete success!"
    else:
        return "Invalid plate! Please try again."

def renew(plate):
    found_plate = False  
    lines = getdata("date_expire")
    update_line = []
    for line in lines:
        if plate in line:
            db_plate = line.split()
            if db_plate[0] == plate:
                month = int(input("Enter the number of months to renew: "))
                date = datetime.now().date()  
                y = date.year
                m = date.month + month
                while m > 12: 
                    m -= 12
                    y += 1
                d = date.day 
                update_date = f"{plate:<10} {y}-{m:02d}-{d:02d}\n"
                update_line.append(update_date)
                found_plate = True 
            else:
                update_line.append(line)
        else:
            update_line.append(line)

    if found_plate:
        with open("data/date_expire.txt", 'w') as f2:
            f2.writelines(update_line)
        status = f"Plate {plate} renewed success for {month} months."
        return status
    else : 
        return "Invalid plate!"

def add_expire(plate):
    with open("data/date_expire.txt", "a") as cars:
        date = datetime.now()
        new_month = date.month + 1
        new_year = date.year
        if new_month > 12:
            new_month = 1
            new_year += 1
        new_date = datetime(new_year, new_month, date.day)
        cars.write(f"{plate:<10} {new_date.strftime('%Y-%m-%d')}\n")

def get_expirecar():
    expirecar = []
    lines = getdata("date_expire")
    current = datetime.now().date()
    for line in lines:
        plate, exp_date_str = line.split()
        expire_date = datetime.strptime(exp_date_str, '%Y-%m-%d').date()
        if expire_date < current:
            expirecar.append(f"{plate} {exp_date_str}")
    return expirecar

def get_expiredate(plate_find) :
    car_in_db = getdata("date_expire")  
    for line in car_in_db:
        if plate_find in line:
            date_exp = line.split()
            return date_exp[1]
    return "Not Found Plate"

def findcar_by_plate(plate_find):
    car_in_db = getdata("all_car")  
    for line in car_in_db:
        if plate_find in line:
            db_plate = line.split()
            return db_plate
    return "Not Found Plate"

def showalldata() :
    data = getdata("all_car")
    maxarea = getdata("cfg_area")
    print("\n" + "All User In Database".center(95, '='))
    print(f"\nAvailable parking lot : {len(data)} / {maxarea[0]}")
    print("="*95)
    print(f"\n{'Name':<25} {'Phone Number':<15} {'Brand car':<10} {'Plate':<10} {'Province plate':<15} {'Register date':<10}")
    for line in data:
        db_user = line.split()
        print(f"{db_user[0] + ' ' + db_user[1]:<25} {db_user[2]:<15} {db_user[3]:<10} {db_user[4]:<10} {db_user[5]:<15} {db_user[6]:<10}")
    print("="*95)

def centertext(text, amt):
    return f"{text.center(amt)}"



# main
user_select = 0
while user_select != 8 :
    user_select = selectandinput()
