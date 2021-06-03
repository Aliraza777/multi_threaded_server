from threading import Thread
import socket
import time
import pickle

SCHEME = "utf-8"
authorization = {}
user_resourses = {}

class CommonThread(Thread):
    def __init__(self,clientsocket):
        Thread.__init__(self)

        self.clientsocket = clientsocket

    def run(self):
        print("Client Thread Started ... ")
        choice = self.clientsocket.recv(1024)
        choice = choice.decode(SCHEME)
        if(choice == "1"):        
            self.addUser()
        elif(choice == "2"):
            self.verifyUser()
        elif(choice == "3"):
            self.authorizeUser()
        elif(choice == "4"):
            self.displayUsers()
        else:
            print("Error Encountered")
        self.clientsocket.close()

    def addUser(self):  
            #recieving the username and password
            username = self.clientsocket.recv(1024)
            password = self.clientsocket.recv(1024)
            username = username.decode(SCHEME)
            password = password.decode(SCHEME)

            #setting username and password 
            authorization[username] = password
            
            #printing the username and password from userlist
            print("Users List \n")
            for x , y in authorization.items():    
                print(" Username : ",x ,"\n" ,"password : ", y , "\n")
            
            #assigning resousrses to the user
            resourses = self.clientsocket.recv(4096)
            resourses_list = pickle.loads(resourses)
            
            user_resourses[username] = resourses_list
            print(user_resourses)
            
            self.clientsocket.send("User Added successfully \n".encode(SCHEME))
    def verifyUser(self):
            #getting the username and password from clients
            user_name = self.clientsocket.recv(1024)
            password = self.clientsocket.recv(1024)

            match = 0
            #decoding the username and password
            check_name = user_name.decode(SCHEME)
            check_pass = password.decode(SCHEME)

            #verifing from our dictionary 
            for users , val in authorization.items():
                if(users == check_name and val == check_pass):
                    match = match + 1 
            #if any match found then it will authenticate otherwise not.
            # print("Verifying Please Wait ... \n")
            # time.sleep(2)
            if(match != 0):
                self.clientsocket.send("Authorized User".encode(SCHEME))
            else:
                self.clientsocket.send("Unautherized User".encode(SCHEME))

    def authorizeUser(self):
            res = 0
            #reciving the username and resourse no.
            username = self.clientsocket.recv(1024)
            username = username.decode(SCHEME)
            resourse = self.clientsocket.recv(1024)
            resourse = resourse.decode(SCHEME)
            #assigning the resourse no
            if(resourse == "1"):
                res = 0
            elif(resourse == "2"):
                res = 1
            elif(resourse == "3"):
                res = 2
            else:
                print("Error")
            #checking resourse
            for user , val in user_resourses.items():
                print(user , val)
                if(user == username):   
                    if(val[res] == 1):
                        self.clientsocket.send("User has access to the Resourse".encode(SCHEME))    
                    else:
                        self.clientsocket.send("User does not have access to the Resourse".encode(SCHEME))
                        
            
            #if no matching user found
            # self.clientsocket.send("No User Found".encode(SCHEME))

    def displayUsers(self):
        data = pickle.dumps(authorization)
        self.clientsocket.send(data)
