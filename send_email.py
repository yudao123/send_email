# coding=utf-8

import os, sys
import json
import zipfile
import tempfile

# email_sender='yinghua.yu@daocloud.io'
# email_receivers=[email_sender]
# smtp_host='smtp.partner.outlook.cn'
# smtp_port=587
# smtp_mode='tls'
# smtp_login='yinghua.yu@daocloud.io'
# smtp_password='8u7e6Pj6fLuiFaw'

email_sender=os.getenv('EMAIL_SENDER', 'yinghua.yu@daocloud.io')
email_receivers=os.getenv('EMAIL_RECEIVERS', email_sender)
email_receivers=email_receivers.split(';')
smtp_host=os.getenv('SMTP_HOST', 'smtp.partner.outlook.cn')
smtp_port=os.getenv('SMTP_PORT', 587)
smtp_mode=os.getenv('SMTP_MODE', 'tls')
smtp_login=os.getenv('SMTP_LOGIN', email_sender)
smtp_password=os.getenv('SMTP_PASSWORD', '8u7e6Pj6fLuiFaw')

email_title = os.getenv('EMAIL_TITLE', '')
email_content = os.getenv('EMAIL_CONTENT', '')

def get_filelist():
    email_files = []
    # add first email file
    email_filename = os.getenv('EMAIL_FILE')
    if email_filename is not None:
        email_files.append(email_filename)
    i = 2
    while True:
        email_filename = os.getenv('EMAIL_FILE{}'.format(i))
        if email_filename is None:
            break
        email_files.append(email_filename)
        i += 1
    return email_files

def send_email(title, content, send_filepaths):
    import pyzmail
    attach_files = []
    for send_filepath in send_filepaths:
        filename = os.path.basename(send_filepath)
        attach_file=(open(send_filepath).read(), 'application', 'octet-stream', filename, '')
        attach_files.append(attach_file)
    payload, mail_from, rcpt_to, msg_id=pyzmail.compose_mail(email_sender, \
                    email_receivers, title, \
                    'utf-8', None, html=(content, 'utf-8'),
                    attachments=attach_files)
    ret=pyzmail.send_mail(payload, email_sender, rcpt_to, smtp_host, \
            smtp_port=smtp_port, smtp_mode=smtp_mode, \
            smtp_login=smtp_login, smtp_password=smtp_password)
    print(ret)


def zip_compress_directory(base_dir):
    '''
    compress whole directory to a temp zip file,
    and return the path of zip file
    '''
    fd, zip_filename = tempfile.mkstemp()
    print('create temp zip file : ' + zip_filename)
    os.close(fd)
    with zipfile.ZipFile(zip_filename, 'w') as fp:
        for top_dir, _, filenames in os.walk(base_dir):
            for filename in filenames:
                zip_name = os.path.join(top_dir[len(base_dir):], filename)
                filepath = os.path.join(top_dir, filename)
                fp.write(filepath, zip_name)
    return zip_filename

def make_attachments_and_send_email(base_dir):
    if not (email_title and email_content):
        raise Exception('missing email title or content')
    filelist = get_filelist()
    result_filenames = []
    for filename in filelist:
        filename = os.path.join(base_dir, filename)
        result_filename = None
        if os.path.isfile(filename):
            result_filename = filename
        elif os.path.isdir(filename):
            result_filename = zip_compress_directory(filename)
        else:
            raise Exception('attachment not found : ' + filename)
        result_filenames.append(result_filename)
    send_email(email_title, email_content, result_filenames)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        base_dir = sys.argv[1]
    else:
        base_dir = os.getcwd()
    make_attachments_and_send_email(base_dir)
