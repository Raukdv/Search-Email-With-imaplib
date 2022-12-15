#Import your libs
import (
    imaplib,
    email
  )

#Use email as user and prefer setup App password with this system, avoid use your personal password for this.
user = ''
password = ''
imap_url = 'imap.gmail.com'

#this will get the body contend
def get_body(msg): 
    if msg.is_multipart(): 
        return get_body(msg.get_payload(0)) 
    else: 
        return msg.get_payload(None, True)
 
#This will get the info about the email recieved or send.
def get_email_info(msg):
    return email.message_from_bytes(msg)

#this will search for specific input, user or tag
#In this case use multi clauses for the searh, FROM, SUBJECT and SEEN or USEEN Clauses
def search(email, subject, is_seen, con):
    #formatting the "Clauses or Query for the sear"
    value = f'(FROM "{email}" SUBJECT "{subject}" {is_seen})'
    result, data = con.search(None, value) 
    return data
    
#this will get the emails in recieved order
def get_emails(result_bytes): 
    msgs = [] 
    for num in result_bytes[0].split(): 
        typ, data = con.fetch(num, '(RFC822)') 
        msgs.append(data) 
    return msgs 


#Setup connection and search by
con = imaplib.IMAP4_SSL(imap_url)  
con.login(user, password)  
con.select('Inbox') #Select the folder, in this case Inbox as main entry
#This work as normal search bar of gmail, you can check how to do a proper searching with the tags.
#For example, FROM its come from:email in the search bar.
#Now you can setup this for do it a multiples search
#For unreads and reads use is:unread or is:read, the tag "is" goes capital.
#For example: is:unread from:(raul@ramarketingconsulting.com) its how locks in searh bar from gmail

#In the next search function i prefer to setup multi clauses format, but indeed you can use single format with the next line in change of the current one.
#msgs = get_emails(search('FROM', 'email', con)) or msgs = get_emails(search('tag/clauses', 'value', con))


#For Multi Clause tag search
#Frist position: From another email.
#Second position: Subject content.
#Third position: SEEN or UNSEEN Email.
msgs = get_emails(search('email', 'New Job Opportunity!', 'SEEN', con))
#the function its for iterate the specific msgs as str and does not Parser
for msg in msgs[::-1]:
    for sent in msg: 
        if type(sent) is tuple: 
            content = str(sent[1], 'utf-8')  
            data = str(content) 
            
            try:
                #This for get the email itself more cleaning.
                indexstart = data.find("ltr") 
                data2 = data[indexstart + 5: len(data)]
                indexend = data2.find("</div>")

                #decode = email.message_from_string(data2[0: indexend])
                #print(decode) 
                print(data2[0: indexend])

            except UnicodeEncodeError as e:
                pass
              
#For do it Parser and more cleaning with a simple result.
#for msg in msgs[::-1]:
#    for sent in msg: 
#        if type(sent) is tuple: 
            #call ge_body function to get only body result
#            body_value = get_body(sent[1])

            #call get_email_info for get the email info, as date, to, from, subject.
 #           email_info_value = get_email_info(sent[1])
