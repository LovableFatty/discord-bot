async def send_error(ctx, error_message: str):
    """Send a formatted error message to the context channel."""
    await ctx.send(f"❌ Error: {error_message}")


def format_quest(quest_id, description, reward, status):
    """Format a quest into a human-readable string."""
    return f"**Quest #{quest_id}:** {description}\n**Reward:** {reward} AI-Noah-Bucks\n**Status:** {status.capitalize()}"


def format_balance(user_mention, balance):
    """Format a balance message into a human-readable string."""
    return f"{user_mention} has {balance} AI-Noah-Bucks."
