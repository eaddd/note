import itchat

# 登录微信
itchat.auto_login()
# 发送消息
itchat.send('Hello, World!', toUserName='filehelper') # 发送消息到文件助手

itchat.run()