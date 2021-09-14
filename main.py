import pygame
import random
from tkinter import *
from settings import *
from sys import exit

pygame.init()
scr = pygame.display.set_mode((scrWidth, scrHeight))

master = Tk()

def onSubmit():
    global arrCnt, dist

    try:
        arrCnt = int(arrSzEntry.get())
        dist = scrWidth // arrCnt - gap
    except:
        pass

    master.quit()
    master.destroy()

def setAlgorithm(key):
    global algo
    algo = sortAlgos[key]

Label(master, text = "Array Size").grid(row = 0, column = 0, sticky = W)
arrSzEntry = Entry(master)
arrSzEntry.grid(row = 0, column = 1, sticky = E)

sortAlgos = {
    "Bubble Sort": "bubbleSort",
    "Merge Sort": "mergeSort",
    "Quick Sort": "quickSort",
    "Heap Sort": "heapSort",
}

for i, key in enumerate(sortAlgos):
    Button(master, text = key, command = lambda key = key: setAlgorithm(key)).grid(row = 3, column = i)

submit = Button(master, text = "Start Sorting", command = onSubmit)
submit.grid(columnspan = 2, row = 4)

master.update()
master.mainloop()

class Sort():
    def __init__(self, arr):
        self.arr = arr

    def bubbleSort(self):
        sz = len(self.arr)
        for i in range(sz):
            for j in range(0, sz - 1 - i):
                self.__draw(j)

                if self.arr[j] > self.arr[j + 1]:
                    self.arr[j], self.arr[j + 1] = self.arr[j + 1], self.arr[j]

    def mergeSort(self, left = None, right = None):
        if left == None or right == None:
            left, right = 0, len(self.arr) - 1

        if left >= right:
            return

        mid = (left + right) // 2

        self.mergeSort(left, mid)
        self.mergeSort(mid + 1, right)

        self.__mergeSort(left, mid, right)

    def quickSort(self):
        self.__quickSort(0, len(self.arr) - 1)

    def heapSort(self):
        n = len(self.arr)

        # build our heap. start from n // 2 - 1 because that's the first index of a non-leaf node in a complete tree.
        for i in range(n // 2 - 1, -1, -1):
            self.__heapify(n, i)

        for i in range(n - 1, 0, -1):
            self.__swap(i, 0)
            self.__heapify(i, 0)

    def isSorted(self):
        isSorted = True
        for i in range(1, len(self.arr)):
            if self.arr[i] < self.arr[i - 1]:
                isSorted = False
                print("Array is not sorted, check implementation for issues.\nIndex:", i - 1, "\t", self.arr[i - 1], ">", self.arr[i])

        return True if isSorted else False

    def __mergeSort(self, left, mid, right):
        i, j = left, mid + 1
        temp = []
        while i <= mid and j <= right:
            self.__draw(i, j)
            if self.arr[i] < self.arr[j]:
                temp.append(self.arr[i])
                i += 1  
            else:
                temp.append(self.arr[j])
                j += 1

        while i <= mid:
            self.__draw(i)
            temp.append(self.arr[i])
            i += 1

        while j <= right:
            self.__draw(j)
            temp.append(self.arr[j])
            j += 1

        y = 0
        for x in range(left, right + 1):
            self.arr[x] = temp[y]
            y += 1
            self.__draw()

    def __quickSort(self, start, end):
        # do insertion sort if the array window size is within the cutoff range.
        if start + 10 > end:
            for i in range(start + 1, end + 1):
                tmp = self.arr[i]
                j = i
                while j > start and tmp < self.arr[j - 1]:
                    self.__draw(i, j)
                    self.arr[j] = self.arr[j - 1]
                    j -= 1
                
                self.arr[j] = tmp

            return

        # use median-of-three partitioning to counter already-sorted and reverse-sorted arrays. lessens likelihood of quicksort degrading into O(n^2) runtime.
        mid = (start + end) // 2
        if self.arr[start] > self.arr[mid]:
            self.__draw(start, mid)
            self.__swap(start, mid)
        if self.arr[start] > self.arr[end]:
            self.__draw(start, end)
            self.__swap(start, end)
        if self.arr[mid] > self.arr[end]:
            self.__draw(mid, end)
            self.__swap(mid, end)

        self.__swap(mid, end - 1)
        pivot = self.arr[end - 1]
        self.__draw(start, end)
        i, j = start + 1, end - 2
        while True:
            self.__draw(i, j)
            while self.arr[i] <= pivot:
                i += 1
            while pivot <= self.arr[j]:
                j -= 1
            
            if i < j:
                self.__swap(i, j)
            else:
                break
                
            self.__draw(i, j)

        self.__swap(i, end - 1)
        self.__draw(i, end)

        self.__quickSort(start, i)
        self.__quickSort(i + 1, end)

        self.__draw()
    
    def __heapify(self, heapSz, rootIdx):
        while rootIdx < heapSz:
            self.__draw(heapSz, rootIdx)

            leftIdx = 2 * rootIdx + 1
            rightIdx = 2 * rootIdx + 2

            if leftIdx >= heapSz:
                break

            largerIdx = leftIdx
            if rightIdx < heapSz and self.arr[rightIdx] > self.arr[leftIdx]:
                largerIdx = rightIdx

            if self.arr[largerIdx] > self.arr[rootIdx]:
                self.__swap(rootIdx, largerIdx)
                rootIdx = largerIdx
            else:
                break

        self.__draw()
        
    # TODO: redo to take multiple indices to allow for more than just two colors.
    def __draw(self, idx1 = -1, idx2 = -1):
        scr.fill(BLACK)

        for i, a in enumerate(self.arr):
            color = RED if i == idx1 or i == idx2 else WHITE
            pygame.draw.rect(scr, color, pygame.Rect(i * dist + (i * gap), scrHeight - a, dist, a))

        pygame.display.update()
        pygame.time.Clock().tick(sortSpeed)

        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                exit()

    def __swap(self, p0, p1):
        self.arr[p0], self.arr[p1] = self.arr[p1], self.arr[p0]

def main():
    arr = [None] * arrCnt
    for i in range(arrCnt):
        curSize = random.randint(1, scrHeight)
        arr[i] = curSize

    srt = Sort(arr)

    finished = False
    while True:
        if not finished:
            getattr(srt, algo)()
            finished = True

        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                exit()

if __name__ == '__main__':
    main()