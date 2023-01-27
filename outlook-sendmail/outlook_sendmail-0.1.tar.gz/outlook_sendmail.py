import win32com.client as win32

def send_mail(email_sender=None, email_recipient=None, email_subject=None, email_body_html=None, email_cc=None, attachment_pth=None, secret_mail=True):
    # Test if required input has been passed
    if None in (email_sender, email_recipient, email_body_html, email_subject):
        raise Exception("One or multiple required variables (sender, recipient, body, subject) are missing...")

    # E-Mail is supposed to be secret as default
    if secret_mail != False:
        email_subject = f"[secret] {email_subject}"

    outlook       = win32.Dispatch('outlook.application')
    mail          = outlook.CreateItem(0)

    # Body and subject
    mail.Subject  = email_subject
    mail.HTMLBody = email_body_html

    # To and CC
    mail.To       = email_recipient

    if isinstance(email_cc, str): 
        mail.CC = email_cc
    elif isinstance(email_cc, list): 
        mail.CC = ";".join(email_cc)

    # Add attachments
    if isinstance(attachment_pth, str): 
        try:
            f = open(attachment_pth)
            f.close()
            mail.Attachments.Add(attachment_pth)
        except FileNotFoundError:
            print('ERROR: E-Mail attachment "' + attachment_pth + '" does not exist. Redirecting E-Mail to "' + email_recipient + '" to sender.')
            mail.To = email_sender
            mail.CC =""
            mail.Subject = mail.Subject + " (NOT DELIVERED)"
    elif isinstance(attachment_pth, list): 
        for i in attachment_pth:
            try:
                f = open(i)
                f.close()
                mail.Attachments.Add(i)
            except FileNotFoundError:
                print('ERROR: E-Mail attachment "' + i + '" does not exist. Redirecting E-Mail to "' + email_recipient +'" to sender.')
                mail.To = email_sender
                mail.CC = ""
                mail.Subject = mail.Subject + " (NOT DELIVERED)"
    
    for account in outlook.Session.Accounts:
        if account.DisplayName == email_sender:
            mail._oleobj_.Invoke(*(64209, 0, 8, 0, account))
    
    # Send mail with Outlook
    mail.Send()