from bot import Bot
from commands import chat_command

if __name__ == '__main__':

    bot = Bot()


    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return

        if message.content.startswith('~chat'):
            bot.chat_count += 1

            if not bot.chat_active:
                chat_command.setup(bot.driver)
                bot.chat_active = True

            dialogue = chat_command.clean_input(message.content)
            output = chat_command.chat(dialogue, bot.driver, bot.chat_count)

            for line in output:
                await message.channel.send(line)


    bot.run('NzQ0OTM4MzI2MzY4MzIxNjI2.Xzqf4Q.O2LsHFhOqsRQdva0o8SIej4h0r8')
