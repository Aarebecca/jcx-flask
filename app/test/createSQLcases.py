# 向测试数据库中添加测试用例

from app.utils import SQL


sqls = [
    'insert into user(`nickname`, `password`, `password_hash`, `signin_time`, `access_token`, `latest_time`,'
    '`authority`, `identity`)values("Aaron", "psw", "pswhs", "2018-12-12 12:23:14", "token", "2018-12-12 15:41:14",'
    '\'{"read": ["news","notice","file"], "edit": ["news","notice","file"], "pub":["news","notice","file"],'
    '"approve":["news", "notice", "file"], "delete": ["news", "notice", "file"]}\', 6);',
    'insert into user(`nickname`, `password`, `password_hash`, `signin_time`, `access_token`, `latest_time`,'
    '`authority`, `identity`)values("Aaron2", "psw", "pswhs", "2018-12-12 12:23:14", "token1", "2018-12-11 15:41:14",'
    '\'{"read": ["news","notice","file"], "edit": ["news","notice","file"], "pub":["news","notice","file"],'
    '"approve":["news", "notice", "file"], "delete": ["news", "notice", "file"]}\', 6);',
    'insert into user(`nickname`, `password`, `password_hash`, `signin_time`, `access_token`, `latest_time`,'
    '`authority`, `identity`)values("Aaron3", "psw", "pswhs", "2018-12-12 12:23:14", "token1", "2018-12-12 11:41:14",'
    '\'{"read": ["news","notice","file"], "edit": ["news","notice","file"], "pub":["news","notice","file"],'
    '"approve":["news", "notice", "file"], "delete": ["news", "notice", "file"]}\', 6);',


    'insert into news (`title`,`abstract`,`content`,`album`,`author`,`authority`,`read`,`type`,`status`)'
    'values ("ti","abs","cont","ab","aut",\'{"read":{"identity":["everyone"],"users":[]},"edit":'
    '{"identity":["everyone"],"users":[]}}\',123,"ty","valid");',
    'insert into news (`title`,`abstract`,`content`,`album`,`author`,`authority`,`read`,`type`,`status`)'
    'values ("ti","abs","cont","ab","aut",\'{"read":{"identity":["everyone"],"users":[]},"edit":'
    '{"identity":["everyone"],"users":[]}}\',123,"ty","valid");',

    'insert into notice (`title`,`tag`,`author`,`authority`,`content`,`read`,`type`,`status`)'
    'values("ttle","newtag","author",\'{"read":{"identity":["everyone"],"users":[]},"edit":'
    '{"identity":["everyone"],"users":[]}}\',"content",123,"type","valid");',

    'insert into people (`no`,`name`,`homepage`,`age`,`job`,`edu`,`degree`,`email`,`native`,'
    '`pho`,`department`,`intro`,`paper`,`other`)'
    'values(20151672,"杨涛","http://www.iaaron.cn","22","sty","cqu","master","943720372@qq.com",'
    '"CQHC","121341241321","SSE","nointro","nopaper","none");',
    'insert into people (`no`,`name`,`homepage`,`age`,`job`,`edu`,`degree`,`email`,`native`,'
    '`pho`,`department`,`intro`,`paper`,`other`)'
    'values(20151673,"杨X","http://www.iaaron.cn","22","sty","cqu","master","943720372@qq.com",'
    '"CQHC","121341241321","SSE","nointro","nopaper","none");',
    'insert into people (`no`,`name`,`homepage`,`age`,`job`,`edu`,`degree`,`email`,`native`,'
    '`pho`,`department`,`intro`,`paper`,`other`)'
    'values(20151674,"杨XX","http://www.iaaron.cn","22","sty","cqu","master","943720372@qq.com",'
    '"CQHC","121341241321","SSE","nointro","nopaper","none");',

    'insert into login (`uid`,`time`,`ip`,`user_agent`,`access_token`,`mani`)'
    'values("1", "2018-12-10 12:00:12","127.0.0.1","CHROME","TOKEN1","signin");',
    'insert into login (`uid`,`time`,`ip`,`user_agent`,`access_token`,`mani`)'
    'values("1", "2018-12-11 12:00:12","127.0.0.1","CHROME","TOKEN1","pub");',
    'insert into login (`uid`,`time`,`ip`,`user_agent`,`access_token`,`mani`)'
    'values("1", "2018-12-12 12:00:12","127.0.0.1","CHROME","TOKEN1","edit");',
    'insert into login (`uid`,`time`,`ip`,`user_agent`,`access_token`,`mani`)'
    'values("1", "2018-12-12 16:00:12","127.0.0.1","CHROME","TOKEN2","logout");',
    'insert into login (`uid`,`time`,`ip`,`user_agent`,`access_token`,`mani`)'
    'values("2", "2018-12-10 12:40:12","127.0.0.1","CHROME","TOKEN3","login");',
    'insert into login (`uid`,`time`,`ip`,`user_agent`,`access_token`,`mani`)'
    'values("2", "2018-12-10 12:50:12","127.0.0.1","CHROME","TOKEN3","pub");',
    'insert into login (`uid`,`time`,`ip`,`user_agent`,`access_token`,`mani`)'
    'values("2", "2018-12-12 16:10:12","127.0.0.1","CHROME","TOKEN3","pub");',

    'insert into file (`name`,`type`,`author`,`path`,`authority`,`hash`,`status`)'
    'values("filename","png","Aaron","https://github.com/Aarebecca/jcx-flask/blob/master/app/models/user.py",'
    '\'{"read":{"identity":["everyone"],"users":[]},"edit":'
    '{"identity":["everyone"],"users":[]}}\',"hash","valid");'
]

s = SQL()

for sql in sqls:
    print(sql)
    s.operator(sql)


