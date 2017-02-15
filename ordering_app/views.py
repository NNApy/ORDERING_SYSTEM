from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from models import Orders
from forms import AddOrder, EditOrder
import arrow


def add_order(request):
    if User.objects.filter(is_superuser=1).count() > 0:
        if request.method == 'POST':
            form = AddOrder(request.POST)
            if form.is_valid():
                Orders.objects.create(customer=request.POST.get('customer'),
                                      buy=request.POST.get('buy'),
                                      email=request.POST.get('email'),
                                      byn=request.POST.get('byn'),
                                      byr=request.POST.get('byr'),
                                      comment=request.POST.get('comment'),
                                      date_create=arrow.utcnow().format('DD-MM-YYYY')
                              )

                send_mail('New order!',
                        'Please buy me a {}.\nMy money: {} BYN, {} BYR\nComment: {}'.format(request.POST.get('buy').encode('utf-8'),
                                                                                            request.POST.get('byn'),
                                                                                            request.POST.get('byr'),
                                                                                            request.POST.get('comment').encode('utf-8')),
                        '{}'.format(request.POST.get('email')),
                        ['admin@orders.com'])

                context = {'message': 'Congratulations! Your order is accepted!',
                            'color': 'green'
                    }
                return render(request, 'index.html', context)
            else:
                data = form.errors
                return HttpResponse('not valid  %s' % data)
        else:
            hour_now = int(arrow.utcnow().to('Europe/Minsk').format('HH'))

            #--------------- Time -------------------------------------

            if 15 <= hour_now <= 24:
                context = {'hour_disabled': 'disabled',
                            'message': 'You late! Orders are taken from 13:00 to 15:00!',
                            'color': 'red'
                          }
            elif 0 <= hour_now < 13:
                    context = {'hour_disabled': 'disabled',
                               'message': 'You are too early! Orders are taken from 13:00 to 15:00!',
                               'color': 'red'
                              }
            else:
                context = {'hour_disable': ''}

            # -------------------------------------------------------------


            return render(request, 'index.html') #, context
    else:
        return redirect('create_admin')


def create_admin(request):
    if User.objects.filter(is_superuser=1).count() > 0:
        return redirect(orders)
    else:
        if request.method == 'POST':
            if request.POST.get('password') == request.POST.get('conf_password'):
                User.objects.create_user(request.POST.get('username'),
                                         request.POST.get('username')+'@orders.com',
                                         request.POST.get('password'),
                                         is_superuser=1
                                        )
                return HttpResponse('Congratulations! Administrator created!')
            else:
                context = {'message_password': 'Password and Confirm Password do not match!'}
                return render(request, 'create_admin.html', context)
        else:
            context = {'message':'This is the first login. Please create an administrator.'}
            return render(request, 'create_admin.html', context)




def edit(request):
    if request.method == 'POST':
        form = EditOrder(request.POST)
        if form.is_valid():
            Orders.objects.filter(id = request.POST.get('id')).update(customer=request.POST.get('customer'),
                                                                      buy=request.POST.get('buy'),
                                                                      email=request.POST.get('email'),
                                                                      byn=request.POST.get('byn'),
                                                                      byr=request.POST.get('byr'),
                                                                      comment=request.POST.get('comment')
                                                                     )

            send_mail('Your order has been changed',
                        'Your new buy: {}\nYour new comment: {}'.format(request.POST.get('buy').encode('utf-8'),
                                                                  request.POST.get('comment').encode('utf-8')),
                        'admin@orders.com',
                        [ '{}'.format(request.POST.get('email'))])
            return redirect('/orders/')
        else:
            data = form.errors
            return HttpResponse('not valid  %s' % data)
    else:
        edit_data = Orders.objects.filter(id=request.GET.get('id')).get()
        context = {'edit_data': edit_data}
        return render(request, 'edit.html', context)




def delete(request):
    del_order = Orders.objects.filter(id=request.GET.get('id')).get()
    send_mail('{}, your order has been deleted'.format(del_order.customer),
              'Sorry, your order has been deleted by the admin',
              'admin@orders.com',
              ['{}'.format(del_order.email)])
    Orders.objects.filter(id=request.GET.get('id')).delete()
    return redirect('/orders/')




@login_required()
def orders(request):
    if request.user.is_superuser == 1:
        byn = 0
        byr = 0
        for i in Orders.objects.filter():
            byn += int(i.byn)
            byr += int(i.byr)
        convert_byr = float(byr)/10000
        context = {'orders_data': Orders.objects.filter(date_create=arrow.utcnow().format('DD-MM-YYYY')).order_by('-id'),
                   'byn': byn,
                   'byr': byr,
                   'total_summ': byn+convert_byr,
                   'date': arrow.utcnow().format('DD-MM-YYYY')
                   }
        return render(request, 'orders.html', context)
    return redirect('/accounts/login/')
