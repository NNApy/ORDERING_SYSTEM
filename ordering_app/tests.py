from django.test import TestCase
from django.contrib.auth.models import User
from models import Orders

class MyTest(TestCase):

    def test_ok_add_order(self):
        User.objects.create_user('username',
                                 'admin@orders.com',
                                 '123',
                                 is_superuser=1
                                 )
        data = {'customer': 'my_test_customer',
                'buy': 'patatos',
                'email': 'test@email.com',
                'byn': '4',
                'byr': '40000',
                'comment': 'test_comment',
                'date_create': '20-07-2016'
                }
        response = self.client.post('', data)
        q_my_order = Orders.objects.filter()
        self.assertEquals(q_my_order.count(), 1)
        order = q_my_order.get()
        self.assertEquals(order.customer, data['customer'])
        self.assertEquals(order.buy, data['buy'])
        self.assertEquals(order.email, data['email'])
        self.assertEquals(order.byn, data['byn'])
        self.assertEquals(order.byr, data['byr'])
        self.assertEquals(order.comment, data['comment'])
        self.assertEquals(order.date_create, data['date_create'])

'''''''''

    def test_ok_delete_my_task(self):
        data = {'task_name': 'my_test_task', 'done': '1'}
        response = self.client.post('/add_task/', data)
        q_my_task = Tasks.objects.filter()
        self.assertEquals(q_my_task.count(), 1)
        Tasks.objects.filter(id=1).delete()
        self.assertEquals(q_my_task.count(), 0)

    def test_ok_edit_my_task(self):
        data = {'task_name': 'my_test_task', 'done': '1'}
        response = self.client.post('/add_task/', data)
        q_my_task = Tasks.objects.filter()
        self.assertEquals(q_my_task.count(), 1)
        Tasks.objects.filter(id=1).update(task_name='NEW NAME FOR MY TASK')
        self.assertEquals(Tasks.objects.filter().get().task_name, 'NEW NAME FOR MY TASK')

'''''''''

