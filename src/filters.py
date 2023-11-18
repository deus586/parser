def filters():
    """

    Возвращает фильтры
    """
    # Фильтры по-умолчанию
    name = ''
    per_page = 100
    sort = 'relevance'
    page_count = 1

    # Варианты сортировки
    sort_variable = {1: 'relevance', 2: 'salary_asc',
                     3: 'salary_desc', 4: 'publication_time'}

    # Спрашиваем у пользователя хочет ли он ввести фильтры
    user_input = input('Хотите ли ввести фильтры?(Y/N): ')
    while True:
        if user_input.upper() == 'N':
            # Если пользователь не хочет вводить фильтры оставляем фильтры по-умолчанию
            break
        elif user_input.upper() == 'Y':
            # Варианты ввода фильтров
            print('Какие фильтры хотите ввести:')
            print('1. Название вакансии')
            print('2. Количество вакансий(по умолчанию: 100)')
            print('3. Варианты сортировки(по умолчанию: по соответствию)')
            print('4. Количество страниц(по умолчанию: 1)')
            choose = int(input())

            if choose == 1:
                name = input('Введите название: ')
            elif choose == 2:
                try:
                    per_page = int(input('Введите количество вакансий(не больше 100): '))
                except ValueError:
                    print('Неверный тип данных.')
                if per_page > 100:
                    print('Слишком много вакансий на одну страницу.')
                    per_page = 100
            elif choose == 3:
                print("1. По соответствию\n2. По возрастанию оплаты\n3. По убыванию оплаты\n4. По дате")
                sort = input('Введите вариант сортировки: ')
                try:
                    sort = sort_variable[int(sort)]
                except KeyError:
                    print('Нет такого варианта.')
            elif choose == 4:
                try:
                    page_count = int(input('Введите количество страниц: '))
                except ValueError:
                    print('Неверный тип данных.')
            else:
                print('Нет такого варианта.')

        user_input = input('Хотите продолжить?(Y/N): ')
    return [name, per_page, sort, page_count]
