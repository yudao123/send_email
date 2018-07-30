# 纯邮件发送脚本

命令: python /opt/send_email/send_email.py

镜像: daocloud.io/dc_pokeman/send_email:latest

功能描述: 该命令用于发送一封邮件，邮件发送方式和内容由环境变量决定

配置方式：环境变量

表格：

| 环境变量名称          | 含义     | 备注                                       | 是否必填 |
| --------------- | ------ | ---------------------------------------- | ---- |
| EMAIL_SENDER    | 发件人    |                                          | 是    |
| EMAIL_RECEIVERS | 收件人    | 多个收件人以(;)分号间隔，不填则与发件人相同                  |      |
| SMTP_HOST       | SMTP主机 | 需要咨询邮件运营商                                | 是    |
| SMTP_PORT       | SMTP端口 | 需要咨询邮件运营商，默认587                          | 是    |
| SMTP_MODE       | SMTP模式 | 默认为tls                                   |      |
| SMTP_LOGIN      | 邮箱账户名  | 默认与发件人相同                                 |      |
| SMTP_PASSWORD   | 邮箱密码   | 密码必填，填错会导致邮件发送失败                         | 是    |
| EMAIL_TITLE     | 邮件标题   |                                          | 是    |
| EMAIL_CONTENT   | 邮件内容   |                                          | 是    |
| EMAIL_FILE      | 附件路径   | 附件路径，文件或目录不存在则报错                         |      |
| EMAIL_FILE2     | 附件路径   | 追加附件路径，文件或目录不存在则报错。可以有EMAIL_FILE3一直到EMAIL_FILEN，整数不可间隔，如有间隔，到中断的整数为止 |      |
