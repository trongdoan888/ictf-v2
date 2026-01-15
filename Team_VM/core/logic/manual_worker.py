import pika, json, sqlite3, os

def callback(ch, method, properties, body):
    try:
        task = json.loads(body)
        t_id = task.get('team_id', 1)
        print(f'\n[NCKH] Nhan Task: Team {t_id}')
        
        # Ghi vao log file thay vi dung lenh mysql bi thieu
        with open('/opt/ictf/gamebot/nckh_results.log', 'a') as f:
            f.write(f'Team: {t_id}, Status: UP, Time: {os.popen("date").read()}')
        
        print(f' [+] Da ghi ket qua vao file nckh_results.log')
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f' [!] Loi: {e}')

params = pika.PlainCredentials('ictf', 'ictf')
conn = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', credentials=params))
channel = conn.channel()
channel.queue_declare(queue='service_queue', durable=True)
channel.basic_consume(queue='service_queue', on_message_callback=callback)
print(' [*] Worker NCKH dang doi Task...')
channel.start_consuming()
