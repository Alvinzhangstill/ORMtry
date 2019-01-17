from django.db import models
import string
# Create your models here.


# 1.生成的表名app01_authordetail
class AuthorDetail(models.Model):
    # 2.id字段是自动添加的，可以不写
    nid=models.AutoField(primary_key=True)
    birthday=models.DateField()
    telephone=models.BigIntegerField()
    addr=models.CharField(max_length=64)


class Author(models.Model):
    nid=models.AutoField(primary_key=True)
    name=models.CharField(max_length=32)
    age=models.IntegerField()
    # authordetail=models.OneToOneField(to=AuthorDetail,to_field="nid")

    # 一对一：
    # 建议用加引号的写法，否则如果AuthorDetail写在本表下面就找不到了
    authordetail=models.OneToOneField(to="AuthorDetail",to_field="nid",on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# 出版社
class Publish(models.Model):
    nid=models.AutoField(primary_key=True)
    name=models.CharField(max_length=32)
    city=models.CharField(max_length=32)
    email=models.EmailField()


class Book(models.Model):
    nid=models.AutoField(primary_key=True)
    title=models.CharField(max_length=32)
    publishDate=models.DateField()
    price=models.DecimalField(max_digits=5,decimal_places=2)
    # 3.外键字段，Django会在字段名上添加"_id"来创建数据库中的外键列名

    # 一对多：
    publish=models.ForeignKey(to="Publish",to_field="nid",on_delete=models.CASCADE,null=True)
    # 外键字段 ForeignKey有一个null=True的设置（它允许外键接受空值 NULL）
    '''
        publish_id int,
        foreign key(publish_id) references publish(id)
    '''

    # 多对多
    authors=models.ManyToManyField(to="Author")   # 只是创建第三张表，不会添加字段
    # 会拼出一张叫 book_authors 的表
    '''
    CREATE TABLE book_authors(
        id INT PRIMARY KEY auto_increment,
        book_id INT,
        author_id INT,
        FOREIGN KEY(book_id) REFERENCES book(id),
        FOREIGN KEY(author_id) REFERENCES author(id)
    )
    '''


# 创建多对多关系  可以自己写一个关系表，Django也提供了更简便的方法
# class Book2Author(models.Model):
#     nid=models.AutoField(primary_key=True)
#     # to_field="nid"  可加可不加
#     book=models.ForeignKey(to="Book")
#     author=models.ForeignKey(to="Author")

    def __str__(self):
        return self.title


class Emp(models.Model):

    name=models.CharField(max_length=32)
    age=models.IntegerField()
    salary=models.DecimalField(max_digits=8,decimal_places=2)
    dep=models.CharField(max_length=32)
    province=models.CharField(max_length=32)








