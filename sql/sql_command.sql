-- 创建目录
CREATE TABLE feishu_chat (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tenant_key VARCHAR(20),
    message_id VARCHAR(50),
    user TEXT,
    assistant TEXT,
    create_time VARCHAR(50)
);
-- 清理数据 
TRUNCATE TABLE feishu_chat;

-- 查询数据
select *
from feishu_chat;

-- 查询当天数据
select distinct message_id
from feishu_chat
where DATE_FORMAT(STR_TO_DATE(create_time, '%Y-%m-%d %H:%i:%s'), '%Y-%m-%d') = DATE_FORMAT(NOW(), '%Y-%m-%d')
;
