import discord

letter_to_emojis = {
    'a' : [['e', 'e', 'e'],
           ['e', 's', 'e'],
           ['e', 'e', 'e'],
           ['e', 's', 'e'],
           ['e', 's', 'e']],

    'b' : [['e', 'e', 'e'],
           ['e', 's', 'e'],
           ['e', 'e', 'e'],
           ['e', 's', 'e'],
           ['e', 'e', 'e']],

    'c' : [['e', 'e', 'e'],
           ['e', 's', 's'],
           ['e', 's', 's'],
           ['e', 's', 's'],
           ['e', 'e', 'e']],

    'd' : [['e', 'e', 's'],
           ['e', 's', 'e'],
           ['e', 's', 'e'],
           ['e', 's', 'e'],
           ['e', 'e', 's']],

    'e' : [['e', 'e', 'e'],
           ['e', 's', 's'],
           ['e', 'e', 'e'],
           ['e', 's', 's'],
           ['e', 'e', 'e']],

    'f' : [['e', 'e', 'e'],
           ['e', 's', 's'],
           ['e', 'e', 's'],
           ['e', 's', 'e'],
           ['e', 's', 's']],

    'g' : [['e', 'e', 'e', 'e'],
           ['e', 's', 's', 's'],
           ['e', 's', 'e', 'e'],
           ['e', 's', 's', 'e'],
           ['e', 'e', 'e', 'e']],

    'h' : [['e', 's', 'e'],
           ['e', 's', 'e'],
           ['e', 'e', 'e'],
           ['e', 's', 'e'],
           ['e', 's', 'e']],
           
    'i' : [['e'],
           ['e'],
           ['e'],
           ['e'],
           ['e']],

    'j' : [['e', 'e', 'e'],
           ['s', 's', 'e'],
           ['s', 's', 'e'],
           ['e', 's', 'e'],
           ['e', 'e', 'e']],

    'k' : [['e', 's', 'e'],
           ['e', 'e', 's'],
           ['e', 's', 's'],
           ['e', 'e', 's'],
           ['e', 's', 'e']],

    'l' : [['e', 's', 's'],
           ['e', 's', 's'],
           ['e', 's', 's'],
           ['e', 's', 's'],
           ['e', 'e', 'e']],

    'm' : [['s', 'e', 's', 'e', 's'],
           ['e', 's', 'e', 's', 'e'],
           ['e', 's', 'e', 's', 'e'],
           ['e', 's', 'e', 's', 'e'],
           ['e', 's', 'e', 's', 'e']],

    'n' : [['e', 's', 'e'],
           ['e', 'e', 'e'],
           ['e', 's', 'e'],
           ['e', 's', 'e'],
           ['e', 's', 'e']],

    'o' : [['e', 'e', 'e'],
           ['e', 's', 'e'],
           ['e', 's', 'e'],
           ['e', 's', 'e'],
           ['e', 'e', 'e']],

    'p' : [['e', 'e', 'e'],
           ['e', 's', 'e'],
           ['e', 'e', 'e'],
           ['e', 's', 's'],
           ['e', 's', 's']],

    'q' : [['e', 'e', 'e', 'e'],
           ['e', 's', 's', 'e'],
           ['e', 's', 's', 'e'],
           ['e', 's', 'e', 'e'],
           ['e', 'e', 'e', 'e']],

    'r' : [['e', 'e', 'e'],
           ['e', 's', 'e'],
           ['e', 'e', 'e'],
           ['e', 'e', 's'],
           ['e', 's', 'e']],

    's' : [['e', 'e', 'e'],
           ['e', 's', 's'],
           ['e', 'e', 'e'],
           ['s', 's', 'e'],
           ['e', 'e', 'e']],

    't' : [['e', 'e', 'e'],
           ['s', 'e', 's'],
           ['s', 'e', 's'],
           ['s', 'e', 's'],
           ['s', 'e', 's']],

    'u' : [['e', 's', 'e'],
           ['e', 's', 'e'],
           ['e', 's', 'e'],
           ['e', 's', 'e'],
           ['e', 'e', 'e']],

    'v' : [['e', 's', 'e'],
           ['e', 's', 'e'],
           ['e', 's', 'e'],
           ['e', 's', 'e'],
           ['s', 'e', 's']],

    'w' : [['e', 's', 'e', 's', 'e'],
           ['e', 's', 'e', 's', 'e'],
           ['e', 's', 'e', 's', 'e'],
           ['e', 's', 'e', 's', 'e'],
           ['s', 'e', 's', 'e', 's']],

    'x' : [['e', 's', 'e'],
           ['e', 's', 'e'],
           ['s', 'e', 's'],
           ['e', 's', 'e'],
           ['e', 's', 'e']],

    'y' : [['e', 's', 'e'],
           ['e', 's', 'e'],
           ['e', 'e', 'e'],
           ['s', 's', 'e'],
           ['e', 'e', 'e']],

    'z' : [['e', 'e', 'e'],
           ['s', 'e', 's'],
           ['s', 'e', 's'],
           ['e', 's', 's'],
           ['e', 'e', 'e']],
}

async def send_word_of_emojis(message, emoji, words):
    lines = ['', '', '', '', '']
    lines_temp = ['', '', '', '', '']
    count = 0
    count_temp = 0

    for word in words:
       for char in word:
           try:
              s = letter_to_emojis[char]
           except KeyError:
              continue

           for i, val in enumerate(s):
              for sym in val:
                  if sym == 'e':
                     lines_temp[i] += emoji
                     count_temp += len(emoji)
                  else:
                     lines_temp[i] += ':spider:'
                     count_temp += len(':spider')
       
           if count + count_temp >= 1500:
              m = ''
              for line in lines:
                     m += line + '\n'
              m.removesuffix('\n')
              await message.channel.send(m)
              count = count_temp
              count_temp = 0
              lines = lines_temp
              for line in lines_temp:
                     line = ''
           else:
              count += count_temp
              count_temp = 0
              for i in range(len(lines)):
                     lines[i] += lines_temp[i]
                     lines_temp[i] = ''

       for line in lines:
            lines += ':spider:'
            count += len(':spider')

    for line in lines:
       line.removesuffix(':spider:') 

    m = ''

    for line in lines:
       m += line + '\n'

    m.removesuffix('\n')

    await message.channel.send(m)