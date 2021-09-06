README 

(this file is better seen as a RAW file, you could click this "RAW" button above this window on the right side)

Financial chat-bot django app

![image](https://user-images.githubusercontent.com/28491749/132144993-4e8304a9-95dd-4fb6-a92a-6ce5775576f3.png)



This app allow registered users to create or enter on a chat-room
and let them chat online and share financial information.
There is a bot that brings stock quotation with a command like this:
"/stock=stock_name", for example, if user wants to bring and share on
the chat-room lattest tesla close price, user could type /stock=tsla,
and a Bot will post a message like this:

"TSLA.US quote is $733.57 per share".

If there is not information for the stock or the stock symbol is wrong,
the Bot will post this:

"There is no data for requested symbol"

Features:

- Bot is handle with a worker using Celery (Celery is a task queue/job),
  and It uses RabbitMQ as its message Broker. This improves its performance.
- For real-time asyncronous comunication this app uses Channels library 
  which supports asyncronous comunication through web-sockets. Channels
  is set-up to use redis as its comunication broker and channel layer.
- Users can Sign up, Login and Logout.
- Registers users can enter on an existing chat-room or create one, typing
  the name of the chat-room desired.
- Comunication on chat room is real-time.
- Messages are stored on DataBase, with date, user, text message and room.


Installation

- It needs python 3.8 | 3.9
- You should have installed on your local machine redis-server > 5 and
  rabbitMQ > 3.9.5.
  also you could run redis on docker as: docker run -p 6379:6379 -d redis:5

  to check the status of rabbitmq type: systemctl status rabbitmq

  You have to see that it is active and running, like this:

  rabbitmq-server.service - RabbitMQ broker
   Loaded: loaded (/lib/systemd/system/rabbitmq-server.service; enabled; vendor preset: enabled)
   Active: active (running) since Sat 2021-09-04 16:27:07 -05; 1 day 1h ago
 Main PID: 1844 (beam.smp)
    Tasks: 28 (limit: 4915)
   CGroup: /system.slice/rabbitmq-server.service
           ├─1844 /usr/lib/erlang/erts-12.0.3/bin/beam.smp -W w -MBas ageffcbf -MHas ageffcbf -MBlmbcs 512 -MHlmbcs 512 -MMmcs 30 -P 1048576 
           ├─2105 erl_child_setup 32768
           ├─2873 /usr/lib/erlang/erts-12.0.3/bin/epmd -daemon
           ├─2962 inet_gethost 4
           └─2963 inet_gethost 4

  to check the status of redis-server type: systemctl status redis-server

  You have to see that it is active and running, like this:

  edis-server.service - Advanced key-value store
   Loaded: loaded (/lib/systemd/system/redis-server.service; disabled; vendor preset: enabled)
   Active: active (running) since Sat 2021-09-04 16:37:53 -05; 1 day 1h ago
     Docs: http://redis.io/documentation,
           man:redis-server(1)
  Process: 7665 ExecStart=/usr/bin/redis-server /etc/redis/redis.conf (code=exited, status=0/SUCCESS)
 Main PID: 7682 (redis-server)
    Tasks: 5 (limit: 4915)
   CGroup: /system.slice/redis-server.service
           └─7682 /usr/bin/redis-server 127.0.0.1:6379

- To install dependencies you can create a virtual env like this:
    Install VirtulEnv
        Run `pip3 install virtualenv`
    Create VirtualEnv
        cd to chatroom directory
        Run `virtualenv -p python3 .env`
    Activate VirtualEnv
        Run `source .env/bin/activate`
    Install Dependencies
        Run `pip install -r requirements.txt`

- From "base" directory run migrations typing:
    python3 manage.py migrate

- Now, let’s make sure that the channel layer can communicate with Redis.
  Open a Django shell and run the following commands from "base" directory:

>>> python3 manage.py shell
>>> 
>>> import channels.layers
>>> 
>>> channel_layer = channels.layers.get_channel_layer()
>>> 
>>> from asgiref.sync import async_to_sync
>>> 
>>> async_to_sync(channel_layer.send)('test_channel', {'type': 'TEST'})
>>> 
>>> async_to_sync(channel_layer.receive)('test_channel')
>>> 

It should return >>> {'type': 'TEST'}

- Now, in order for the Bot works, from "base" directory open a new terminal an type:
  celery -A base worker -l info

  It should display something like this:

  -------------- celery@norman-dell v5.1.2 (sun-harmonics)
--- ***** ----- 
-- ******* ---- Linux-5.4.0-81-generic-x86_64-with-glibc2.27 2021-09-05 23:43:38
- *** --- * --- 
- ** ---------- [config]
- ** ---------- .> app:         base:0x7f0832968310
- ** ---------- .> transport:   amqp://guest:**@localhost:5672//
- ** ---------- .> results:     disabled://
- *** --- * --- .> concurrency: 4 (prefork)
-- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
--- ***** ----- 
 -------------- [queues]
                .> celery           exchange=celery(direct) key=celery
                

[tasks]
  . base.celery.debug_task
  . chat.tasks.send_bot_message

[2021-09-05 23:43:39,016: INFO/MainProcess] Connected to amqp://guest:**@127.0.0.1:5672//
[2021-09-05 23:43:39,028: INFO/MainProcess] mingle: searching for neighbors
[2021-09-05 23:43:40,083: INFO/MainProcess] mingle: all alone
[2021-09-05 23:43:40,129: WARNING/MainProcess] /home/norman/jobsity/chatroom/.env/lib/python3.9/site-packages/celery/fixups/django.py:203: UserWarning: Using settings.DEBUG leads to a memory
            leak, never use this setting in production environments!
  warnings.warn('''Using settings.DEBUG leads to a memory

[2021-09-05 23:43:40,129: INFO/MainProcess] celery@norman-dell ready.
[2021-09-05 23:43:40,130: INFO/MainProcess] Task chat.tasks.send_bot_message[283ac847-1c82-4884-9ecd-117d87f4db3e] received
[2021-09-05 23:43:41,518: INFO/ForkPoolWorker-1] Task chat.tasks.send_bot_message[283ac847-1c82-4884-9ecd-117d87f4db3e] succeeded in 1.2835561700048856s: None

- Finally, from another terminal you start the server typing:
  python3 manage.py runserver

  you will see:

    System check identified no issues (0 silenced).
    September 05, 2021 - 23:45:26
    Django version 3.2.7, using settings 'base.settings'
    Starting ASGI/Channels version 3.0.1 development server at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.

- Now you can go type on your navigator http://127.0.0.1:8000/ and use the app. ENJOY.

- There are 3 unit test to check bot functions. you can run this tests by running from
  "base" directory:

    python3 manage.py test chat


Creator: Norman Isaza
