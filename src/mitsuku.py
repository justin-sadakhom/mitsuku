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


    # TODO: Uncomment the line of code below and fill in the token.
    # bot.run([your bot token])
