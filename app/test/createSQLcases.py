# 向测试数据库中添加测试用例

from app.utils import SQL


sqls = [
    "insert into user (`nickname`,`password`,`password_hash`,`signin_time`,`authority`,`identity`)"
    "values('qwd','psw','pswhs','2018-12-12 12:23:14','asd','asd')",

    "insert into news (`title`,`abstract`,`content`,`album`,`author`,`read`,`type`,`status`)"
    "values ('ti','abs','cont','ab','aut',123,'ty','valid')",

    "insert into notice (`title`,`tag`,`author`,`content`,`read`,`type`)"
    "values('ttle','newtag','author','content',123,'tyoe')",

    "insert into people (`no`,`name`,`homepage`,`age`,`job`,`edu`,`degree`,`email`,`native`,"
    "`pho`,`department`,`intro`,`paper`,`other`)"
    "values(20151671,'杨涛','http://www.iaaron.cn','22','sty','cqu','master','943720372@qq.com',"
    "'CQHC','121341241321','SSE','nointro','nopaper','none')"
]

s = SQL()
# 重复次数
times = 5
for t in range(times):
    for sql in sqls:
        print(s.operator(sql))
