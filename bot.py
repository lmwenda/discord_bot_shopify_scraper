import os
import time
import hikari
import lightbulb
from scraping import articles, base_url

embed_thumbail_link = "https://comicvine.gamespot.com/a/uploads/original/11141/111416458/7392637-8009724742-7310212-4422353572-latest";

token = str(os.getenv("DISCORD_TOKEN"))
bot = lightbulb.BotApp(token="NjkzMTc5MzM2OTI0MzMyMTgy.G2LpIF.hr6mqax_aRo0zgmPd-eoH089iN6a2uh4Hcw5gs")

@bot.listen(hikari.StartedEvent)
async def on_started(event):
    print(f'Judgement has now awakened...')

@bot.listen(lightbulb.CommandErrorEvent)
async def on_error(event: lightbulb.CommandErrorEvent) -> None:
    if isinstance(event.exception, lightbulb.CommandInvocationError):
        await event.context.respond(f"Something went wrong during this command event fired: `{event.context.command.name}`.")
        raise event.exception

    # Unwrap the exception to get the original cause
    exception = event.exception.__cause__ or event.exception

    if isinstance(exception, lightbulb.NotOwner):
        await event.context.respond("You are not the captain of this bot.")
    elif isinstance(exception, lightbulb.CommandIsOnCooldown):
        await event.context.respond(f"This command is on cooldown. Retry in `{exception.retry_after:.2f}` seconds.")
    elif ...:
        ...
    else:
        raise exception

@bot.listen(hikari.GuildMessageCreateEvent)
async def log_messages(event: hikari.Event):
    print(f'({event.author}) {event.content} ({event.channel_id})')

@bot.command
@lightbulb.command('hello', 'Hello Message')
@lightbulb.implements(lightbulb.SlashCommand)
async def say_hello(ctx: lightbulb.Context):
    await ctx.respond("Hello")

@bot.command
@lightbulb.command('bye', 'Bye Message')
@lightbulb.implements(lightbulb.SlashCommand)
async def say_hello(ctx: lightbulb.Context):
    await ctx.respond("Bye")

@bot.command
@lightbulb.command('creator', 'Shows the Creator of the Bot')
@lightbulb.implements(lightbulb.SlashCommand)
async def say_hello(ctx: lightbulb.Context):
    await ctx.respond("maetyu! oh.. wait... PANGUUUUUU")

@bot.command()
@lightbulb.command("articles", "Sends Embeds of Business Articles")
@lightbulb.implements(lightbulb.SlashCommand)
async def send_articles(ctx: lightbulb.Context):
    for article in articles:
        _article_link = article.find('a', class_ = "article--index__link")

        article_link = str(base_url+_article_link['href']);
        article_title = str(_article_link.text);

        article = {
            "title": article_title,
            "href": article_link
        }

        print(article)

        embed_message = hikari.Embed(title=article_title, description=article_link, color=0x00ff00, url=embed_thumbail_link)
        embed_message.set_thumbnail(embed_thumbail_link)
        await ctx.respond(embed_message)
        time.sleep(0.7)

@bot.command
@lightbulb.option("text", "text to repeat", modifier=lightbulb.OptionModifier.CONSUME_REST)
@lightbulb.command("echo", "the bot will mimic your text")
@lightbulb.implements(lightbulb.SlashCommand)
async def echo(ctx: lightbulb.Context) -> None:
    await ctx.respond(ctx.options.text)


@bot.command
@lightbulb.command("clear", "Clears the Chat")
@lightbulb.implements(lightbulb.SlashCommand)
async def clear_chat(ctx):
    pass

           
bot.run();
