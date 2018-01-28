from smtplib import SMTP_SSL


#stand in user interface
to_addr = input("pay to: ")
msg = input("message: ")


server = SMTP_SSL("smtp.gmail.com", 465)

server.login("jmdelaney8@gmail.com", "klcfkamvubxpcqit")

from_addr = "jmdelaney8@gmail.com"

server.sendmail(from_addr, to_addr, msg)

server.quit()
