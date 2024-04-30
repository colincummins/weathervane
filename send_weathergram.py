def send_weathergram(to_address,quotation):

    import smtplib
    import wv_config

    smtp_object = smtplib.SMTP('smtp.gmail.com',587)

    smtp_object.ehlo()

    smtp_object.starttls()

    email = wv_config.gmail_address
    password = wv_config.gmail_token

    from_address = wv_config.gmail_address
    smtp_object.login(email,password)

    subject = 'Here is your Weathervane for today'
    message = str(quotation)
    msg = 'Subject: ' + subject + '\n' + message
    smtp_object.sendmail(from_address,to_address,msg)

    smtp_object.quit()