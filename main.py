#!/usr/bin/python
import os
import asyncio
import telebot
import json
from telebot import formatting
from telebot import types, util
from telebot.async_telebot import AsyncTeleBot

my_secret = os.getenv('TOKEN')
# my_secret = os.environ['bot_token']
bot = AsyncTeleBot(my_secret)


@bot.message_handler(commands=['json'])
async def send_json(message):
    js = json.dumps(message.json,
                    indent=4,
                    separators=(',', ':'),
                    ensure_ascii=False)
    await bot.reply_to(message, js)


@bot.message_handler(commands=['reply_json'])
async def send_rjson(message):
    if message.reply_to_message == None:
        return
    js = json.dumps(message.reply_to_message.json,
                    indent=4,
                    separators=(',', ':'),
                    ensure_ascii=False)
    await bot.reply_to(message, js)


@bot.message_handler(commands=['all_json'])
async def send_ajson(message):
    await bot.reply_to(message, message)


@bot.message_handler(commands=['id'])
async def get_id(message):
    id = '`' + str(message.from_user.id) + '`'
    await bot.reply_to(message, id, parse_mode='MarkdownV2')


@bot.message_handler(commands=['reply_id'])
async def get_rid(message):
    if message.reply_to_message.from_user.id == None:
        return
    id = '`' + str(message.reply_to_message.from_user.id) + '`'
    await bot.reply_to(message, id, parse_mode='MarkdownV2')


@bot.message_handler(commands=['help'])
async def send_welcome(message):
    help_text = '''
  *%s*

  *指令列表*
 /id 查询user\_id
 /json 查询message\_json
 /reply\_id 查询replymsg\_user\_id
 /reply\_json 查询message\_reply\_json
 /all\_json 查询所有json信息

  [Official Channel](https://t\.me/QsBotChannel) \| [Github](https://github\.com)
  ''' % botname
    await bot.reply_to(message,
                       help_text,
                       parse_mode='MarkdownV2',
                       disable_web_page_preview=True)

    # strp = formatting.format_text(
    #     formatting.mbold("相关"),
    #     formatting.mlink('Official Channel','https://t.me/QsBotChannel'),
    #     '/id 查询user\_id',
    #     'hello',
    #     formatting.mlink('Github','https://github.com'),
    #     separator='\n' # separator separates all strings
    #       )
    # print(strp)
    # await bot.reply_to(message,strp,
    #       parse_mode='MarkdownV2',disable_web_page_preview= True)


@bot.chat_member_handler()
async def chat_m(message: types.ChatMemberUpdated):
    old = message.old_chat_member
    new = message.new_chat_member
    if new.status == "member":
        await bot.send_message(message.chat.id,
                               "Hello {name}!".format(name=new.user.first_name)
                               )  # Welcome message


# if bot is added to group, this handler will work
@bot.my_chat_member_handler()
async def my_chat_m(message: types.ChatMemberUpdated):
    old = message.old_chat_member
    new = message.new_chat_member
    if new.status == "member":
        await bot.send_message(message.chat.id, "Somebody added me to group"
                               )  # Welcome message, if bot was added to group
        # await bot.leave_chat(message.chat.id)


@bot.message_handler(commands=['test'])
async def start_message(message):
    await bot.send_message(
        message.chat.id,
        # function which connects all strings
        formatting.format_text(
            formatting.mbold(message.from_user.first_name),
            formatting.mitalic(message.from_user.first_name),
            formatting.munderline(message.from_user.first_name),
            formatting.mstrikethrough(message.from_user.first_name),
            formatting.mcode(message.from_user.first_name),
            separator=" "  # separator separates all strings
        ),
        parse_mode='MarkdownV2')

    # just a bold text using markdownv2
    await bot.send_message(message.chat.id,
                           formatting.mbold(message.from_user.first_name),
                           parse_mode='MarkdownV2')

    # html
    await bot.send_message(
        message.chat.id,
        formatting.format_text(
            formatting.hbold(message.from_user.first_name),
            formatting.hitalic(message.from_user.first_name),
            formatting.hunderline(message.from_user.first_name),
            formatting.hstrikethrough(message.from_user.first_name),
            formatting.hcode(message.from_user.first_name),
            # hide_link is only for html
            formatting.hide_link(
                'https://telegra.ph/file/c158e3a6e2a26a160b253.jpg'),
            separator=" "),
        parse_mode='HTML')

    # just a bold text in html
    await bot.send_message(message.chat.id,
                           formatting.hbold(message.from_user.first_name),
                           parse_mode='HTML')


@bot.message_handler(commands=['del'])
async def del_msge(message):
    num = telebot.util.extract_arguments(message.text)
    print(num)
    if num == None:
        return
    else:
        id = message.id
        status = await bot.delete_message(message.chat.id, id, timeout=0.5)
        if not status:
            await bot.send_message(message.chat.id, "请检查是否具有删除消息权限")
            return
        id = id - 1
        p = 0
        for i in range(int(num)):
            if id == 1:
                return
            status = False
            while not status:
                if id == 1:
                    return
                if p > 50:
                    return
                try:
                    status = await bot.delete_message(message.chat.id,
                                                      id,
                                                      timeout=3)
                    p = 0
                except:
                    print(id)
                    id = id - 1
                    p = p + 1
            id = id - 1
            if i % 8 == 0:
                await asyncio.sleep(3)


async def main():
    global botname
    jsonkk = await bot.get_me()
    botname = jsonkk.username
    # use in for delete with the necessary scope and language_code if necessary
    await bot.delete_my_commands(scope=None, language_code=None)

    await bot.set_my_commands(
        commands=[
            telebot.types.BotCommand("id", "查询user_id"),
            telebot.types.BotCommand("json", "查询message_json"),
            telebot.types.BotCommand("reply_id", "查询replymsg_user_id"),
            telebot.types.BotCommand("reply_json", "查询message_reply_json"),
            telebot.types.BotCommand("all_json", "查询json所有信息"),
            telebot.types.BotCommand("help", "帮助菜单")
        ],
        # scope=telebot.types.BotCommandScopeChat(12345678)  # use for personal command menu for users
        # scope=telebot.types.BotCommandScopeAllPrivateChats()  # use for all private chats
    )


if __name__ == '__main__':
    botname = ''
    asyncio.run(main())
    asyncio.run(bot.polling(skip_pending=True))

