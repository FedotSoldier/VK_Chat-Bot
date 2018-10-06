import vk_api
import time, json

token = 'af4a5098f7f8b1782f9087f6cdfd04e6a952d31299e75cc56823cc8a53aa1fa66067cf272f1692982baf6'
# Сменить токен. У меня новый телефон и не могу получить ключ доступа для новой беседы.
vk=vk_api.VkApi(login='---', token=token)  # scope - права доступа(не знаю точно, что это)
# В поле login рекомендуется указать номер телефона, для автоматического обхода проверки безопасности
# Насколько я понял многие методы не работают без авторизации
# То есть некоторые методы недоступны без указания своего логина и пароля
vk.auth(token_only=True) # vk.auth() не работает без login
# Если авторизоваться, то вся информация пойдет о пользователе, а не о сообществе
# Чтобы получить информацию о пользователе, при возникновении ошибки no acces_token passed
# нужно передать password в vk = VkApi(... и запустить программу еще раз. Потом password можно будет убрать

print(  # Получаем информацию о чате.
		#vk.method('messages.getConversations')
		vk.method('wall.get', {'owner_id':-171852677}),  # messages.getConversations
		# vk.method('users.get')
		)
# При использовании методов users.get или docs.get в текущей директории появляется файл vk_config.v2.json с информацией о пользователе
# 'messages.getLongPollServer' ts = 1755371275
'''
# Создаём клавиатуру в формате словаря(это списал с сайта)
keyboard = \
{ 
		"one_time": True, 
		"buttons": [ 
			[{ 
				"action": { 
					"type": "text", 
					"label": "Red" 
				}, 
				"color": "negative" 
			}, 
		 { 
				"action": { 
					"type": "text",  
					"label": "Green" 
				}, 
				"color": "positive" 
			}], 
			[{ 
				"action": { 
					"type": "text", 
					"label": "White" 
				}, 
				"color": "default" 
			}, 
		 { 
				"action": { 
					"type": "text", 
					"label": "Blue" 
				}, 
				"color": "primary" 
			}] 
		] 
	} 

my_id = vk.method('messages.getConversations')['items'][0]['last_message']['from_id']
# my_id - это id последнего сообщения в чате, поэтому сначала напиши в группу любое сообщение.
# (Или убедись, что твоё сообщение последнее)

vk.method('messages.send', 
			{'user_id':my_id, 
			'message':'Клавиатуру в студию!',
			'keyboard':str(json.dumps(keyboard)) # Делаем из нашего словаря с параметрами клавиатуры json объект
			})									 # Как это работает я понятия не имею. 
												 # Просто передаем словарь с параметрами клавиатуры в соответствующую функцию,
												 # встроенной библиотеки json и получаем результат
'''
