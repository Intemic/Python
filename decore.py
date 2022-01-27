
def add_comp(comp: str) -> None:
    print('Добавлен компонент : ', comp)

def make_comp(func):
    def wrapper(comp: str):
        print('----------------------------')
        func(comp)
        print('----------------------------')

    return wrapper

add_comp = make_comp
comp = ['Материнская плата', 'Видеокарта', 'ОЗУ', 'Процессор']

print('Собираем компьютер :')
for value in comp:
    add_comp(value)