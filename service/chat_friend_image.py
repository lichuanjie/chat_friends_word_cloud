# codding=UTF-8
import itchat
import os

import PIL.Image as Image
from os import listdir
import math
import shutil
import codecs


def login():
    itchat.auto_login(hotReload=True)  # hotReload=True


"""
获取登录用户所有的朋友信息
"""


def get_friends():
    itchat.auto_login(hotReload=True)
    friends = itchat.get_friends(update=True)[0:]
    count = len(friends)
    print("member count:" + str(count))
    for i in range(0, count):
        sex_name = ('男' if friends[i]['Sex'] == 1 else '女')
        print("所在城市:" + friends[i]['Province'] + "；性别：" + sex_name + "；昵称：" + friends[i]['NickName'])

    return friends


"""
保存登录用户所有的朋友头像地址到本地
"""


def save_friend_image(login_user_file_name):
    num = 0
    friends = get_friends()
    for i in friends:
        img = itchat.get_head_img(userName=i["UserName"])
        fileName = login_user_file_name + "/" + i["UserName"] + ".jpg"
        fileImage = open(fileName, 'wb')
        fileImage.write(img)
        fileImage.close()
        print("write local image:" + fileName)
        num += 1


"""
把文件夹中的图片整合一张图片
"""


def split_one_image(login_user_file_name):
    pics = listdir(login_user_file_name)
    numPic = len(pics)
    print("your friends images count is :" + str(numPic))
    eachsize = int(math.sqrt(float(1200 * 1200) / numPic))
    print(eachsize)
    numline = int(1200 / eachsize)
    toImage = Image.new('RGB', (1200, 1200))
    print(numline)
    x = 0
    y = 0
    for i in pics:
        try:
            img = Image.open(login_user_file_name + "/" + i)
        except IOError:
            print("Error: ")
        else:
            img = img.resize((eachsize, eachsize), Image.ANTIALIAS)
            toImage.paste(img, (x * eachsize, y * eachsize))
            x += 1
            if x == numline:
                x = 0
                y += 1

    toImage.save(login_user_file_name + ".jpg")


"""
发送整合的图片
"""


def send_chat_split_image():
    login()
    # 获取自己的用户信息，返回自己的属性字典
    login_user_obj = itchat.search_friends()
    login_user = login_user_obj["UserName"]
    print(login_user)

    # os.removedirs(login_user)
    if os.path.exists(login_user):
        shutil.rmtree(login_user)

    os.mkdir(login_user)
    # save all friend image local
    save_friend_image(login_user)
    split_one_image(login_user)
    #send_user_obj = itchat.search_friends(nickName='笨石头')
    #send_userName = send_user_obj[0]["UserName"]
    #itchat.send_msg("hello send you a big image", toUserName=send_userName)
    #itchat.send_image(login_user + ".jpg", toUserName=send_userName)
    itchat.send_image(login_user + ".jpg", "filehelper")


def write_friend_file():
    friends = get_friends()
    module_path_file = os.path.dirname(os.path.dirname(__file__)) + "/document/friends.txt"
    if os.path.exists(module_path_file):
        os.remove(module_path_file)

    f = codecs.open(module_path_file, 'w', encoding='utf-8')
    for m in friends:
        f.writelines(m["NickName"] + "\n")
        print(m["NickName"])

    f.close()

def send_image_to_myself(file_path):
    login()
    itchat.send_image(file_path, "filehelper")
    print("send success")
#if __name__ == '__main__':
    #write_friend_file()
    # send_chat_split_image()
