# 新闻列表按页查询
DROP procedure IF EXISTS `newslist`;
DELIMITER $$
CREATE PROCEDURE `newslist` (IN pageno int ,IN pagesize int)
BEGIN
	select `id`, `album`, `title`, `pub_date`, `abstract`
    from `news`
    where `status` = 'valid'
    and `id` > (pageno-1) * pagesize limit pagesize;
END$$
DELIMITER ;


# 公告列表按页查询
DROP procedure IF EXISTS `noticelist`;
DELIMITER $$
CREATE PROCEDURE `noticelist` (IN pageno int ,IN pagesize int)
BEGIN
	select `id`, `pub_date`, `tag` ,`title`
    from `notice`
	where `id` > (pageno-1) * pagesize limit pagesize;
  where `id` > 
END$$
DELIMITER ;