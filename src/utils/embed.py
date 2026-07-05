import discord

from src.utils.formatting import emoji_slash

def update_embed(embed: discord.Embed, counts: dict[str, int]) -> discord.Embed:
    total = sum(counts.values())
    for index, option in enumerate(embed.fields):
        if not option.name:
            continue
        votes = counts.get(option.name, 0)
        embed.set_field_at(
            index=index,
            name=option.name,
            value=f"{emoji_slash(votes, total)} {votes} votos",
            inline=option.inline
        )
    return embed