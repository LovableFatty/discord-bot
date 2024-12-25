import discord
from discord.ext import commands
from utils import send_error, format_quest
from database import db_cursor, db_conn


class QuestCommands(commands.Cog):
    def __init__(self, bot, user_id):
        self.bot = bot
        self.user_id = user_id

    @commands.command(name='create_quest', help='Create a new quest. Usage: !create_quest reward description')
    async def create_quest(self, ctx, reward: int, *, description: str):
        if ctx.author.id == self.user_id:
            # Insert quest into database
            db_cursor.execute(
                "INSERT INTO quests (description, reward, status) VALUES (?, ?, 'open')", (
                    description, reward)
            )
            db_conn.commit()
            quest_id = db_cursor.lastrowid

            # Post the quest to the quest board channel
            quest_board = discord.utils.get(
                ctx.guild.channels, name="quest-board")
            if quest_board:
                await quest_board.send(format_quest(quest_id, description, reward, 'open'))
                await ctx.send(f"Quest #{quest_id} created successfully!")
            else:
                await send_error(ctx, "Quest board channel not found.")
        else:
            await send_error(ctx, "You do not have permission to create quests.")

    @commands.command(name='list_quests', help='Lists all available quests.')
    async def list_quests(self, ctx):
        # Fetch all open quests from the database
        db_cursor.execute(
            "SELECT quest_id, description, reward, status FROM quests WHERE status = 'open'"
        )
        quests = db_cursor.fetchall()

        # Format and send the response
        if quests:
            response = "**Available Quests:**\n" + "\n".join(
                [format_quest(quest[0], quest[1], quest[2], quest[3])
                 for quest in quests]
            )
            await ctx.send(response)
        else:
            await send_error(ctx, "No quests are currently available.")

    @commands.command(name='complete_quest', help='Mark a quest as completed and reward the player. Usage: !complete_quest quest_id @player')
    async def complete_quest(self, ctx, quest_id: int, member: discord.Member):
        if ctx.author.id == self.user_id:
            # Fetch the quest from the database
            db_cursor.execute(
                "SELECT reward, status FROM quests WHERE quest_id = ?", (quest_id,))
            quest = db_cursor.fetchone()

            if quest and quest[1] == 'open':
                reward = quest[0]

                # Mark quest as completed and reward the player
                db_cursor.execute(
                    "UPDATE quests SET status = 'completed', player_id = ? WHERE quest_id = ?", (
                        member.id, quest_id)
                )
                db_cursor.execute(
                    "INSERT OR IGNORE INTO balances (user_id, balance) VALUES (?, ?)", (
                        member.id, 0)
                )
                db_cursor.execute(
                    "UPDATE balances SET balance = balance + ? WHERE user_id = ?", (
                        reward, member.id)
                )
                db_conn.commit()

                await ctx.send(f"Quest #{quest_id} has been completed by {member.mention}! They have been awarded {reward} AI-Noah-Bucks.")
            else:
                await send_error(ctx, "Invalid quest ID or the quest is not available.")
        else:
            await send_error(ctx, "You do not have permission to mark quests as completed.")

    @commands.command(name='completed_quests', help='Lists all completed quests.')
    async def completed_quests(self, ctx):
        # Fetch all completed quests from the database
        db_cursor.execute(
            "SELECT quest_id, description, reward, player_id FROM quests WHERE status = 'completed'"
        )
        quests = db_cursor.fetchall()

        # Format and send the response
        if quests:
            response = "**Completed Quests:**\n"
            for quest in quests:
                # Fetch user information
                player = await self.bot.fetch_user(quest[3])
                response += (
                    f"**Quest #{quest[0]}:** {quest[1]} - Reward: {quest[2]} AI-Noah-Bucks - Completed by {player.mention}\n"
                )
            await ctx.send(response)
        else:
            await send_error(ctx, "No quests have been completed yet.")
