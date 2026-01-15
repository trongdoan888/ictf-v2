import pika, json, time, sys

def start_engine():
    print(' [!] NCKH GAMEBOT DANG KHOI DONG...')
    while True:
        try:
            credentials = pika.PlainCredentials('ictf', 'ictf')
            parameters = pika.ConnectionParameters('rabbitmq', credentials=credentials)
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()
            channel.queue_declare(queue='service_queue', durable=True)
            
            # Tao Task mau tu du lieu Database
            task = {'team_id': 1, 'service_id': 1, 'script': 'test_script.py', 'type': 'benign'}
            
            channel.basic_publish(exchange='', routing_key='service_queue', body=json.dumps(task))
            print(' [+] [TICK] Da tu dong gui Task vao RabbitMQ!')
            connection.close()
            
            time.sleep(10) # Gui lai sau 10 giay
        except Exception as e:
            print(f' [!] Loi ket noi: {e}')
            time.sleep(5)

if __name__ == '__main__':
    start_engine()
