单表的分组查询：

    查询每一个部门名称以及对应的员工数
    
    emp:
    
    id   name   age   salary   dep 
    1    alex   12    2000     销售部
    2    egon   22    3000     人事部
    3    wen    22    5000     人事部
    
    
    sql:  select dep,count(id) from emp group by dep;
    思考： 如何用ORM语法进行分组查询？
    
    
    
insert into emp values
(1,'alex',12,2000,"销售部"),
(2,'egon',22,3000,"人事部"),
(3,'wen',22,5000,"人事部");

create table emp(
id int primary key,
name varchar(8),
age int,
salary decimal,
dep char
);

跨表的分组查询：
    
    查询每一个出版社出版的书籍个数
    Book.objects.values("publish_id").annotate(Count("id"))