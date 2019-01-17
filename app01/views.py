from django.shortcuts import render,HttpResponse

# Create your views here.
from app01.models import *


def add(request):
    '''
    绑定关系的视图
    :param request:
    :return:
    '''
    # pub=Publish.objects.create(name="四川广电出版社",email="yituosi@qq.com",city="suining")

    # ####################################### 绑定一对多的关系 ########################################
    # 方式1：为book表绑定出版社   book --- publish
    # book_obj=Book.objects.create(title="红楼梦",price=120,publishDate="2009-09-12",publish_id=1)
    # print(book_obj.title)

    # 方式2：
    # pub_obj=Publish.objects.filter(nid=1).first()
    # book_obj=Book.objects.create(title="红楼梦",price=100,publishDate="2012-10-09",publish=pub_obj)
    # print(book_obj.title)
    # print(book_obj.price)
    # print(book_obj.publishDate)
    #
    # print(book_obj.publish)   # 与这本书关联的出版社对象 （重点）
    # print(book_obj.publish.name)
    # print(book_obj.publish.email)
    # print(book_obj.publish_id)

    # 查询西游记的出版社的邮箱
    # xyj = Book.objects.filter(title="三国演义").first()
    # print(xyj.publish.email)

    # ####################################### 绑定多对多的关系 ########################################
    # book_obj=Book.objects.create(title="金瓶梅",price=120,publishDate="2012-01-05",publish_id=1)
    #
    # egon=Author.objects.get(name="egon")
    # alex=Author.objects.get(name="alex")

    # 绑定多对多关系的API：
    # book_obj.authors.add(egon,alex)
    # book_obj.authors.add(1,2,3)  # 可以直接写作者id
    # book_obj.authors.add(*[1,2,3])  # 也可以写 *args形式

    # 解除多对多关系 （先查出来）
    book=Book.objects.filter(nid=4).first()
    # book.authors.remove(1,2)
    # book.authors.remove(*[1,2])

    # book.authors.clear()  # 清除所有

    print(book.authors.all())  # [obj1,obj2...] queryset:与这本书关联的所有作者对象集合

    # 查询主键为4的书籍的所有作者名字 （重点）
    ret=book.authors.all().values("name")
    print(ret)

    return HttpResponse("OK!")


