from .models import Choice, Question,Product_info
from django.shortcuts import get_object_or_404,render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Question 
from django.template import loader
from django.urls import reverse
from django.views import generic
import os
from selenium import webdriver
import requests
from time import sleep
import time
from bs4 import BeautifulSoup
from selenium import webdriver
import datetime
import sys
import re

class PriceView(generic.TemplateView):
    template_name = 'getprice/index.html'

def crawler(request):
    targetGetter = ""
    if request.method == 'POST':
        print(request.POST.get('crawlTarget'))
        targetGetter = request.POST.get('crawlTarget')
    else:
        print("input error")
    temp = re.findall(r'[A-Za-z]+|\d+', targetGetter)
    keyword = (" ".join(temp))
    print(keyword)
    pchome_url = "https://ecshweb.pchome.com.tw/search/v3.3/?q=" + \
        targetGetter + "%20&scope=all&sortParm=rnk&sortOrder=dc"
    momo_url = "https://www.momoshop.com.tw/search/searchShop.jsp?keyword=" + \
        keyword + "&searchType=1"

    #取得檔案位置
    DIR_NAME = os.path.dirname(os.path.abspath(__file__))
    print(DIR_NAME)
    #開啟driver
    driver = webdriver.Chrome(executable_path=DIR_NAME+'/chromedriver')
    # #Get item price in pchome
    driver.get(pchome_url)
    sleep(4)
    i = 0
    prod_id = ""
    d1 = driver.find_elements_by_tag_name('dl')
    for items in d1:
            if i == 1:
                break
            else:
                if items.get_attribute("id") != "":
                    prod_id = items.get_attribute("id")
                    i += 1
    price_path = "//div[@id='ItemContainer']/dl[@id='" + \
        prod_id + "']/dd[3]/ul/li/span/span"
    price = driver.find_element_by_xpath(price_path)

    pc_price = price.get_attribute('textContent')
    pc_crawDate = datetime.date.today()
    #Get item price in momo
    driver.get(momo_url)
    sleep(4)
    # price_path = "//div[contains(@class, 'listArea')]/ul/li"
    # price = driver.find_element_by_xpath(price_path)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    item_list = soup.find_all('div', class_='listArea')
    item_content = str(item_list)
    soup2 = BeautifulSoup(item_content, "html.parser")
    price = soup2.find('span', class_='price')

    momo_price = (str(price.text).replace("$", "")).replace(",", "")
    momo_crawDate = datetime.date.today()
    # Product_info.object.create(p_name="Pixel4", p_price=pc_price, p_site="PChome")
    print(pc_price, pc_crawDate)

    print(momo_price, momo_crawDate)
    
    
    return render(request, "getprice/index.html", {'momo': momo_price, "pchome": pc_price, "c_data": pc_crawDate}
    )
    # return HttpResponseRedirect(reverse("polls:price"), args=(keyword))



# Create your views here.

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
        #取得question
        question = get_object_or_404(Question, pk=question_id)
        try:
            #找question的外節鍵
            selected_choice = question.choice_set.get(pk=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            # Redisplay the question voting form.
            return render(request, 'polls/detail.html', {
                'question': question,
                'error_message': "You didn't select a choice.",
            })
        else:
            selected_choice.votes += 1
            selected_choice.save()
            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back button.
            return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))



























# def index(request):
#     " '-' 號 代表相反 (reverse), [:5] 表示前五"
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     # template = loader.get_template("polls/index.html")
#     context = {
#         "latest_question_list":latest_question_list
#     }
#     return render(request,"polls/index.html",context)
#     # return HttpResponse(template.render(context, request))
#     # output = '\n'.join([q.question_text for q in latest_question_list])
#     # return HttpResponse(output)


# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question': question})
#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exist")
#     # return render(request, 'polls/detail.html', {'question': question})


# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})



# def vote(request, question_id):
#     #取得question
#     question = get_object_or_404(Question, pk=question_id)
#     try:
#         #找question的外節鍵
#         selected_choice = question.choice_set.get(pk=request.POST['choice'])
#     except (KeyError, Choice.DoesNotExist):
#         # Redisplay the question voting form.
#         return render(request, 'polls/detail.html', {
#             'question': question,
#             'error_message': "You didn't select a choice.",
#         })
#     else:
#         selected_choice.votes += 1
#         selected_choice.save()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#         return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


