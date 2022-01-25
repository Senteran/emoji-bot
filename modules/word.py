import discord

letter_to_emojis = {
    'a' : [['e', 'e', 'e'],
           ['e', 's', 'e'],
           ['e', 'e', 'e'],
           ['e', 's', 'e'],
           ['e', 's', 'e']]
}

async def send_word_of_emojis(message, emoji, words):
    lines = ['', '', '', '', '']

    for word in words:
        for char in word:
            s = letter_to_emojis[char]

            for i, val in enumerate(s):
                for sym in val:
                    if sym == 'e':
                        lines[i] += emoji
                    else:
                        lines[i] += ':spider:'
        for line in lines:
            line += ':spider:'
    
    for line in lines:
        line.removesuffix(':spider:')

    m = ''
    for line in lines:
        m += line + '\n'

    m.removesuffix('\n')

    await message.channel.send(m)