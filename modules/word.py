import discord

lines = ['', '', '', '', '']

letter_to_emojis = {
    'a' : [['e', 'e', 'e'],
           ['e', 's', 'e'],
           ['e', 'e', 'e'],
           ['e', 's', 'e'],
           ['e', 's', 'e']]
}

async def send_word_of_emojis(message, emoji, words):
    e = emoji

    for word in words:
        for char in word:
            s = letter_to_emojis[char]

            for i, val in s:
                if val == 'e':
                    lines[i] += e
                else:
                    lines[i] += '🕷'
        for line in lines:
            line += '🕷'
    
    for line in lines:
        line.removesuffix('🕷')

    m = ''
    for line in lines:
        m += line + '\n'

    m.removesuffix('\n')

    await message.channel.send(m)