def emoji_slash(votos: int, total: int, tamanho: int = 10) -> str:
    to_fill = "🟩"
    empty = "⬜"

    if total == 0:
        blocks = 0
    else:
        blocks = round((votos / total) * tamanho)

    blocks_filled = (to_fill * blocks) + (empty * (tamanho - blocks))
    return blocks_filled