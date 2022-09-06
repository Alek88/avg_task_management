import xmlrpc.client
import getpass
url = 'http://localhost:15069'
db = 'sg_tm'
username = input('Username: ').strip()
password = getpass.getpass()
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
common.version()
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
res_user = models.execute_kw(db, uid, password,
                             'sg.tm.employee',
                             'search_read',
                             [[('user_id', '=', uid)]],
                             {'fields': ['id'], 'limit': 1})
work_next = True
while work_next:
    if res_user:
        user_id = res_user[0].get('id')
        task_all = models.execute_kw(db, uid, password,
                                     'sg.tm.task',
                                     'search_read',
                                     [[('status', '!=', 'done'),
                                       ('responsible_id', '=', user_id)]],
                                     {'fields':
                                         ['name', 'project_id', 'task_date'],
                                         'limit': 0})
        task_to_display = {}
        k = 1
        for task in task_all:
            task_to_display[k] = task
            k += 1
        for k in range(1, len(task_to_display)+1):
            task = task_to_display.get(k)
            name = task.get('name')
            project = task.get('project_id')[1]
            date = task.get('task_date')
            print(f'{k}) {project}, {name}, {date}')
        print('Для регістрації часу, введіть номер задачі\
та час в хвилинах через пробіл та натисніть Enter/Return')
        err = False
        while not err:
            list = ['1', '2', '3', '4', '5', '6', '7', '8', '0', ' ']
            num, minut = '', ''
            data = input(
                'Введіть дані (Приклад: 1 20).\
Для завершення введіть "q(в)": ').strip()
            if data == 'q' or data == 'в':
                work_next = False
                break
            if data.count(' ') != 1:
                err = True
            if not err:
                for i in data:
                    if i not in list:
                        err = True
                        break
            if err:
                print('Помилка введення. Повторити? (y(д)/n(н)')
                answer = input()
                if answer == 'y' or answer == 'д':
                    err = False
                    continue
            else:
                num, minut = data.split()
                num = int(num)
                minut = int(minut)
                current_task = task_to_display.get(num)
                if current_task is None:
                    print('Вказана задача не знайдена.')
                else:
                    id = current_task.get('id')
                    comment = input('Введіть коментар: ')
                    print('----------------------------------------')
                    write_task = models.execute_kw(db, uid, password,
                                                   'sg.tm.task',
                                                   'write',
                                                   [[id],
                                                    {'number_of_minut':  minut,
                                                    'comment': comment}])
                    err = True
