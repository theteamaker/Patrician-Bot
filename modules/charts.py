import discord,re
from discord.ext import commands
from discord.ext.commands import BucketType



class charts():
	def __init__(self,bot):
		self.bot=bot
		self.pool=bot.pool


	@commands.group(pass_context=True)
	async def chart(self,ctx):
		if ctx.invoked_subcommand is None:
			try:
				async with self.pool.acquire() as conn:
					val = await conn.fetchval('SELECT chart FROM users WHERE userid = $1',int(ctx.message.author.id))
				await self.bot.say(val)
			except:
				await self.bot.say('Your chart isn\'t in the database , fix this by doing `!chart submit imagelinkhere`')
	
	@chart.command(pass_context=True, description = 'Use this to submit your chart')
	async def submit(self,ctx,link:str):
		await self.bot.send_typing(ctx.message.channel)
		Regex = re.compile(
			'^https://.*\.com/.+(\.jpg|\.png|\.jpeg)$|^http://.*\.com/.+(\.jpg|\.png|\.jpeg)$|.*\.com/.+(\.jpg|\.png|\.jpeg)$')
		try:
			var = Regex.search(link)
			if var is not None:
				async with self.pool.acquire() as conn:
					try:
						await conn.execute('''INSERT INTO users(userid,chart) VALUES($1,$2)''',int(ctx.message.author.id),link)
					except:
						await conn.execute('''UPDATE users SET chart = $1 WHERE userid = $2''',link,int(ctx.message.author.id))
					await self.bot.say("Your chart has been submitted, you may call it using !chart")
			elif var is None:
				await self.bot.say("Invalid Input.")

		except Exception as e:
			print(e)
			await self.bot.say("Invalid Input")


	
	@chart.command(pass_context=True , description= "Tag whoever's chart you want to judge. example: !chart get @Amb1tion#6969")
	async def get(self,ctx,m:discord.Member):
		await self.bot.send_typing(ctx.message.channel)
		async with self.pool.acquire() as conn:
			try:
				val = await conn.fetchval('SELECT chart FROM users WHERE userid = $1',int(m.id))
				await self.bot.say(val)
			except:
				await self.bot.say('Something went wrong , maybe they haven\'t submitted a chart yet?')

def setup(bot):
	bot.add_cog(charts(bot))
