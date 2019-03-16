import smtplib



def send_mail(meet_person,sent_person,date_meet):
	content = "this is for testing"



	mail = smtplib.SMTP('smtp.gmail.com',587)


	mail.starttls()


	mail.login('easymeet99@gmail.com','Vishnu123$')

	mail.sendmail('easymeet99@gmail.com',meet_person,content)

	mail.quit()
send_mail('17pa1a05g1@vishnu.edu.in','srikanth','13-02-2019')