def query(request):
    '''
    跨表查询：
        1 基于对象查询
        2 基于双下划线查询
        3 聚合和分组查询
        4 F 与 Q查询
    :param request:
    :return:
    '''

    # ----------------------------------------- 基于对象的跨表查询（子查询）--------------------------------------------

    # 一对多的正向查询：查询金瓶梅这本书的出版社的名字

    # book_obj=Book.objects.filter(title="金瓶梅").first()
    # print(book_obj.publish)  # 与这本书关联的出版社对象
    # print(book_obj.publish.name)

    # 一对多的反向查询：查询人民出版社出版过的书籍名称

    # publish=Publish.objects.filter(name="人民出版社").first()
    # ret=publish.book_set.all()
    # print(ret)
    #

    # 多对多的正向查询：查询金瓶梅的作者姓名
    # book_obj=Book.objects.filter(title="金瓶梅").first()
    # author_list=book_obj.authors.all()   # queryset [author1,...]
    #
    # for author in author_list:
    #     print(author.name)
    #     print(author.age)

    # 多对多的反向查询：查询alex出版的所有书籍名称
    # author_obj=Author.objects.filter(name="alex").first()
    # books = author_obj.book_set.all()
    # # print(books)
    # for book in books:
    #     print(book.title)

    # 一对一的正向查询：查询作者alex的出生日期（地址、电话）
    # author_obj=Author.objects.filter(name="alex").first()
    # print(author_obj.authordetail.telephone)

    # 一对一的反向查询：查询手机号为119的作者的名字和年龄
    # ad_obj=AuthorDetail.objects.filter(telephone=119).first()   # 这里测试119 不管是给int还是str类型都可以
    # print(ad_obj.author.name)
    # print(ad_obj.author.age)

    # ----------------------------------------- 基于双下划线的跨表查询（join查询）--------------------------------------------
    '''
    正向查询：按字段
    反向查询：按表名(小写)，用来告诉ORM引擎join哪张表
    '''
    # 一对多查询：查询金瓶梅这本书的出版社的名字
    # 方式一：
    # ret=Book.objects.filter(title="金瓶梅").values("publish__city")
    # print(ret)   # <QuerySet [{'publish__city': 'beijing'}]>
    # 方式二：
    # ret=Publish.objects.filter(book__title="金瓶梅").values("email")
    # print(ret)

    # 多对多查询：查询金瓶梅这本书的所有作者的名字

    # 方式1：
    # 需求：通过Book表join与其关联的Author表，属于正向查询：按字段authors通知通知ORM引擎join book_authors与author两张表
    # ret=Book.objects.filter(title="金瓶梅").values("authors__name")  # 正向查询按字段
    # print(ret)

    # 方式2：
    # 需求：通过Author表join与其关联的Book表，属于反向查询：按表名小写book通知ORM引擎join book_authors与book表
    # ret=Author.objects.filter(book__title="金瓶梅").values("name")
    # print(ret)

    # 一对一查询：查询alex的手机号
    # 方式1：
    # 需求：通过Author表join与其关联的AuthorDetail表，属于正向查询：按字段authordetail通知ORM引擎关联AuthorDetail表
    # ret=Author.objects.filter(name="alex").values("authordetail__telephone")
    # print(ret)  # <QuerySet [{'telephone': 110}]>

    # 方式2：
    # 需求：通过AuthorDetail表join与其关联的Author表，属于反向查询：按表名小写author通知ORM引擎关联Author表
    # ret=AuthorDetail.objects.filter(author__name="alex").values("telephone")
    # print(ret)  # <QuerySet [{'telephone': 110}]>

    # 进阶练习：
    # 练习：手机号以110开头的作者出版过的所有书籍名称及其出版社的名称

    # 方式1：
    # 需求：通过Book表join AuthorDetail表，Book与AuthorDetail无关联，所以必须连续跨表
    # ret=Book.objects.filter(authors__authordetail__telephone__startswith="110").values("title","publish__name")
    # print(ret)

    # 2：
    # 分析：author查询book表是反向查询，按表名小写
    # ret=Author.objects.filter(authordetail__telephone__startswith=110).values("book__title","book__publish__name")
    # print(ret)

    # 3：尝试
    # 分析：AuthorDetail查询author 是反向查询 靠表名小写，然后author表查询book也是反向查询
    # ret=AuthorDetail.objects.filter(telephone=110).values("author__book__title","author__book__publish__name")
    # print(ret)

    # ---------------------------------------- 聚合与分组查询 --------------------------------------------------------

    # ############################## 聚合 aggregate：返回值是一个字典，不再是queryset ##############################

    # 查询所有书籍的平均价格
    from django.db.models import Avg,Max,Min,Count,Sum

    # ret=Book.objects.all().aggregate(avg_price=Avg("price"),max_price=Max("price"))  # 可以自己定义名称
    # print(ret)   # {'avg_price': 90.5, 'max_price': Decimal('120.00')}

    # ############################## 分组查询 annotate ，返回值依然是queryset  ##############################

    # =============================单表分组查询：
    # 查询每一个部门的名称以及员工的平均薪水
    # select dep,Avg(salary) from emp group by dep;

    # ret=Emp.objects.values("dep").annotate(avg_salary=Avg("salary"))
    # print(ret)  #

    # 单表分组查询的ORM语法：单表模型.objects.values("group by的字段").a计字nnotate(聚合函数("统段"))

    # 示例2：
    # 查询每个省份的名称以及员工数
    # ret=Emp.objects.values("province").annotate(Count("id"))
    # print(ret)
    # < QuerySet[{'province': '山东省', 'id__count': 2},{'province': '河北省','id__count': 1}] >

    # 补充知识点：
    # ret=Emp.objects.all()
    # print(ret)  # select * from emp;
    # ret=Emp.objects.values("name")
    # print(ret)   # select name from emp;
    #
    # Emp.objects.all().annotate(avg_salary=Avg("salary"))

    # ========================= 多表分组查询：
    # 示例1：查询每一个出版社的名字以及出版的书籍个数：
    # res=Publish.objects.values("name").annotate(Count("book__nid"))
    # res=Book.objects.values("publish__name").annotate(Count("nid"))

    # 按主键分组，然后再取想要的字段（annotate结果是queryset）
    # res=Publish.objects.values("nid").annotate(c=Count("book__title")).values("name","c")
    # print(res)

    # 示例2：查询每一个作者的名字以及出版过的书籍的最高价格
    # (最好不要直接按name分组，因为作者名字有可能是相同的，而通过主键分组就没问题？？)
    # ret=Author.objects.values("nid").annotate(Max("book__price")).values("name","book__price")
    # print(ret)

    # 示例3：查询每本书籍的名称以及对应的作者个数
    # res=Book.objects.values("pk").annotate(author_count=Count("authors__nid")).values("title","author_count")
    # print(res)

    # =========================== 跨表分组查询的另一种玩法：
    # 示例1：查询每一个出版社的名称以及出版的书籍个数：
    # ret=Publish.objects.values("nid").annotate(c=Count("book__title")).values("name","email")
    # ret=Publish.objects.all().annotate(c=Count("book__title"))
    # print(ret)

    # 总结跨表的分组查询的模型：
    # 每个后的表模型.objects.values("pk").annotate(聚合函数(关联表__统计字段)).values("表模型的字段+统计字段")
    # 每个后的表模型.objects.annotate(聚合函数(关联表__统计字段)).values("表模型的字段+统计字段")   # 可以不加all

    # ======================= 练习 =======================
    # 1.统计每一本书的作者个数
    # res=Book.objects.values("pk").annotate(c=Count("authors__pk")).values("title","c")
    # print(res)

    # 2.统计每一本以py开头的书籍的作者个数
    # res=Book.objects.filter(title__startswith="py").annotate(c=Count("authors__pk")).values("title","c")
    # print(res)

    # 3.统计不止一个作者的图书
    # res=Book.objects.values("pk").annotate(c=Count("authors__name")).filter(c__gt=1).values("title","c")
    # print(res)

    # 4.根据一本图书作者数量的多少对查询集Queryset进行排序
    # res=Book.objects.values("pk").annotate(c=Count("authors__name")).order_by("-c").values("title","c")
    # print(res)

    # 5.查询各个作者出的书的总价格
    # res=Book.objects.values("authors__name").annotate(Count("price"))
    res=Author.objects.values('pk').annotate(c=Sum("book__price")).values("name","c")
    # res=Author.objects.annotate(SumPrice=sum("book__price")).values_list("name","SumPrice")
    print(res)

    return HttpResponse("OK")


'''
A - B
关联属性放在A表中

正向查询： A -----------> B
反向查询： B -----------> A

# 一对多查询：
    正向查询：按字段
    反向查询：按表名小写_set.all()

                                      book_obj.publish
            Book(关联属性：publish)  ------------------->  Publish
                                    <--------------------
                                    publish_obj.book_set.all()    # queryset
                                      
# 多对多查询：
    正向查询：按字段
    反向查询：按表名小写_set.all()

                                      book_obj.authors.all()
            Book(关联属性：authors)  ------------------------>  Author
                                    <-------------------------
                                      author_obj.book_set.all() 

# 一对一查询：       
    正向查询：按字段
    反向查询：表名小写
                                          author.authordetail
    Author(关联属性：authordetail)对象  ------------------------->  AuthorDetail对象
                                        <-------------------------          
                                          authordetail.author    # 因为是一对一 所以不用加 _set
'''






