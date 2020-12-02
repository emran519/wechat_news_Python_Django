-- phpMyAdmin SQL Dump
-- version 4.9.0.1
-- https://www.phpmyadmin.net/
--
-- 主机： localhost
-- 生成日期： 2020-12-02 23:26:46
-- 服务器版本： 5.6.46-log
-- PHP 版本： 7.2.24

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 数据库： `wxtest_2free_cn`
--

-- --------------------------------------------------------

--
-- 表的结构 `oreo_article`
--

CREATE TABLE `oreo_article` (
  `id` int(11) NOT NULL COMMENT '唯一ID',
  `title` text NOT NULL COMMENT '标题',
  `text` text NOT NULL COMMENT '内容',
  `title_img` text NOT NULL COMMENT '缩略图',
  `status` tinyint(4) NOT NULL COMMENT '1=>显示;2=>不显示',
  `add_time` date NOT NULL COMMENT '添加时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='新闻数据表';

--
-- 转存表中的数据 `oreo_article`
--

INSERT INTO `oreo_article` (`id`, `title`, `text`, `title_img`, `status`, `add_time`) VALUES
(10, '我校韩国留学生在2020中韩大学生演讲大赛获佳绩', '11月18日下午，由中国人民对外友好协会、中韩友好协会与韩国国际交流财团和韩中友好协会共同主办的中韩大学生演讲大赛总决赛暨颁奖仪式以线上线下相结合的方式在中国人民对外友好协会举办。\r\n\r\n我校韩国留学生禹永哲在江苏赛区预赛中获得二等奖，代表江苏赛区参加中韩大学生演讲大赛总决赛。最终，禹永哲凭借扎实的语言功底和精彩的才艺展示脱颖而出，荣获汉语组第九名。\r\n\r\n本次大赛以“道不远人、人无异国”为主题，自今年9月启动以来，吸引中韩两国大学生100余人报名参赛。经北京、山东、江苏三个分赛区的选拔比赛，共有30名选手入围总决赛。中韩大学生演讲大赛是中国人民对外友好协会创新开展“云上”中韩民间交流活动之一，两国大学生积极参赛表达了对中韩人民共享发展、共创未来的美好期待，彰显了中韩地缘相近、文缘相通、人缘相亲的友好情谊，对方国家语言分享了在疫情期间学习生活的经历，讲述了中韩守望相助、患难与共的感人故事和对后疫情时期两国友好的美好期待，以及对环境保护、气候变化、文化交流、亚洲团结、世界和平等话题的深入思考和感悟。', 'https://www.ycit.cn/__local/F/A0/06/0493AE431CF5AE89EB47B28D09F_9BA8ADAC_BBAC7.png', 1, '2020-11-21');

-- --------------------------------------------------------

--
-- 表的结构 `oreo_collect`
--

CREATE TABLE `oreo_collect` (
  `id` int(11) NOT NULL COMMENT '唯一ID',
  `user_openid` varchar(64) NOT NULL COMMENT '用户OpenId',
  `article_id` int(11) NOT NULL COMMENT '新闻ID',
  `collect_time` date NOT NULL COMMENT '收藏时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户收藏信息表';

-- --------------------------------------------------------

--
-- 表的结构 `oreo_config`
--

CREATE TABLE `oreo_config` (
  `k` varchar(200) NOT NULL,
  `v` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `oreo_config`
--

INSERT INTO `oreo_config` (`k`, `v`) VALUES
('applet_navigation_bar_color', '#1c97f5'),
('applet_navigation_bar_title', '基于WAMP高校新闻小程序'),
('applet_user_navigation_bar_color', '#1c97f5');

-- --------------------------------------------------------

--
-- 表的结构 `oreo_navigator`
--

CREATE TABLE `oreo_navigator` (
  `id` int(11) NOT NULL COMMENT '唯一ID',
  `image_src` text NOT NULL COMMENT '轮播图链接',
  `article_id` text COMMENT '文章ID',
  `status` tinyint(4) NOT NULL COMMENT '1=>展示;2=>不展示',
  `add_time` datetime NOT NULL COMMENT '添加时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='轮播图数据表';

--
-- 转存表中的数据 `oreo_navigator`
--

INSERT INTO `oreo_navigator` (`id`, `image_src`, `article_id`, `status`, `add_time`) VALUES
(8, 'https://www.ycit.edu.cn/images/9.7.jpg', '', 1, '2020-11-18 00:00:00'),
(30, 'http://php.applet.2free.cn/file/news/navigatorPhoto/2020120223255925238.png', '10', 1, '2020-12-02 23:26:04');

-- --------------------------------------------------------

--
-- 表的结构 `oreo_user`
--

CREATE TABLE `oreo_user` (
  `id` int(11) NOT NULL COMMENT '唯一ID',
  `user_openid` varchar(64) NOT NULL COMMENT '用户openid',
  `user_nickname` varchar(125) DEFAULT NULL COMMENT '微信名',
  `user_sex` tinyint(4) DEFAULT NULL COMMENT '1=>男;2=>女;3=>保密',
  `user_city` varchar(125) DEFAULT NULL COMMENT '城市',
  `user_province` varchar(125) DEFAULT NULL COMMENT '省份',
  `user_country` varchar(125) DEFAULT NULL COMMENT '国家',
  `user_headimgurl` text COMMENT '微信头像链接',
  `add_time` datetime NOT NULL COMMENT '注册时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户数据表';

--
-- 转储表的索引
--

--
-- 表的索引 `oreo_article`
--
ALTER TABLE `oreo_article`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `oreo_collect`
--
ALTER TABLE `oreo_collect`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_openid` (`user_openid`);

--
-- 表的索引 `oreo_config`
--
ALTER TABLE `oreo_config`
  ADD PRIMARY KEY (`k`);

--
-- 表的索引 `oreo_navigator`
--
ALTER TABLE `oreo_navigator`
  ADD PRIMARY KEY (`id`) USING BTREE;

--
-- 表的索引 `oreo_user`
--
ALTER TABLE `oreo_user`
  ADD PRIMARY KEY (`id`);

--
-- 在导出的表使用AUTO_INCREMENT
--

--
-- 使用表AUTO_INCREMENT `oreo_article`
--
ALTER TABLE `oreo_article`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '唯一ID', AUTO_INCREMENT=46;

--
-- 使用表AUTO_INCREMENT `oreo_collect`
--
ALTER TABLE `oreo_collect`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '唯一ID', AUTO_INCREMENT=228;

--
-- 使用表AUTO_INCREMENT `oreo_navigator`
--
ALTER TABLE `oreo_navigator`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '唯一ID', AUTO_INCREMENT=32;

--
-- 使用表AUTO_INCREMENT `oreo_user`
--
ALTER TABLE `oreo_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '唯一ID', AUTO_INCREMENT=52;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
