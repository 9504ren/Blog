from django.shortcuts import render,HttpResponse,redirect
from repository import models
# Create your views here.
def index(request,**kwargs):
    if kwargs:
        article_type_id = int(kwargs['article_type_id'])
        article = models.Article.objects.filter(article_type_id=article_type_id).all()
    else:
        article_type_id = None
        article = models.Article.objects.all()
    article_type_list=models.Article.type_choices

    page_num=5#每页显示几条数据
    page_len=11#每页显示多少页码
    if request.GET.get('p'):
        page_p=request.GET.get('p')
        page_p=int(page_p)
    else:
        page_p=1
    start=(page_p-1)*page_num
    end=page_p*page_num
    data = article[start:end]#这一页显示的数据
    len=article.count()
    count,m=divmod(len,page_num)#总共的页数，余数不为零页数加一
    if m:
        count+=1
    if count<page_len:
        start_p=1
        end_p=count+1
    else:
        if page_p<int(page_len/2+2):
            start_p=1
            end_p=page_len+1
        elif page_p+int(page_len/2)>count:
            start_p=count-10
            end_p=count+1
        else:
            start_p=page_p-5
            end_p=page_p+5
    page_list = []  # 当前页的显示列表
    for i in range(start_p,end_p):
        if i ==page_p:
            datap='<a href="./?p=%s" class="num choose">%s</a>'%(i,i)
        else:
            datap = '<a href="./?p=%s" class="num">%s</a>' % (i, i)
        page_list.append(datap)
    page_str="".join(page_list)
    from django.utils.safestring import mark_safe
    page_s=mark_safe(page_str)
    return render(request,
                  'index.html',
                  {
                      'article_type_list':article_type_list,
                       'article_type_id':article_type_id,
                      'article':article,
                      'data':data,
                      'page':page_s
                   })

def detail(request,**kwargs):
    article_type_list = models.Article.type_choices
    if kwargs:
        blog_id = int(kwargs['blog_id'])
        article_id=int(kwargs['article_id'])
        articlede=models.ArticleDetail.objects.filter(article_id=article_id).first()
    return render(request,'detail.html',
                  {
                      'article_type_list':article_type_list,
                       'articlede':articlede,
                      'blog_id':blog_id,
                      'article_id':article_id
                  })

def updown(request):
    if request.session['user_info']:
        print(type(request.GET.get('article_id')),request.GET.get('article_id'))
        id=int(request.GET.get('article_id'))
        article=models.ArticleDetail.objects.filter(article_id=id).first()
        user=models.UserInfo.objects.filter(username=request.session['user_info']['username']).first()
        print(request.GET.get('up'))
        if int(request.GET.get('up')) == 1:
            models.UpDown.objects.create(article=article.article,user=user,up=True)
        else:
            models.UpDown.objects.create(article=article.article, user=user, up=False)
        article_id=int(request.GET.get('article_id'))
        # up_c=models.UpDown.objects.filter(article=article,up=1).count()
        # down_c=models.UpDown.objects.filter(article=article,up=0).count()
        # models.Article.objects.filter(id=article_id).update(up_count=up_c,down_count=down_c)
        url_p='/detail/%s-%s.html'%(request.GET.get('blog_id'),article_id)
        return redirect(url_p)
    else:
        return redirect('/login.html')
