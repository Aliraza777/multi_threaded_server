from commonthread import SCHEME
import socket
import pickle
import time

ADDRESS = "127.0.0.1"

PORT = 2222

c = socket.socket()

c.connect((ADDRESS,PORT))

print("Connected with server successfully \n")

print(" Press 1 to Add New User  \n Press 2 to verify User \n Press 3 to authenticate User  \n Press 4 to Display Users \n-----------------------------------\n")
choice = input("Enter Choice :  ")

if(choice == "1"):
    resourses = []
    #sending choice
    c.send(choice.encode(SCHEME))
    
    #adding new username and password and sending it to the server
    username = input("Enter Username :  ")
    password = input("Enter Password :  ")

    c.send(username.encode(SCHEME))
    c.send(password.encode(SCHEME))
    #setting resourses for the user
    print("please enter 1 for yes and 0 for no for resourses to use for the User")
    for i in range(3):
        print("for resourse R",i+1)
        resourse = int(input())
        resourses.append(resourse)
    data = pickle.dumps(resourses)
    c.send(data)
    
    #receiving the output from server
    data = c.recv(1024)
    print("From Server : " , data.decode(SCHEME))

elif(choice == "2"):
    c.send(choice.encode(SCHEME))
    
    username = input("Enter Username :  ")
    password = input("Enter Password :  ")

    c.send(username.encode(SCHEME))
    c.send(password.encode(SCHEME))
    
    #receiving the output from server
    data = c.recv(1024)
    print("From Server : " , data.decode(SCHEME))
elif(choice == "3"):
    c.send(choice.encode(SCHEME))
    username = input("Enter Username :  ")
    c.send(username.encode(SCHEME))
    resourse = input("Which resourse do you want to check \n  Enter R1 , R2 or R3 : ")
    if(resourse == "R1" or resourse == "r1"):
        res = 1
        c.send(str(res).encode(SCHEME))
    elif(resourse == "R2" or resourse == "r2"):
        res = 2
        c.send(str(res).encode(SCHEME))
    elif(resourse == "R3" or resourse == "r3"):
        res = 3
        c.send(str(res).encode(SCHEME))
    print("Searching please wait ... \n")
    time.sleep(2)
    data = c.recv(1024)
    print("From Server : " , data.decode(SCHEME))
elif(choice == "4"):
    c.send(choice.encode(SCHEME))

    data = c.recv(4096)
    data_list = pickle.loads(data)
    print(" ---- Users List --- \n")
    for users , val in data_list.items():
        print(" UserName = " , users , "\n" , "Password = " , val,  "\n")

else:
    print("Invalid choice")