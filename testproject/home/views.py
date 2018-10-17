


from django import forms

import re
import json

MY_CHOICES = (
    ('1', 'sub.'),
    ('2', 'sub.sub.'),
    ('3', 'sub.sub.sub'),
)


class ContactForm(forms.Form):

    ipadres = forms.ChoiceField(choices=MY_CHOICES)
    domain_tar = forms.CharField()
    work_done = forms.CharField(required=False,disabled=True)



from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail, BadHeaderError


def clear_url(target):
	return re.sub('.*www\.','',target,1).split('/')[0].strip() # target передает домен 

def save_subdomains(subdomain,output_file):
	with open(output_file,"a") as f:
		f.write(subdomain + '\n')
		f.close()

def main():
	
	#banner()
	#args = parse_args()

	subdomains = []
	target = clear_url(domain_tar.domain)
	output = domain_tar.output

	req = requests.get("https://crt.sh/?q=%.{d}&output=json".format(d=target))

	if req.status_code != 200:
		print("[X] Information not available!") 
		exit(1)

	json_data = json.loads('[{}]'.format(req.text.replace('}{', '},{')))

	for (key,value) in enumerate(json_data):
		subdomains.append(value['name_value'])

	
	# print("\n[!] ---- TARGET: {d} ---- [!] \n".format(d=target))

	subdomains = sorted(set(subdomains))

	for subdomain in subdomains:
#		print("[-]  {s}".format(s=subdomain))
		if output is not None:
			save_subdomains(subdomain,output)

 #  print("\n\n[!]  Done. Have a nice day! ;).")


def home(request):

	if request.method == 'POST':
		form = ContactForm(request.POST)
		#Если форма заполнена корректно, сохраняем все введённые пользователем значения
		if form.is_valid():
			subject = form.cleaned_data['subject']
			sender = form.cleaned_data['sender']
			message = form.cleaned_data['message']
			copy = form.cleaned_data['copy']
                        #ipadres = forms.cleaned_data['ipadres']
			recipients = ['bigcaches@ya.ru']
			#Если пользователь захотел получить копию себе, добавляем его в список получателей
			if copy:
				recipients.append(sender)
			try:
				send_mail(subject, message, 'bigcaches@ya.ru', recipients)
			except BadHeaderError: #Защита от уязвимости
				return HttpResponse('block некорректный заголовок')
			#Переходим на другую страницу, если сообщение отправлено
			return render(request, 'landing/landing.html')
	else:
		#Заполняем форму
		form = ContactForm()
	#Отправляем форму на страницу
	return render(request, 'home/index.html', {'form': form})





#def contact(request):
 #   return render(request, 'contact/contact.html', locals()) 