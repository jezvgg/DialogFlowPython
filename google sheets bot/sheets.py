import pygsheets
import pandas as pd

class sheets:
    '''
    Класс для работы с Google Sheets.
    '''
    __sheets = None
    books = None
    movies = None

    def __init__(self, settings):
        self.__sheets = pygsheets.authorize(client_secret=settings.client_secret)
        sheet1 = self.__sheets.open('new_books')
        sheet2 = self.__sheets.open('new_movies')
        self.books = sheet1.sheet1
        self.movies = sheet2.sheet1


    def BookstoText(self, df: pd.DataFrame) -> str:
        '''
        Класс для обработки таблицы про книги. Возращает ответ для пользователя.
        '''
        result = 'Могу порекомендовать:\n'
        if len(df['Название']) == 0: return 'Извини, но таких книг я тебе порекомендовать не могу, я их не знаю.'
        for i in range(len(df['Название'])):
            result += f'{i+1}. {df["Название"].iloc[i]}\nАвтор: {df["Автор"].iloc[i]}\nЖанры: {df["Жанр"].iloc[i]}\n\n'
        return result


    def MoviestoText(self,df: pd.DataFrame) -> str:
        '''
        Класс для обработки таблицы про фильмы. Возращает ответ для пользователя.
        '''
        result = 'Могу порекомендовать:\n'
        if len(df['Название фильма']) == 0: return 'Извини, но таких книг я тебе порекомендовать не могу, я их не знаю.'
        for i in range(len(df['Название фильма'])):
            result += f'{i+1}. {df["Название фильма"].iloc[i]}\nЭмоции: {df["Эмоция"].iloc[i]}\nЖанры: {df["Жанр"].iloc[i]}\n\n'
        return result


    def get_books(self, genre: str = '', index: int = 0) -> str:
        '''
        Обращается к Google Sheets. Обрабатывает таблицу и конверитурет в DataFrame, после чего фильтрует
        по жанру (если передан). Возращает ответ для пользователя.
        '''
        df = self.books.get_as_df()
        df = df.drop(columns=['Индекс', ''])
        if genre != '':
            df = df[df['Жанр'].apply(lambda x: genre in x)].sort_values('Общая оценка', ascending=False).head(3)
        else:
            df = df.sort_values('Общая оценка', ascending=False)[index,index+3]
        return self.BookstoText(df)
    

    def get_movies(self, genre: str = '', emotions: str = '', index: int = 0) -> str:
        '''
        Обращается к Google Sheets. Обрабатывает таблицу и конверитурет в DataFrame, после чего фильтрует
        по жанру или эмоции (если передан). Возращает ответ для пользователя.
        '''
        df = self.movies.get_as_df()
        if genre and emotions:
            df = df[df['Жанр'].apply(lambda x: genre in x)]
            df = df[df['Эмоция'].apply(lambda x: emotions in x)]
        elif genre:
            df = df[df['Жанр'].apply(lambda x: genre in x)]
        elif emotions:
            df = df[df['Эмоция'].apply(lambda x: emotions in x)]
        df = df.sort_values('Рейтинг фильма', ascending=False)[index, index+3]
        return  self.MoviestoText(df)