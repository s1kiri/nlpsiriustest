import pandas as pd
data = pd.read_csv('data.csv')
dialogues = []
first = '@@ПЕРВЫЙ@@'
second = '@@ВТОРОЙ@@'
for i in range(len(data)):
    if data.iloc[i].isna().sum()<3:
        unit = first
        firstused = True
        secondused = False
        for j in range(4):
            if str(data.iloc[i][j]) != 'nan':
                unit += ' '+ data.iloc[i][j] + ' '
                if firstused:
                    firstused, secondused = False, True
                    unit += second
                elif secondused:
                    firstused, secondused = True, False
                    unit += first
        dialogues.append(unit[:-11])

file_path = 'dialogues.txt'

with open(file_path, 'w', encoding='utf-8') as file:
    for dialogue in dialogues:
        file.write(dialogue + '\n')