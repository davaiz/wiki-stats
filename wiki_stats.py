#!/usr/bin/python3

import os
import sys
import math

import array

import statistics as st

from matplotlib import rc
rc('font', family='Droid Sans', weight='normal', size=14)

import matplotlib.pyplot as plt


class WikiGraph:

    def load_from_file(self, filename):
        print('Загружаю граф из файла: ' + filename)

        with open(filename) as f:
            a = f.readline()
            a = a.strip()
            a = list(map(int, a.split(' ')))
            self._n, self._nlinks = a[0], a[1]
            i = 0
            self._titles = []
            self._sizes = array.array('L', [0]*self._n)
            self._links = array.array('L', [0]*self._nlinks)
            self._redirect = array.array('B', [0]*self._n)
            self._offset = array.array('L', [0]*(self._n))
            self._idunnootherways = array.array('L', [0]*(self._n))
            self._linksto = array.array('L', [0]*(self._n))

            for n in range(self._n):
                a = f.readline().strip()
                self._titles.append(a)
                a = f.readline()
                a = list(a.split(' '))
                self._sizes[n] = int(a[0])
                self._redirect[n] = int(a[1])
                self._offset[n] = self._offset[n-1] + int(a[2])
                self._idunnootherways[n] = int(a[2])
                a = int(a[2])
                i+=a
                while a != 0:
                    self._links[i-a] = int(f.readline())
                    a -= 1
            for i in range(self._n):
                self._linksto[i] = self._links.count(i)
        print('Граф загружен')

    def get_number_of_links_from(self, _id):
        return self._offset[_id+1] - self._offset[_id]

    def get_links_from(self, _id):
        for i in range(self._offset[_id+1]-self._offset[_id]):
            return self._links[self._offset[_id]+i]

    def get_id(self, title):
        for i in range(len(self._titles)):
            if title == self._titles[i]:
                return i
                break
        return None

    def get_number_of_pages(self):
        return self._n


    def get_title(self, _id):
        return self._titles[_id]

    def get_page_size(self, _id):
        return self._sizes[_id]

    def is_redirect(self, _id):
        if self._redirect[_id]==1:
            return True

def hist(fname, data, bins, xlabel, ylabel, title, facecolor='green', alpha=0.5, transparent=True, **kwargs):
    plt.clf()



if __name__ == '__main__':
    wg = WikiGraph()
    wg.load_from_file('wiki_small.txt')
    print('Kоличество статей с перенаправлением: ', sum(wg._redirect))
    print('Mинимальное количество ссылок из статьи: ', min(wg._idunnootherways))
    print('Kоличество статей с минимальным количеством ссылок: ', wg._links.count(min(wg._idunnootherways)))
    print('Mаксимальное количество ссылок из статьи: ', max(wg._idunnootherways))
    a = 0
    for i in range(len(wg._offset)-1):
        if wg._offset[i+1]-wg._offset[i] == max(wg._idunnootherways):
            a +=1
            s = i+1
    print('Kоличество статей с максимальным количеством ссылок: ', a)
    print('Cтатья с наибольшим количеством ссылок: ', wg.get_title(s))
    print('Cреднее количество ссылок в статье: %0.2f (ср. откл. %0.2f)' %(st.mean(wg._idunnootherways), st.stdev(wg._idunnootherways)))

    print('Mинимальное количество ссылок на статью: ', min(wg._linksto))
    print('Kоличество статей с минимальным количеством внешних ссылок: ', wg._links.count(min(wg._linksto)))
    print('Максимальное количество ссылок на статью: ', max(wg._linksto))
    print('Количество статей с максимальным количеством внешних ссылок: ', wg._linksto.count(max(wg._linksto)))
    for i in range(len(wg._linksto)):
        if wg._linksto[i] == max(wg._linksto):
            break
    print('Статья с наибольшим количеством внешних ссылок: ', wg.get_title(i))

    # TODO: статистика и гистограммы

    # TODO: статистика и гистограммы
