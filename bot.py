from telegram.ext import Updater, CommandHandler
import requests
import json
import telegram

API_KEY = "foo_bar"

def lookup(update, context):
    try:
        print(context.args)
        #update.message.reply_text("Hello!")
        repo_dict, status_code = get_git_info(context.args[0])
        if status_code == 404:
            update.message.reply_text("User " + context.args[0] + " not found.")
            return -1
        #print(repo_dict)
        response = "forks for " + context.args[0] + "'s repositories:\n"
        for ele in repo_dict.keys():
            response += "<b>" + ele + "</b>:\t"
            response += "<b>"+ str(repo_dict.get(ele)) + "</b>"
            response += "\n"
        #response += "</table>"
        print(response)
        update.message.reply_text(
            'Hello {}, {}'.format(update.message.from_user.first_name, response), parse_mode=telegram.ParseMode.HTML)
    except Exception as e:
        print(e)
        if context.args == []:
            update.message.reply_text("Please add a GitHub username as the argument to /lookup.")


def get_git_info(entity):
    global tmp_json1
    repo_dict = {}
    try:
        resp = requests.get("https://api.github.com/users/" + entity + "/repos")
        tmp_json = json.loads(resp.text)
        #print(resp.links)
        for entry in range(len(tmp_json)):
            repo_dict.update({tmp_json[entry].get("name"): tmp_json[entry].get("forks")})
        if resp.links != {}:
            last_page = int(resp.links.get("last").get("url").split("=")[1])
            #print(last_page)
            for i in range(2, last_page + 1):
                resp_tmp = requests.get("https://api.github.com/users/" + entity + "/repos?page=" + str(i))
                #print(resp_tmp.status_code)
                tmp_json1 = json.loads(resp_tmp.text)
                for entry in range(len(tmp_json1)):
                    repo_dict.update({tmp_json1[entry].get("name"): tmp_json1[entry].get("forks")})
    except Exception as e:
        print(e)
    return repo_dict, resp.status_code

updater = Updater(API_KEY, use_context=True)

updater.dispatcher.add_handler(CommandHandler('lookup', lookup))

updater.start_polling()
updater.idle()
