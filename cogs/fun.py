from discord.ext import commands
import discord
import os
import aiohttp
import onetimepad
import asyncio
import random
from owotext import OwO
import random
from iso639 import languages
import async_google_trans_new
import datetime
import time
import lyricsgenius
import utils.embed as qembed
geniustoken = os.environ['genius']
genius = lyricsgenius.Genius(geniustoken)
flipnotetoken = os.environ['tflipnote']
nasakey = os.environ['nasakey']


class fun(commands.Cog):
    """For the fun commands"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='smolpp',
                      hidden=True,
                      help='Tells someone that they have a smol pp')
    async def smolpp(self, ctx, *, thing):
        message = thing.capitalize()
        if message == ('You', 'I', 'They'):
            await qembed.send(ctx, f'{message} have a smol pp')
        else:
            await qembed.send(ctx, f'{message} has a smol pp')

    @commands.command(name='garsh', hidden=True)
    async def garsh(self, ctx):
        await qembed.send(
            ctx,
            'ASTRELLA OUTDATED <:Pog:790609728782073876> CERRET OVERRATED <:Pog:790609728782073876> GARSH ACTIVATED'
        )

    @commands.command(name='copypasta', hidden=True)
    async def copypasta(self, ctx):
        await ctx.send(
            'https://media.discordapp.net/attachments/788422986717200444/790627982813036580/Screenshot_2020-12-21_at_11.10.48_AM.png'
        )
        await ctx.send(
            'https://media.discordapp.net/attachments/788422986717200444/790627978774183936/Screenshot_2020-12-21_at_11.13.03_AM.png'
        )
        await ctx.send(
            'https://media.discordapp.net/attachments/788422986717200444/790627980681543730/Screenshot_2020-12-21_at_11.11.47_AM.png'
        )

    @commands.command(name='astrelladies',
                      help='The gif astrella used as he was losing the match')
    async def fakeembed(self, ctx):
        embed = discord.Embed(title='he ded',
                              description='can we get an f in the chat',
                              color=self.bot.embed_color, timestamp=ctx.message.created_at).set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        embed.set_image(
            url=
            'https://media.tenor.com/images/b5e65cd0e7a8c8fef19af759a29d1acd/tenor.gif'
        )

        await ctx.send(embed=embed)


    @commands.command(
        name='translate',
        help='Translates text into another language with Google Translate')
    async def gtr(self, ctx, language, *, text: str):
        language = language.capitalize()
        try:
            try:
                lang = languages.get(name=language)
                g = async_google_trans_new.google_translator()
                gemb = discord.Embed(title='Google Translation',
                                    color=self.bot.embed_color, timestamp=ctx.message.created_at).set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                gemb.add_field(name='Input:', value=f'```\n{text}\n```')
                gemb.add_field(
                    name=f'Output in {language}:',
                    value=f'```\n{await g.translate(text, lang.alpha2)}\n```',
                    inline=False)
                await ctx.send(embed=gemb)
            except KeyError:
                await qembed.send(ctx, 'Language not found.')
        except TypeError:
            await qembed.send(ctx, 'This is different from other translate commands. In this, you actually say the language. `en` becomes `english`.')

    @commands.command(help='Finds the PPSIZE of a user')
    async def ppsize(self, ctx, user: discord.Member = None):
        user = user.name if user else ctx.author.name
        async with self.bot.session.get(
                'https://www.potatoapi.ml/ppsize') as f:
            f = await f.json()
            e = discord.Embed(title=f'{user}\'s ppsize:',
                              description=f['size'],
                              color=self.bot.embed_color, timestamp=ctx.message.created_at).set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=e)

    @commands.command(name='multiply', help='Multiplies a saying.')
    async def multiply(self, ctx, times: int, *, message=None):
        if ctx.author.id != self.bot.owner_id and times > 10:
            await qembed.send(ctx, 'No more than 10 times.')
        else:
            await qembed.send(ctx, f'{message} ' * times)

    @commands.command(help='Rascal MVP?')
    async def rascal(self, ctx):
        await qembed.send(
            ctx,
            'I cannot believe it. I can NOT fucking believe it. I simply REFUSE to believe the absolute imcompetent, negligence, of actually not, for ANY of these categories whatsoever, not picking up FUCKING Rascal. This guy doesn\'t get props by anyone, on no one\'s social media radar whatsoever. Everyone\'s talking about like "oh Smurf, ya know, Smurf he\'s-- poor Smurf!" think about Rascal! He literally came into the league at the start of the year, was the BEST Mei. He revolutionized the way you play Echo, and set the guidelines for everyone else in the league for MONTHS! Or pretty much like half the season! And then he comes into the Countdown Cup and plays the Genji, that actually turns the SanFranciscoShockaroundandtheywintheseriesagainstthePhiladelphiaFusion! How is NO ONE, on this PLANET talking about Rascal as one of the most underrated players of the year! It\'s absolutely... HURTING MY SOUL!'
        )

    @commands.command(name='lyrics', help='WIP', hidden=True)
    async def lyric(self, ctx, *, songname):
        cs = aiohttp.ClientSession()
        song = await cs.get('')

    @commands.command(help='Checks your speed.')
    async def react(self, ctx, seconds: int=None):
        if seconds and seconds > 31:
            return await qembed.send(ctx, 'You cannot specify more than 30 seconds. Sorry.')
        emg = str(random.choice(self.bot.emojis))
        if not seconds:
            seconds = 5
        embed = discord.Embed(description=f'React to this message with {emg} in {seconds} seconds.', timestamp=ctx.message.created_at, color=self.bot.embed_color).set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        msg = await ctx.send(embed=embed)
        await msg.add_reaction(emg)
        start = time.perf_counter()
        def gcheck(reaction, user):
            return user == ctx.author and str(reaction.emoji) == emg
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=seconds * 1.5, check=gcheck)
        except asyncio.TimeoutError:
            embed = discord.Embed(description='You did not react in time', timestamp=ctx.message.created_at, color=self.bot.embed_color).set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await msg.edit(embed=embed)
        else:
            end = time.perf_counter()
            tim = end - start
            embed = discord.Embed(description=f'You reacted in **{tim:.2f}** seconds, **{seconds - tim:.2f}** off.', timestamp=ctx.message.created_at, color=self.bot.embed_color).set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await msg.edit(embed=embed)
                

    @commands.command(name='chucknorris',
                      aliases=['norris', 'chucknorrisjoke'],
                      help='Gets a random Chuck Norris Joke')
    async def norris(self, ctx):
        data = await self.bot.session.get(
            'https://api.chucknorris.io/jokes/random')
        joke = await data.json()
        e = discord.Embed(title='Chuck Norris Joke',
                          url=joke['url'],
                          description=joke['value'],
						  color=self.bot.embed_color, timestamp=ctx.message.created_at).set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        e.set_thumbnail(url=joke['icon_url'])
        await ctx.send(embed=e)

    @commands.command(help='Sends a waifu')
    async def waifu(self, ctx, user: discord.Member = None):
        if not user:
            user = ctx.author
        async with self.bot.session.get(
                'https://waifu.pics/api/sfw/waifu'
        ) as waifu:  # https://waifu.pics/docs DOCS
            waifu = await waifu.json()
            w = discord.Embed(title=f'Waifu for {user.name}', color=self.bot.embed_color, timestamp=ctx.message.created_at).set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            w.set_image(url=waifu['url'])
            await ctx.send(embed=w)

    @commands.command(
        help=
        'NASA Picture of the day. Optional date arg should be formatted like YYYY-MM-DD'
    )
    async def nasa(self, ctx, dateintime=None):
        try:
            if dateintime is None:
                dateintime = datetime.datetime.utcnow().strftime("%Y-%m-%d")
            async with self.bot.session.get(
                    f'https://api.nasa.gov/planetary/apod?date={dateintime}&api_key={nasakey}'
            ) as nasa:
                nasa = await nasa.json()
            nemb = discord.Embed(
                title=f'NASA Image of the day for {dateintime}',
                description=nasa['explanation'][:1024], color=self.bot.embed_color, timestamp=ctx.message.created_at).set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            try:
                nemb.add_field(name=nasa['title'])
            except TypeError:
                pass
            nemb.set_image(url=nasa['url'])
            await ctx.send(embed=nemb)
        except KeyError:
            await ctx.send('Enter a valid date please!')

    @commands.command(help='Gets a random cat fact')
    async def catfact(self, ctx):
        async with self.bot.session.get(
                'https://cat-fact.herokuapp.com/facts/random?animal_type=cat&amount=1'
        ) as cat:
            cat = await cat.json()
        async with self.bot.session.get(
                'https://api.thecatapi.com/v1/images/search') as catimg:
            catimg = await catimg.json()
        catemb = discord.Embed(title='Random Cat Fact',
                               description=cat['text'],
							   color=self.bot.embed_color, timestamp=ctx.message.created_at).set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        catemb.set_thumbnail(url=catimg[0]['url'])
        await ctx.send(embed=catemb)

    @commands.command(help='Gets a random image of a cat')
    async def cat(self, ctx):
        async with self.bot.session.get(
                'https://api.thecatapi.com/v1/images/search') as catimg:
            catimg = await catimg.json()
        catemb = discord.Embed(title='Random Cat', color=self.bot.embed_color, timestamp=ctx.message.created_at).set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        catemb.set_image(url=catimg[0]['url'])
        await ctx.send(embed=catemb)

    @commands.command(help='OwO owoifys a text stwing ( ͡° ᴥ ͡°)')
    async def owoify(self, ctx, *, text: str):
        uwu = OwO()
        await qembed.send(ctx, uwu.whatsthis(text))

    @commands.command(help='Gets a random comic from XKCD')
    async def xkcd(self, ctx, query: int = None):
        async with ctx.typing():
            if isinstance(query, int):
                num = query
            else:
                async with self.bot.session.get(
                        "https://xkcd.com/info.0.json") as resp:
                    max_num = (await resp.json())["num"]
                    num = random.randint(1, max_num)

            async with self.bot.session.get(
                    f"https://xkcd.com/{num}/info.0.json") as resp:
                if resp.status in range(400, 500):
                    return await ctx.send(
                        "Couldn't find a comic with that number.")
                elif resp.status >= 500:
                    return await ctx.send("Server error.")
                data = await resp.json()

            embed = discord.Embed(
                title=f"{data['safe_title']} (Number `{data['num']}`)",
                description=data["alt"],
                colour=self.bot.embed_color, timestamp=ctx.message.created_at).set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            embed.set_image(url=data["img"])
            await ctx.send(embed=embed)

    @commands.command(name='monke', help='reject discord return to monke')
    async def monk(self, ctx, monke: discord.Member = None):
        monke = f"{monke.mention}, " if monke else ""
        await qembed.send(
            ctx,
            f"https://tenor.com/view/reject-modernity-return-to-monke-monke-gif-19167526\n{monke}return to monke"
        )

    @commands.command(help='Encrypts a message')
    async def encrypt(self, ctx, *, message: str):
        cipher = onetimepad.encrypt(message, 'a_random_key')
        gemb = discord.Embed(title='Encryption', color=self.bot.embed_color, timestamp=ctx.message.created_at).set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        gemb.add_field(name='Input:', value=f'```\n{message}\n```')
        gemb.add_field(name='Output:',
                       value=f'```\n{cipher}\n```',
                       inline=False)
        await ctx.send(embed=gemb)

    @commands.command(help='Decrypts a message')
    async def decrypt(self, ctx, *, text: str):
        msg = onetimepad.decrypt(text, 'a_random_key')
        gemb = discord.Embed(title='Decryption', color=self.bot.embed_color, timestamp=ctx.message.created_at).set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        gemb.add_field(name='Input:', value=f'```\n{text}\n```')
        gemb.add_field(name='Output:', value=f'```\n{msg}\n```', inline=False)
        await ctx.send(embed=gemb)

    @commands.command(help='translates some text into pig latin')
    async def piglatin(self, ctx, *, text: str):
        async with self.bot.session.get(
                f'https://www.potatoapi.ml/piglatin?text={text}') as resp:
            resp = await resp.json()
            emb = discord.Embed(title='Pig Latin!', color=self.bot.embed_color, timestamp=ctx.message.created_at).set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            emb.add_field(name='Input:', value=f'```\n{text}\n```')
            emb.add_field(name='Output:',
                          value=f'```\n{resp["text"]}\n```',
                          inline=False)
            await ctx.send(embed=emb)


def setup(bot):
    bot.add_cog(fun(bot))
