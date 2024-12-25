import discord
from discord.ext import commands
from utils import send_error, format_balance
from database import db_cursor, db_conn


class BalanceCommands(commands.Cog):
    def __init__(self, bot, user_id):
        self.bot = bot
        self.user_id = user_id

    @commands.command(name='balance', help='Check your or another player\'s AI-Noah-Bucks balance. Usage: !balance [@player]')
    async def balance(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        db_cursor.execute(
            "SELECT balance FROM balances WHERE user_id = ?", (member.id,))
        result = db_cursor.fetchone()
        if result:
            await ctx.send(format_balance(member.mention, result[0]))
        else:
            await ctx.send(format_balance(member.mention, 0))

    @commands.command(name='award', help='Award AI-Noah-Bucks to a player. Usage: !award @player amount')
    async def award(self, ctx, member: discord.Member, amount: int):
        if ctx.author.id == self.user_id:
            db_cursor.execute(
                "INSERT OR IGNORE INTO balances (user_id, balance) VALUES (?, ?)", (member.id, 0))
            db_cursor.execute(
                "UPDATE balances SET balance = balance + ? WHERE user_id = ?", (amount, member.id))
            db_conn.commit()
            await ctx.send(f'{member.mention} has been awarded {amount} AI-Noah-Bucks!')
        else:
            await send_error(ctx, "You do not have permission to award AI-Noah-Bucks.")

    @commands.command(name='deduct', help='Deduct AI-Noah-Bucks from a player. Usage: !deduct @player amount')
    async def deduct(self, ctx, member: discord.Member, amount: int):
        if ctx.author.id == self.user_id:
            db_cursor.execute(
                "SELECT balance FROM balances WHERE user_id = ?", (member.id,))
            result = db_cursor.fetchone()
            if result and result[0] >= amount:
                db_cursor.execute(
                    "UPDATE balances SET balance = balance - ? WHERE user_id = ?", (amount, member.id))
                db_conn.commit()
                await ctx.send(f'{amount} AI-Noah-Bucks have been deducted from {member.mention}.')
            else:
                await send_error(ctx, f'{member.mention} does not have enough AI-Noah-Bucks.')
        else:
            await send_error(ctx, "You do not have permission to deduct AI-Noah-Bucks.")
