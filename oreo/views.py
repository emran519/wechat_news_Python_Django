from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponse
import requests, json
# 把模型表引入
from django.utils import timezone
from oreo.models import Navigator, User, Article, Collect, Config
from django.views import View


class AppletApi(View):

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
        # 用户登录
        if url == 'user_login':
            return AppletApi.userOpenId(request)
        # 写入用户信息
        elif url == 'user_info':
            return AppletApi.setUserInfo(request)
        # 获取首页轮播图
        elif url == 'rotation_chart':
            return AppletApi.rotationChart(request)
        # 获取新闻
        elif url == 'news_info':
            return AppletApi.newsInfo(request)
        # 获取对应ID的新闻
        elif url == 'article_info':
            return AppletApi.articleInfo(request)
        # 收藏检测
        elif url == 'collection_news_info':
            return AppletApi.collectionNewsInfo(request)
        # 收藏添加
        elif url == 'collection_news_add':
            return AppletApi.collectionAdd(request)
        # 收藏取消
        elif url == 'collection_news_del':
            return AppletApi.collectionDel(request)
        # 用户收藏的新闻
        elif url == 'user_article':
            return AppletApi.userArticle(request)
        # 获取导航条信息
        elif url == 'navigation_Bar':
            return AppletApi.navigationBar(None)
        return AppletApi.resJson(code='-1', data='error')

    # 获取OpenId
    def userOpenId(request):
        # 接受小程序端GET来的用户CODE
        user_code = request.POST.get('code')
        if not user_code:
            return AppletApi.resJson(code=-1, data="用户CODE不能为空")
        wx_url = "https://api.weixin.qq.com/sns/jscode2session"
        param = {
            'appid': '小程序appId',
            'secret': '小程序secret',
            'js_code': user_code,
            'grant_type': "authorization_code"
        }
        r = requests.get(wx_url, params=param, timeout=20)
        # 转为json 格式的字符串
        data = json.loads(r.content.decode("utf-8"))
        # 获取openid
        open_id = data['openid']
        # 如果获取到OpenID
        if open_id:
            # 查询用户是否存在
            user_info = User.objects.filter(user_openid=open_id)
            # 如果用户不存在
            if not user_info:
                # 写入数据
                User.objects.create(user_openid=open_id, add_time=timezone.now())
                return AppletApi.resJson(code=200, data=open_id)
            return AppletApi.resJson(code=-1, data='数据库已记录该用户信息')
        else:
            return AppletApi.resJson(code='-1', data='error')

    # 写入用户信息
    def setUserInfo(request):
        open_id = request.POST.get('openId')
        if not open_id:
            return AppletApi.resJson(code=-1, data="openId不能为空111")
        avatar_url = request.POST.get('avatarUrl')
        nick_name = request.POST.get('nickName')
        gender = request.POST.get('gender')
        city = request.POST.get('city')
        country = request.POST.get('country')
        province = request.POST.get('province')
        # 根据openId查找用户
        user_info = User.objects.filter(user_openid=open_id)
        # 如果用户存在
        if user_info:
            # 更新数据
            User.objects.filter(user_openid=open_id).update(user_nickname=nick_name, user_sex=gender, user_city=city, user_province=province, user_country=country, user_headimgurl=avatar_url)
            return AppletApi.resJson(code=200, data='更新用户数据成功')
        return AppletApi.resJson(code=-1, data='用户不存在')

    # 获取首页轮播图
    def rotationChart(self):
        res = Navigator.objects.filter(status=1).order_by('-id')
        json_list = []
        for ret in res:
            json_dict = model_to_dict(ret)
            json_list.append(json_dict)
        return AppletApi.resJson(code=200, data=json_list, safe=False)

    # 获取新闻
    def newsInfo(self):
        res = Article.objects.filter(status=1).order_by('-id')
        json_list = []
        for ret in res:
            json_dict = model_to_dict(ret)
            json_list.append(json_dict)
        return AppletApi.resJson(code=200, data=json_list, safe=False)

    # 获取对应ID的新闻
    def articleInfo(request):
        article_id = request.POST.get('newsId')
        if not article_id:
            return AppletApi.resJson(code=-1, data="新闻ID不能为空")
        res = Article.objects.filter(id=article_id).order_by('-id')
        for ret in res:
            json_dict = model_to_dict(ret)
        return AppletApi.resJson(code=200, data=json_dict)

    # 收藏检测
    def collectionNewsInfo(request):
        articleId = request.POST.get('newsId')
        if not articleId:
            return AppletApi.resJson(code=-1, data="新闻ID不能为空")
        open_id = request.POST.get('openId')
        if not open_id:
            return AppletApi.resJson(code=-1, data="用户OpenId不能为空")
        # 查询是否收藏
        collection = Collect.objects.filter(user_openid=open_id, article_id=articleId)
        # 如果已经收藏
        if collection:
            return AppletApi.resJson(code=-1, data="您已经收藏过了哟")
        else:
            return AppletApi.resJson(code=200, data="还未收藏")


    # 收藏新闻
    def collectionAdd(request):
        articleId = request.POST.get('newsId')
        if not articleId:
            return AppletApi.resJson(code=-1, data="新闻ID不能为空")
        open_id = request.POST.get('openId')
        if not open_id:
            return AppletApi.resJson(code=-1, data="用户OpenId不能为空")
        # 查询是否收藏
        collection = Collect.objects.filter(user_openid=open_id, article_id=articleId)
        # 如果已经收藏
        if collection:
            return AppletApi.resJson(code=-1, data="您已经收藏过了哟")
        else:
            # 写入数据
            Collect.objects.create(user_openid=open_id, article_id=articleId, collect_time=timezone.now())
            return AppletApi.resJson(code=200, data="收藏成功")

    # 收藏取消
    def collectionDel(request):
        articleId = request.POST.get('newsId')
        if not articleId:
            return AppletApi.resJson(code=-1, data="新闻ID不能为空")
        open_id = request.POST.get('openId')
        if not open_id:
            return AppletApi.resJson(code=-1, data="用户OpenId不能为空")
        # 查询是否收藏
        collection = Collect.objects.filter(user_openid=open_id, article_id=articleId)
        # 如果已经收藏
        if collection:
            # 删除数据
            Collect.objects.filter(user_openid=open_id, article_id=articleId).delete()
            return AppletApi.resJson(code=200, data="已取消收藏")
        else:
            return AppletApi.resJson(code=-1, data="为收藏")

    # 用户收藏的新闻
    def userArticle(request):
        open_id = request.POST.get('openId')
        if not open_id:
            return AppletApi.resJson(code=-1, data=open_id)
        # 先查询用户收藏信息获取ID
        user_article = Collect.objects.filter(user_openid=open_id).order_by('-id')
        # 数组长度
        res_length = len(user_article)
        user_article_id = []
        # 遍历ID
        for i in range(res_length):
            user_article_id.append(user_article[i].article_id)
        # 根据得到的ID来IN查询新闻信息表
        res = Article.objects.filter(id__in=user_article_id).order_by('-id')
        json_list = []
        for ret in res:
            json_dict = model_to_dict(ret)
            json_list.append(json_dict)
        return AppletApi.resJson(code=200, data=json_list)

    # 获取导航条信息
    def navigationBar(self):
        conf = Config.objects.all()
        # 数组长度
        res_length = len(conf)
        # 遍历
        _list = {}
        for i in range(res_length):
            _list[conf[i].k] = conf[i].v
        return AppletApi.resJson(code=200, data=_list)


