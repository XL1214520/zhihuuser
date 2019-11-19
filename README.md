# zhihuuser
爬取知乎用户信息

流程：
一、首先获取用户的主页，和个人信息，


二、解析个人信息函数里  （parse_user）
解析个人信息 返回给item
两件事：
1.继续调用获取自己关注列表
2.继续调用获取自己粉丝列表


三、解析关注列表   （parse_follows）
解析关注列表里每一位用户
两件事
1.获取每一个用户后，调用个人信息函数
2.判断next是否为False,如果为False继续回调此函数


四、解析粉丝列表  （parse_followers）
解析分析列表里的每一个用户
两件事
1.获取每一个用户后，调用个人信息函数
2.判断next是否为False，如果为False继续回调此函数


五、解析完后的数据，保存到Mongodb数据库里，使用update方法去重，


1.第一个参数传入查询的条件，这里使用url_token，
2.第二个参数传入字典类型的对象，也就是item,
3.第三个参数传入True，如果查询数据存在的话就更新，不存在的话就插入，保证数据不会重复。
self.post.update({"url_token":item['url_token']},{'$set':item},True)
