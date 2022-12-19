#Connection lib
import imaplib 
#Email lib
import email

class EmailChecker():
    
    #Init constructor
    def __init__(self, **kwargs):
        #Constants
        self.imap_url = 'imap.gmail.com'
        #Variables have to be present in the inheritance
        self.user = kwargs.get('user', None)
        self.password = kwargs.get('password', None)
        self.tag = kwargs.get('tag', 'INBOX')
        
        #Perma-connection
        #Make sure the user info its given, else do nothing
        if self.user and self.password:
            self.connection = self.do_connection()
        else:
            self.connection = None
    
    #Do connection - this for try perma connection.
    def do_connection(self):
        con = imaplib.IMAP4_SSL(self.imap_url)  
        con.login(self.user, self.password)
        
        result, data = con.select(self.tag)
        alleged_amount = str(data[0], 'utf-8')
        print(f'The server response is: {result}')
        print(f'{alleged_amount} possible mailings for {self.tag} were found')
        return con
    
    def do_recent(self):
        result, data = self.connection.recent()
        print(f'The recent check is: {result}')
        return result
    
    def close_email(self):
        print("***SE HA CERRADO EL CORREO***")
        self.connection.close()
    
    def logout_email(self):
        print("***SE HA CERRADO LA SESION AL CORREO***")
        print(self.user)
        self.connection.logout()

    #this will get the body contend
    def get_body(self, msg): 
        if msg.is_multipart(): 
            return self.get_body(msg.get_payload(0)) 
        else: 
            return msg.get_payload(None, True) 

    def get_email_info(self, msg):
        return email.message_from_bytes(msg[1])

    #this will search for specific Clauses. In this case FROM email, Subject and SEEN or UNSEEN email.
    def search(self, email, subject, is_seen):
        if self.connection:
            #formatting the "Clauses or Query for the sear"
            value = f'(FROM "{email}" SUBJECT "{subject}" {is_seen})'
            result, data = self.connection.search(None, value) 
            return data
        else:
            return None
    
    #this will get the emails we want to find.
    def get_emails(self, result_bytes): 
        msgs = []
        
        if self.connection:
            for num in result_bytes[0].split(): 
                typ, data = self.connection.fetch(num, '(RFC822)') 
                msgs.append(data)
        
        print(f'*** {len(msgs)} emails were founds ***')
        return msgs
    
    def search_email(self, **kwargs):
        #For Multi Clause tag search
        #Frist position: From another email.
        #Second position: Subject content.
        #Third position: SEEN or UNSEEN Email.

        msgs = self.get_emails(
            self.search(
                kwargs.get('from_email', None), 
                kwargs.get('subject', None),
                kwargs.get('is_seen', 'SEEN')
                )
            )

        #return msgs with the initial values when you do the next cycle is for get the content in str and decode.
        for msg in msgs[::-1]:
            #This the decode part and you can get message_from_string
            for sent in msg: 
                if type(sent) is tuple: 
                    content = str(sent[1], 'utf-8')  
                    data = str(content)

                    decode = email.message_from_string(data)
                    print(decode['subject'])
            
                    #the next code is for getting the data as long str.
                    # try:
                    #     #This for get the email itself.
                    #     indexstart = data.find("ltr") 
                    #     data2 = data[indexstart + 5: len(data)]
                    #     indexend = data2.find("</div>")

                    #this code is for try it cleaning long str
                    #     #decode = email.message_from_string(data2[0: indexend])
                    #     print(data2[0: indexend])
                    #     #print(decode) 

                    # except UnicodeEncodeError as e:
                    #     pass

#tag is for labels in the email. Have to be given exactly as the name given in the account.
#Inbox and INBOX are the only exception for the upper and lower case. 
emailer = EmailChecker(user='user@gmail.com', password='app-password', tag='Inbox')
emailer.search_email(from_email='', subject=', is_seen='SEEN')
