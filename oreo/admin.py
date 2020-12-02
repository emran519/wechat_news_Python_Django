from urllib.parse import urlsplit

from django.forms import model_to_dict
from django.utils import timezone
from django.utils.datetime_safe import datetime
from django.views import View
from django.http import JsonResponse, HttpResponse
from oreo.models import Navigator, User, Article, Collect, Config
from djangoProject.settings import STATICFILES_DIRS
import os

class AppletController(View):

    # Json
    def resJson(code, data, safe=True):
        """
           :param code: 200=>成功;-1->失败
           :param data: 返回的参数
           :return: 输出JSON
           """
        if code == 200:
            json_dict = {'code': 200, 'msg': "成功", 'data': data}
        else:
            json_dict = {'code': -1, 'msg': "失败", 'data': data}
        return JsonResponse(json_dict, safe=safe)

    # 函数选择器
    def isRequestUrl(request):
        """
        @require_GET
        :return: json
        """
        url = request.GET.get('api_uri')
        # 上传图片
        if url == 'upload_photo':
            return AppletController.uploadPhoto(request)
        # 用户列表
        if url == 'user_list':
            return AppletController.userList(request)
        # 新闻列表
        if url == 'article_list':
            return AppletController.articleList(request)
        # 添加新闻
        if url == 'article_add':
            return AppletController.articleAdd(request)
        # 编辑新闻页面获取新闻信息
        if url == 'article_info':
            return AppletController.articleInfo(request)
        # 编辑新闻
        if url == 'article_edit':
            return AppletController.articleEdit(request)
        # 删除新闻
        if url == 'article_del':
            return AppletController.articleDel(request)
        # 轮播图列表
        if url == 'rotation_list':
            return AppletController.rotationList(request)
        # 添加轮播图
        if url == 'rotation_add':
            return AppletController.rotationAdd(request)
        # 修改轮播图
        if url == 'rotation_edit':
            return AppletController.rotationEdit(request)
        # 删除轮播图
        if url == 'rotation_del':
            return AppletController.rotationDel(request)
        # 小程序设置参数
        if url == 'applet_info':
            return AppletController.appletInfo(None)
        # 编辑小程序设置参数
        if url == 'applet_edit':
            return AppletController.appletEdit(request)

        return AppletController.resJson(code='-1', data='error')


    # 上传图片
    def uploadPhoto(request):
        if request.method == 'GET':
            return AppletController.resJson(code=-1, data="error")
        elif request.method == 'POST':
            # 上传的文件
            content = request.FILES.get('file', None)
            # 获取源文件名的后缀
            ext = content.name.split('.')[-1]
            # 通过当前时间字符串作为文件名
            file_name = datetime.now().strftime("%Y%m%d_%H%M%S")
            # 拼接文件名和后缀
            file = file_name + '.' + ext
            if not content:
                return AppletController.resJson(code=-1, data="无上传文件")
            # 获取上传文件的文件名，并将其存储到指定位置
            path_type = request.POST.get('type')
            if not path_type:
                src_path = "news/newsPhoto/"
            elif int(path_type) == 1:
                src_path = "news/newsIndexPhoto/"
            elif int(path_type) == 2:
                src_path = "news/navigatorPhoto/"
            position = os.path.join(STATICFILES_DIRS[0], src_path + file)
            # 打开存储文件
            storage = open(position, 'wb+')
            # 分块写入文件
            for chunk in content.chunks():
                storage.write(chunk)
                # 写入完成后关闭文件
                storage.close()
            # 如果是https则为True，反之为False
            http = urlsplit(request.build_absolute_uri(None)).scheme
            # 获得当前的HTTP或HTTPS
            host = request.META['HTTP_HOST']
            # 获取当前域名
            shorturl = http + '://' + host + '/static/' + src_path + file
            data = {}
            data['src'] = shorturl
            return AppletController.resJson(code=200, data=data)
        return AppletController.resJson(code=-1, data="不支持的请求方法")

    # 用户列表
    def userList(request):
        # 接受前端传来的查询条件信息
        page = int(request.GET.get('page'))
        limit = int(request.GET.get('limit'))
        start =limit * (page-1)
        # 查询用户表
        user = User.objects.all()[start:limit]
        json_list = []
        for ret in user:
            json_dict = model_to_dict(ret)
            json_list.append(json_dict)
        return AppletController.resJson(code=200, data=json_list, safe=False)

    # 新闻列表
    def articleList(request):
        # 接受前端传来的查询条件信息
        page = int(request.GET.get('page'))
        limit = int(request.GET.get('limit'))
        start =limit * (page-1)
        # 查询用户表
        user = Article.objects.all()[start:limit]
        json_list = []
        for ret in user:
            json_dict = model_to_dict(ret)
            json_list.append(json_dict)
        return AppletController.resJson(code=200, data=json_list, safe=False)

    # 添加新闻
    def articleAdd(request):
        if request.method == 'GET':
            return AppletController.resJson(code=-1, data="error")
        elif request.method == 'POST':
            news_title = request.POST.get('news_title')
            news_text = request.POST.get('news_text')
            news_logo = request.POST.get('newsLogo')
            status = request.POST.get('status')
            # 写入数据
            Article.objects.create(title=news_title, text=news_text, title_img=news_logo, status=status, add_time=timezone.now())
            return AppletController.resJson(code=200, data='添加成功')
        return AppletController.resJson(code=-1, data="不支持的请求方法")

    # 编辑新闻页面获取新闻信息
    def articleInfo(request):
        if request.method == 'GET':
            return AppletController.resJson(code=-1, data="error")
        elif request.method == 'POST':
            news_id = request.POST.get('news_id')
            _article = Article.objects.filter(id=news_id)
            json_list = []
            for ret in _article:
                json_dict = model_to_dict(ret)
                json_list.append(json_dict)
            return AppletController.resJson(code=200, data=json_list, safe=False)
        return AppletController.resJson(code=-1, data="不支持的请求方法")

    # 编辑新闻
    def articleEdit(request):
        if request.method == 'GET':
            return AppletController.resJson(code=-1, data="error")
        elif request.method == 'POST':
            news_id = request.POST.get('news_id')
            news_title = request.POST.get('news_title')
            news_text = request.POST.get('news_text')
            news_logo = request.POST.get('newsLogo')
            status = request.POST.get('status')
            # 更新数据
            Article.objects.filter(id=news_id).update(title=news_title, text=news_text, title_img=news_logo, status=status)
            return AppletController.resJson(code=200, data='更新成功')
        return AppletController.resJson(code=-1, data="不支持的请求方法")

    # 删除新闻
    def articleDel(request):
        if request.method == 'GET':
            return AppletController.resJson(code=-1, data="error")
        elif request.method == 'POST':
            news_id = request.POST.get('news_id')
            # 删除数据
            Article.objects.filter(id=news_id).delete()
            return AppletController.resJson(code=200, data="删除成功")
        return AppletController.resJson(code=-1, data="不支持的请求方法")

    # 轮播图列表
    def rotationList(request):
        # 接受前端传来的查询条件信息
        page = int(request.GET.get('page'))
        limit = int(request.GET.get('limit'))
        start =limit * (page-1)
        # 查询用户表
        nav = Navigator.objects.all()[start:limit]
        json_list = []
        for ret in nav:
            json_dict = model_to_dict(ret)
            json_list.append(json_dict)
        return AppletController.resJson(code=200, data=json_list, safe=False)

    # 添加轮播图
    def rotationAdd(request):
        if request.method == 'GET':
            return AppletController.resJson(code=-1, data="error")
        elif request.method == 'POST':
            image_src = request.POST.get('image_src')
            article_id = request.POST.get('news_id')
            status = request.POST.get('status')
            # 写入数据
            Navigator.objects.create(image_src=image_src, article_id=article_id, status=status, add_time=timezone.now())
            return AppletController.resJson(code=200, data='添加成功')
        return AppletController.resJson(code=-1, data="不支持的请求方法")

    # 修改轮播图
    def rotationEdit(request):
        if request.method == 'GET':
            return AppletController.resJson(code=-1, data="error")
        elif request.method == 'POST':
            navigator_id = request.POST.get('navigator_id')
            image_src = request.POST.get('image_src')
            article_id = request.POST.get('article_id')
            status = request.POST.get('status')
            # 更新数据
            Navigator.objects.filter(id=navigator_id).update(image_src=image_src, article_id=article_id, status=status)
            return AppletController.resJson(code=200, data='更新成功')
        return AppletController.resJson(code=-1, data="不支持的请求方法")

    # 删除轮播图
    def rotationDel(request):
        if request.method == 'GET':
            return AppletController.resJson(code=-1, data="error")
        elif request.method == 'POST':
            navigator_id = request.POST.get('navigator_id')
            # 删除数据
            Navigator.objects.filter(id=navigator_id).delete()
            return AppletController.resJson(code=200, data="删除成功")
        return AppletController.resJson(code=-1, data="不支持的请求方法")

    # 小程序设置参数
    def appletInfo(self):
        conf = Config.objects.all()
        # 数组长度
        res_length = len(conf)
        # 遍历
        _list = {}
        for i in range(res_length):
            _list[conf[i].k] = conf[i].v
        return AppletController.resJson(code=200, data=_list)

    # 小程序设置参数
    def appletEdit(request):
        if request.method == 'GET':
            return AppletController.resJson(code=-1, data="error")
        elif request.method == 'POST':
            applet_navigation_bar_title = request.POST.get('applet_navigation_bar_title')
            applet_navigation_bar_color = request.POST.get('applet_navigation_bar_color')
            applet_user_navigation_bar_color = request.POST.get('applet_user_navigation_bar_color')
            # 更新数据
            Config.objects.filter(k='applet_navigation_bar_title').update(v=applet_navigation_bar_title)
            Config.objects.filter(k='applet_navigation_bar_color').update(v=applet_navigation_bar_color)
            Config.objects.filter(k='applet_user_navigation_bar_color').update(v=applet_user_navigation_bar_color)
            return AppletController.resJson(code=200, data="编辑成功")
        return AppletController.resJson(code=-1, data="不支持的请求方法")


