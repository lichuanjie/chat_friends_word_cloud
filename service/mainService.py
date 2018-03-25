from service.RockWordCloud import RockWordCloud
import os
import chat_friend_image 

if __name__ == '__main__':

    ##chat_friend_image.write_friend_file()
    #chat_friend_image.send_chat_split_image()
    #chat_friend_image.write_friend_file()

    module_path = os.path.dirname(os.path.dirname(__file__))
    rockCloud = RockWordCloud(module_path + "/document/friends.txt",
                              module_path + "/wordLexicon/SourceHanSerifSC-SemiBold.otf",
                              module_path + "/images")

    file_path = module_path+"/images/13.jpg"
    save_file = rockCloud.build_backgroud_image(file_path)

    chat_friend_image.send_image_to_myself(save_file)
    chat_friend_image.send_image_to_myself(file_path)
