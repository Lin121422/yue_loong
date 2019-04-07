from django.shortcuts import render
from .forms import numForm
from .create_order import create
from .RFM import rfm
from .MPS import mps
from .BOM import bom
from .MRP import mrp
from .operationScheduling import scheduling
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect

# Create your views here.
def hello_view(request):

    return render(request, 'Home.html', {
        'data': "Hello Django ",
    })

# 接收POST请求数据
def search_post(request):
    if request.method == 'POST':    #是否為post請求
        form = numForm(request.POST)
        #if form.is_valid(): #檢查輸入是否符合規範
        ans = {}
        #n = form.cleaned_data['q']
        n = int(request.POST['q'])
        n += 1
        ans['result'] = n
        return render(request, "gogogo.html", ans)
    else:
        return render(request, "gogogo.html")

# enter web page
def home_page(request):
    return render(request, "home.html")

def function_page(request):
    return render(request, "function.html")

def inputOrder_page(request):
    return render(request, "inputOrder.html")

def rfm_page(request):
    return render(request, "RFM.html")

def mps_page(request):
    return render(request, "MPS.html")

def bom_page(request):
    return render(request, "BOM.html")

def mrp_page(request):
    return render(request, "MRP.html")

def operationScheduling_page(request):
    return render(request, "operationScheduling.html")

def showImg(request):
    image = open("FinalProject\\pic\\裕隆汽車.jpg", "rb").read()
    return HttpResponse(image)

#產銷功能
def create_main(request):
    ans = {}
    if request.method == 'POST':
        product = request.POST['Menu']
        quantity = request.POST['amount']
        discount = request.POST['discount'] + "% off"
        ans['result'] = create(product, quantity, discount)
    return  render(request, "inputOrder.html", ans)

def rfm_main(request):
    ans = {}
    if request.method == 'POST':
        ans['result'] = rfm()
    return render(request, "RFM.html", ans)

def mps_main(request):
    ans = {}
    if request.method == 'POST':
        quarter = request.POST['seasonMenu']
        year = request.POST['yearMenu']
        ans['title'] = '%s 年 第 %s 季\t 主排程' %(year, quarter)
        ans['result1'] = mps(year, quarter)[2]
        ans['result2'] = mps(year, quarter)[3]
    return render(request, "MPS.html", ans)

def bom_main(request):
    ans = {}
    if request.method == 'POST':
        ans['bom'] = bom()
    return render(request, "BOM.html", ans)


def mrp_main(request):
    ans = {}
    m1 = ""
    m2 = ""
    if request.method == 'POST':
        month = request.POST['monthMenu']
        year = request.POST['yearMenu']
        # check car 1
        if checkMrp(year, month, 1) == 1:
            m1 = mrp(month, "Car 1")
        elif checkMrp(year, month, 1) == 0:
            m1 = "      No task"
        # check car 2
        if checkMrp(year, month, 2) == 1:
            m2 = mrp(month, "Car 2")
        elif checkMrp(year, month, 2) == 0:
            m2 = "      No task"

        ans['car1'] = "Car 1 : "
        ans['car1Mrp'] = m1
        ans['car2'] = "Car 2 : "
        ans['car2Mrp'] = m2
    return render(request, "MRP.html", ans)


def checkMrp(year, month, car):
    m = 0
    action = 0
    if month == '1' or month == '2' or month == '3':
        if int(month) % 3 == 0:
            m = mps(year, '1')[car - 1][2]
        elif int(month) % 3 == 1:
            m = mps(year, '1')[car - 1][0]
        elif int(month) % 3 == 2:
            m = mps(year, '1')[car - 1][1]
    elif month == '4' or month == '5' or month == '6':
        if int(month) % 3 == 0:
            m = mps(year, '2')[car - 1][2]
        elif int(month) % 3 == 1:
            m = mps(year, '2')[car - 1][0]
        elif int(month) % 3 == 2:
            m = mps(year, '2')[car - 1][1]
    elif month == '7' or month == '8' or month == '9':
        if int(month) % 3 == 0:
            m = mps(year, '3')[car - 1][2]
        elif int(month) % 3 == 1:
            m = mps(year, '3')[car - 1][0]
        elif int(month) % 3 == 2:
            m = mps(year, '3')[car - 1][1]
    elif month == '10' or month == '11' or month == '12':
        if int(month) % 3 == 0:
            m = mps(year, '4')[car - 1][2]
        elif int(month) % 3 == 1:
            m = mps(year, '4')[car - 1][0]
        elif int(month) % 3 == 2:
            m = mps(year, '4')[car - 1][1]

    # do or not
    if m > 0:
        action = 1
    else:
        action = 0
    return action

def operationScheduling_main(request):
    ans = {}
    if request.method == 'POST':
        month = request.POST['monthMenu']
        year = request.POST['yearMenu']
        e1 = ""
        e2 = ""
        # check car 1
        if checkMrp(year, month, 1) == 1:
            s1 = scheduling(month, "Car 1")[0]
            e1 = scheduling(month, "Car 1")[1]
        elif checkMrp(year, month, 1) == 0:
            s1 = "Car 1 : No task"
        # check car 2
        if checkMrp(year, month, 2) == 1:
            s2 = scheduling(month, "Car 2")[0]
            e2 = scheduling(month, "Car 2")[1]
        elif checkMrp(year, month, 2) == 0:
            s2 = "Car 2 : No task"

        ans['title'] = year + "年 " + month + "月"
        ans['car1'] = "Car 1 : "
        ans['car1S'] = s1
        ans['car1E'] = e1
        ans['car2'] = "Car 2 : "
        ans['car2S'] = s2
        ans['car2E'] = e2
    return render(request, "operationScheduling.html", ans)