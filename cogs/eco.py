from discord.ext import commands
import discord
from utils.default import qembed
import humanize
import time
import random
import typing

class Economy(commands.Cog, command_attrs=dict(hidden=False)):
	def __init__(self, bot):
		self.bot = bot
	
	@staticmethod
	async def get_stats(self, id: int):
		try:
			data = dict(await self.bot.db.fetchrow('SELECT wallet, bank FROM economy WHERE userid = $1', id))
			wallet = data["wallet"]
			bank = data["bank"]
		except:
			await self.bot.db.execute("INSERT INTO public.economy(userid, wallet, bank) VALUES($1, 100, 100)", id)
			data = dict(await self.bot.db.fetchrow('SELECT wallet, bank FROM economy WHERE userid = $1', id))
			wallet = data["wallet"]
			bank = data["bank"]
		return wallet, bank

	@commands.command(help='Registers you into the database')
	async def register(self, ctx):
		try:
			await self.bot.db.execute("INSERT INTO public.economy(userid, wallet, bank) VALUES($1, 100, 100)", id)
			await qembed(ctx, 'Sucessfully registered you!')
		except:
			await qembed(ctx, 'You are already registered!')

	@commands.command(help='View yours or someone elses balance', aliases=['bal'])
	async def balance(self, ctx, user: discord.Member = None):
		data = await self.get_stats(self, user.id if user else ctx.author.id)
		wallet = data[0]
		bank = data[1]
		e = discord.Embed(title=f'{user.name if user else ctx.author.name}\'s balance', description=f'<:member_join:596576726163914752> **Wallet**: ${humanize.intcomma(wallet)}\n<:member_join:596576726163914752> **Bank**: ${humanize.intcomma(bank)}\n<:member_join:596576726163914752>  **Total**: ${humanize.intcomma(wallet + bank)}', color=self.bot.embed_color, timestamp=ctx.message.created_at).set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
		e.set_thumbnail(url=user.avatar_url if user else ctx.author.avatar_url)
		await ctx.send(embed=e)

	@commands.command(help='Gets the top 5 users.', aliases=['top', 'lb', 'top5'])
	async def leaderboard(self, ctx):
		stats = await self.bot.db.fetch("SELECT * FROM economy ORDER BY bank+wallet DESC LIMIT 5")
		await ctx.send(embed=discord.Embed(title='Leaderboard', description='**TOP 5 PLAYERS:**\n```py\n' + "\n".join([f'{number}) {await self.bot.try_user(stats[number-1]["userid"])} » ${stats[number-1]["wallet"]+stats[number-1]["bank"]}' for number, i in enumerate(range(5), start=1)]) + '```', color=self.bot.embed_color, timestamp=ctx.message.created_at).set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url))
	
	@commands.command(help='Deposits a set amount into your bank', aliases=['dep'])
	async def deposit(self, ctx, amount):
		data = await self.get_stats(self, ctx.author.id)
		wallet = data[0]
		bank = data[1]
		message = 'An error occured'
		if amount.lower() == 'all':
			bank = bank + wallet
			wallete = 0
			message = f'You deposited your entire wallet of ${humanize.intcomma(wallet)}'
		else: 
			if int(amount) > wallet:
				return await qembed(ctx, 'You don\'t have that much money in your wallet.')
			if int(amount) < 0:
				return await qembed(ctx, 'How exactly are you going to deposit a negative amount of money?')
			wallete = wallet - int(amount)
			bank = bank + int(amount)
			message = f'You deposited ${humanize.intcomma(amount)}'
		await self.bot.db.execute("UPDATE economy SET wallet = $1, bank = $2 WHERE userid = $3", wallete, bank, ctx.author.id)
		await qembed(ctx, message)

	@commands.command(help='Deposits a set amount into your bank', aliases=['wd', 'with', 'withdraw'])
	async def withdrawl(self, ctx, amount):
		data = await self.get_stats(self, ctx.author.id)
		wallet = data[0]
		bank = data[1]
		message = 'An error occured'
		if amount.lower() == 'all':
			wallet = bank + wallet
			banke = 0
			message = f'You withdrew your entire bank of ${humanize.intcomma(bank)}'
		else: 
			if int(amount) > bank:
				return await qembed(ctx, 'You don\'t have that much money in your bank.')
			if int(amount) < 0:
				return await qembed(ctx, 'You can\'t exactly withdraw a negative amount of money')
			if bank < int(amount):
				return await qembed(ctx, 'You don\'t have that much money!')
			wallet = wallet + int(amount)
			banke = bank - int(amount)
			message = f'You withdrew ${humanize.intcomma(amount)}'
		await self.bot.db.execute("UPDATE economy SET wallet = $1, bank = $2 WHERE userid = $3", wallet, banke, ctx.author.id)
		await qembed(ctx, message)

	@commands.command(help='Lets you send money over to another user', alises=['send'])
	async def transfer(self, ctx, user: discord.Member, amount: typing.Union[str, int]):
		#data = self.get_stats()
		data = await self.get_stats(self, ctx.author.id)
		author_wallet = data[0]
		author_bank = data[1]

		data2 = await self.get_stats(self, user.id)
		target_wallet = data2[0]
		target_bank = data2[1]

		if isinstance(amount, int): 
			if amount > author_wallet:
				return await qembed(ctx, 'You don\'t have that much money in your wallet.')
			elif amount <= 0:
				return await qembed(ctx, f'{ctx.author.name}, it just isn\'t yet possible to send {user.name} a negative amount of money.')
			amount = int(amount)
		elif isinstance(amount, str) and amount.lower() == 'all':
			amount = author_wallet 

		author_wallet -= int(amount)
		target_wallet += int(amount)     

		await self.bot.db.execute("UPDATE economy SET wallet = $1, bank = $2 WHERE userid = $3", author_wallet, author_bank, ctx.author.id)
		await self.bot.db.execute("UPDATE economy SET wallet = $1, bank = $2 WHERE userid = $3", target_wallet, target_bank, user.id)

		await qembed(ctx, f'You gave {user.mention} ${humanize.intcomma(amount)}')

	@commands.command(help='Takes a random amount of $ from someone', alises=['mug', 'steal'])
	async def rob(self, ctx, user: discord.Member):
		data = await self.get_stats(self, ctx.author.id)
		author_wallet = data[0]
		author_bank = data[1]

		data2 = await self.get_stats(self, user.id)
		target_wallet = data2[0]
		target_bank = data2[1]

		if target_wallet == 0:
			return await qembed(ctx, 'That user has no money in their wallet. Shame on you for trying to rob them.')

		amount = random.randint(1, target_wallet)

		author_wallet += int(amount)
		target_wallet -= int(amount)

		await self.bot.db.execute("UPDATE economy SET wallet = $1, bank = $2 WHERE userid = $3", author_wallet, author_bank, ctx.author.id)
		await self.bot.db.execute("UPDATE economy SET wallet = $1, bank = $2 WHERE userid = $3", target_wallet, target_bank, user.id) 

		await qembed(ctx, f'You stole ${humanize.intcomma(amount)} from {user.mention}!')

	@commands.command(help='Work for some $$$')
	@commands.cooldown(rate=1, per=7200, type=commands.BucketType.user)
	async def work(self, ctx):
		data = await self.get_stats(self, ctx.author.id)
		author_wallet = data[0]
		author_bank = data[1]

		cash = random.randint(100, 500)
		await self.bot.db.execute("UPDATE economy SET wallet = $1, bank = $2 WHERE userid = $3", author_wallet + cash, author_bank, ctx.author.id)
		if cash >= 250:
			amount = 'handsome'
		if cash <= 249:
			amount = 'meager'
		await qembed(ctx, f'You work and get paid a {amount} amount of ${cash}.')


	@commands.command(help='Daily reward')
	@commands.cooldown(rate=1, per=86400, type=commands.BucketType.user)
	async def daily(self, ctx):
		data = await self.get_stats(self, ctx.author.id)
		cash = random.randint(500, 700)
		await self.bot.db.execute("UPDATE economy SET wallet = $1, bank = $2 WHERE userid = $3", data[0] + cash, data[1], ctx.author.id)
		await qembed(ctx, f'You collected ${cash} from the daily gift!')
			

	@commands.command(help='Fish in order to get some money.')
	@commands.cooldown(rate=1, per=7200, type=commands.BucketType.user)
	async def fish(self, ctx):
		data = await self.get_stats(self, ctx.author.id)
		price = random.randint(20, 35)
		fish = random.randint(5, 20)
		cash = price * fish
		await self.bot.db.execute("UPDATE economy SET wallet = $1, bank = $2 WHERE userid = $3", data[0] + cash, data[1], ctx.author.id)
		emoji = ['🐟', '🐠', '🐡']
		await qembed(ctx, f'You travel to the local lake and catch {fish} fish {random.choice(emoji)}. Then you sell them to the market at a price of ${price}, totaling in at ${cash} for a days work.')

	@commands.command(help='Beg in the street')
	@commands.cooldown(rate=1, per=200, type=commands.BucketType.user)
	async def beg(self, ctx):
		async with self.bot.session.get('https://pipl.ir/v1/getPerson') as f:
			cities = await f.json()
		data = await self.get_stats(self, ctx.author.id)
		gender = ['man', 'woman']
		cash = random.randint(0, 500)
		await self.bot.db.execute("UPDATE economy SET wallet = $1, bank = $2 WHERE userid = $3", data[0] + cash, data[1], ctx.author.id)
		await qembed(ctx, f'You sit on the streets of {cities["person"]["personal"]["city"]} and a nice {random.choice(gender)} hands you ${cash}.')

def setup(bot):
	bot.add_cog(Economy(bot))