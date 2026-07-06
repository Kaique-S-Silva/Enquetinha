import discord

from src.utils.formatting import emoji_slash

def update_embed(embed: discord.Embed, counts: dict[str, int], end: bool = False) -> discord.Embed:

    total = sum(counts.values())

    for index, option in enumerate(embed.fields):
        if not option.name:
            continue

        votes = counts.get(option.name, 0)

        value = f"{emoji_slash(votes, total)}\n↳ **{votes}** votos"

        embed.set_field_at(
            index=index,
            name=option.name,
            value=value,
            inline=option.inline
        )

    if end:
        embed.description = f"## ⌛ Enquete encerrada!"
        embed.color = discord.Color.red()

        if total > 0:
            max_votos = max(counts.values())
            winners = [name for name, votos in counts.items() if votos == max_votos]
            winners_text = ", ".join(winners)

            value = f"` {winners_text} `"
            
            if len(winners) > 1:
                embed.add_field(
                    name="🏆 Vencedores:",
                    value=value,
                    inline=False
                )
            else:
                embed.add_field(
                    name="🏆 Vencedor:",
                    value=value,
                    inline=False
                )

    return embed