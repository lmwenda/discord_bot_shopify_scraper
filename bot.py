import os
import time
import hikari
import lightbulb
from scraping import articles, base_url

embed_thumbail_link = "https://i.pinimg.com/originals/da/d3/c0/dad3c0f67dd0118a5fdd9abdaf0fc05e.png";
mods = [ 662074152806645783 ]
bot = lightbulb.BotApp(token="NjkzMTc5MzM2OTI0MzMyMTgy.GDR-eJ.QmeWv4nUb_bgQevGX4dcmI3aYq2kGpsIwRuSTY")

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

@lightbulb.Check
def check_author_is_mod(ctx: lightbulb.Context) -> bool:
    return ctx.author.id in mods

@bot.command
@lightbulb.add_checks(check_author_is_mod)
@lightbulb.option("reason", "Reason for the kick", required=False)
@lightbulb.option("user", "User to kick", type=hikari.User)
@lightbulb.command("kick", "Kick a user from the server")
@lightbulb.implements(lightbulb.SlashCommand)
async def kick_user(ctx: lightbulb.SlashContext) -> None:
    if not ctx.guild_id:
        await ctx.respond("This command can only be used in a server.")
        return
    
    if ctx.options.user.id in mods:
        await ctx.respond("You can't kick a moderator!")
        return

    await ctx.app.rest.kick_user(ctx.guild_id, ctx.options.user.id)
    await ctx.respond(f"{ctx.options.user.mention} has been kicked from the server by {ctx.author}\n**Reason:** {ctx.options.reason or 'No reason provided'}.")

@bot.command
@lightbulb.command("clear", "Clears the whole channel history")
@lightbulb.implements(lightbulb.SlashCommand)
async def clear_chat(ctx: lightbulb.SlashContext) -> None:
    messages = ( 
        await bot.rest.fetch_messages(ctx.channel_id)
    )

    await bot.rest.delete_messages(ctx.channel_id, messages)
    await ctx.respond(f"{ctx.author} cleared ({ctx.channel_id}) chats")

           
bot.run();
