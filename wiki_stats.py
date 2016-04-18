import os
import sys
import math

import array

import statistics

from matplotlib import rc
rc('font', family='Droid Sans', weight='normal', size=14)

import matplotlib.pyplot as plt


class WikiGraph:

    def load_from_file(self, file):
        print('Загружаю граф из файла: ' + file)

        with open(file) as f:
            (n, _nlinks) = (map(int, f.readline().split()))
            self._titles = []

            self._sizes = array.array('L', [0]*n)
            self._links = array.array('L', [0]*_nlinks)
            self._redirect = array.array('B', [0]*n)
            self._offset = array.array('L', [0]*(n+1))
            n_lks = 0
            for i in range(n):
                self._titles.append(f.readline().rstrip())
                (size, redirect, lks) = (map(int, f.readline().split()))
                self._sizes[i] = size
                self._redirect[i] = redirect
                for j in range(n_lks, n_lks + lks):
                    self._links[j] = int(str(f.readline()))
                n_lks += lks
                self._offset[i+1] = self._offset[i] + lks


        print('Граф загружен')

    def get_number_of_links_from(self, _id):
        return len(self._links[self._offset[_id]:self._offset[_id+1]])

    def get_links_from(self, _id):
        return self._links[self._offset[_id]:self._offset[_id+1]]

    def get_id(self, title):
        for i in range(len(self._titles)):
            if self._titles[i] == title:
                return(i)

    def get_number_of_pages(self):
        return len(self._titles)

    def is_redirect(self, _id):
        return self._redirect[_id]

    def get_title(self, _id):
        return self._titles[_id]

    def get_page_size(self, _id):
        return self._sizes(_id)


def analyse_links_from_page(G):
    numlinks_from = list(map(G.get_number_of_links_from, range(G.get_number_of_pages())))
    _max = max(numlinks_from)
    _min = min(numlinks_from)
    mxn = sum(x == _max for x in numlinks_from)
    mnn = sum(x == _min for x in numlinks_from)
    print("Минимальное количество:", _min)
    print("Количество статей с минимальным количеством ссылок:", mnn)
    print("Максимальное количество ссылок из статьи:", _max)
    print("Количество статей с максимальным количеством ссылок:", mxn)
    found_id = None
    for i in range(G.get_number_of_pages()):
        if G.get_number_of_links_from(i) == _max:
            found_id = i
            break
    print("Статья с наибольшим количеством внешних ссылок:",  G.get_title(found_id)) 
    middle_counr_links_in_article = [G.get_number_of_links_from(i) for i in range(G.get_number_of_pages()) if not G.is_redirect(i)]
    print("Среднее количество внешних ссылок в статье: %0.2f  (ср. откл. : %0.2f)"  %(statistics.mean(middle_counr_links_in_article), statistics.stdev(middle_counr_links_in_article)))
def analyse_links_to_page(G):
    numlinks_to = [0 for i in range(G.get_number_of_pages())]
    for i in range(G.get_number_of_pages()):
        for x in G.get_links_from(i):
            numlinks_to[x] += 1
            if G.is_redirect(i) == 1:
                numlinks_to[x] -= 1
    _max = max(numlinks_to)
    _min = min(numlinks_to)
    mxn = sum(x == _max for x in numlinks_to)
    mnn = sum(x == _min for x in numlinks_to)
    print("Минимальное количество ссылок на статью:", _min)
    print("Количество статей с минимальным количеством внешних ссылок:", mnn)
    print("Максимальное количество ссылок на статью:", _max)
    print("Количество статей с максимальным количеством внешних ссылок:", mxn)
    found_id = None
    for i in range(G.get_number_of_pages()):
        if numlinks_to[i] == _max:
            found_id = i
            break
    print("Статья с наибольшим количеством внешних ссылок:",  G.get_title(found_id))
    print("Среднее количество внешних ссылок на статью: %0.2f  (ср. откл. : %0.2f)" %(statistics.mean(numlinks_to), statistics.stdev(numlinks_to)))


def analyse_redirects(G):
    redirects_to = [0 for i in range(G.get_number_of_pages())]
    for i in range(G.get_number_of_pages()):
        for x in G.get_links_from(i):
            if G.is_redirect(i) == 1:
                redirects_to[x] += 1
    _max = max(redirects_to)
    _min = min(redirects_to)
    mxn = sum(x == _max for x in redirects_to)
    mnn = sum(x == _min for x in redirects_to)
    print("Минимальное количество перенаправление на статью:", _min)
    print("Количество статей с минимальным количеством внешних перенаправлений:", mnn)
    print("Максимальное количество перенаправлений на статью:", _max)
    print("Количество статей с максимальным количеством внешних перенаправлений:", mxn)
    found_id = None
    for i in range(G.get_number_of_pages()):
        if redirects_to[i] == _max:
            found_id = i
            break
    print("Статья с наибольшим количеством внешних перенаправлений:",  G.get_title(found_id))
    print("Среднее количество внешних перенаправлений на статью: %0.2f  (ср. откл. : %0.2f)" %(statistics.mean(redirects_to), statistics.stdev(redirects_to)))

def hist(fname, data, bins, xlabel, ylabel, title, facecolor='green', alpha=0.5, transparent=True, **kwargs):
    plt.clf()
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.hist(x=data, bins=bins, facecolor=facecolor, alpha=alpha, **kwargs)
    plt.savefig(fname, transparent=transparent)
def path(self):
    start = self.get_id("Python")
    end = self.get_id("Список_файловых_систем")
    shortest_leng = {vert:float("+inf") for vert in range(self.get_number_of_pages())}
    print("Запускаем поиск в ширину")
    shortest_path = {vert:[] for vert in range(self.get_number_of_pages())}
    queue = [start]
    fired = [start]
    shortest_leng[start] = 0
    while queue:
        star = queue.pop(0)
        for neibours in self.get_links_from(star):
            new_shortest_path_length = shortest_leng[star] + 1
            if neibours not in fired:
                queue.append(neibours)
                fired.append(neibours)
            if new_shortest_path_length <= shortest_leng[neibours]:
                shortest_leng[neibours] = new_shortest_path_length
                shortest_path[neibours] = (star,neibours)  
    x = shortest_path[end]
    path = []
    path.insert(0,x)
    print("Поиск закончен. Найден путь:")
    print(self.get_title(start))
    while x[0] != start:
        path.insert(0,shortest_path[x[0]])
        x = shortest_path[x[0]]
    for y in path:
        print(self.get_title(y[1]))
if __name__ == '__main__':
    wg = WikiGraph()
    wg.load_from_file('wiki_small.txt')
    print("Количество статей с перенаправлением:", sum(wg._redirect))
    analyse_links_from_page(wg)
    analyse_links_to_page(wg)
    analyse_redirects(wg)
    wg.path()
    hist(fname='1.png', data=[wg.get_number_of_links_from(i) for i in range(1211)],bins=200,xlabel='Количество статей', ylabel="Количество ссылок", title="Распределение количества ссылок из статьи")
    #hist('2',wg. 100, 'Количество статей', "Количество ссылок", "Распределение количества ссылок на статью", range=(0,200))
    #hist('3',wg., 20, 'Количество статей', "Количество ссылок", "Распределение количества редиректов на статью", range=(0,20))
    hist(fname='4.png', data=[wg._sizes[i] for i in range(1211)], bins=50, xlabel='Количество статей', ylabel="Количество ссылок", title="Распределение размеров статей")
    hist(fname='5.png', data=[wg._sizes[i] for i in range(1211)], bins=50, xlabel='Количество статей', ylabel="Количество ссылок", title="Распределение размеров статей (log)", log=True)

    
