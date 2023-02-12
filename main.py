import pygame
import random
import math

pygame.init()


class Information:
    # global variables
    Black = 0, 0, 0
    WHITE = 240, 240, 240
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    GREY = 117, 147, 206
    BACKGROUND_COLOR = WHITE
    SIDE_PAD = 100
    TOP_PAD = 150

    GRADIENTS = [

        GREY,
        (117, 147, 206),
        (186, 217, 248),
        (247, 251, 252)
    ]

    Font = pygame.font.SysFont('Verdana', 25)
    LARGE_FONT = pygame.font.SysFont('comicsans', 40)

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualizer")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)

        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))

        self.start_x = self.SIDE_PAD // 2


def generate_starting_list(n, min_val, max_val):
    lst = []

    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)
    return lst

def draw(draw_info, algo_name, ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.GREEN)
    draw_info.window.blit(title, (draw_info.width / 2 - title.get_width() / 2, 2))

    controls = draw_info.Font.render("G - Generate new array | SPACE - Start Sorting | A - Ascending | D - Descending", 1, draw_info.Black)
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2 , 60))

    sorting = draw_info.Font.render("I - Insertion Sort | B - Bubble Sort | S - Selection Sort | Q - Quick Sort | M -  Merge Sort | H - Heap Sort", 1, draw_info.Black)
    draw_info.window.blit(sorting, (draw_info.width / 2 - sorting.get_width() / 2, 95))


    draw_list(draw_info)
    pygame.display.update()

def draw_list(draw_info, color_positions={}, clear_bg=False):
    lst = draw_info.lst

    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, draw_info.width-draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

        color = draw_info.GRADIENTS[i % 3]

        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

    if clear_bg:
        pygame.display.update()


# BUBBLE SORT
def bubble_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(len(lst) - 1):
        for j in range(len(lst)-1-i):
            num1, num2 = lst[j], lst[j+1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j+1] = lst[j+1], lst[j]
                draw_list(draw_info, {j: draw_info.GREEN, j+1: draw_info.RED}, True)
                yield True
    return lst


# INSERTION SORT
def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(1, len(lst)):
        temp = lst[i]

        while True:
            ascending_sort = i > 0 and lst[i-1] > temp and ascending
            descending_sort = i > 0 and lst[i-1] < temp and not ascending

            if not ascending_sort and not descending_sort:
                break

            lst[i] = lst[i-1]
            i -= 1
            lst[i] = temp
            draw_list(draw_info, {i: draw_info.GREEN, i-1: draw_info.RED}, True)
            yield True
    return lst


# SELECTION SORT
def selection_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(len(lst) - 1):
        if ascending:
            min_val = min(lst[i:])
            min_ind = lst.index(min_val,i)
            if lst[i] != lst[min_ind]:
                lst[i], lst[min_ind] = lst[min_ind], lst[i]
            draw_list(draw_info, {i: draw_info.GREEN, min_ind: draw_info.RED}, True)
            yield True
        else:
            max_val = max(lst[i:])
            max_ind = lst.index(max_val, i)
            if lst[i] != lst[max_ind]:
                lst[i], lst[max_ind] = lst[max_ind], lst[i]
            draw_list(draw_info, {i: draw_info.GREEN, max_ind: draw_info.RED}, True)
            yield True
    return lst


# This function is same in both iterative and recursive
def partition(lst, l, h,ascending):
    if ascending:
        pivot = lst[l]

        i = l
        j = h
        while i <= j:
            if lst[i] > pivot and lst[j] < pivot:
                lst[i], lst[j] = lst[j], lst[i]
            elif lst[i] <= pivot:
                i += 1
            elif lst[j] >= pivot:
                j -= 1
        lst[j], lst[l] = lst[l], lst[j]
        return j


# QUICK SORT
def quick_sort(draw_info, ascending=True):
    lst = draw_info.lst
    l = 0
    h = len(lst) - 1
    size = h - l + 1
    stack = [0] * (size)
    top = -1

    top = top + 1
    stack[top] = l

    top = top + 1
    stack[top] = h

    while top >= 0:
        h = stack[top]
        top = top - 1
        l = stack[top]
        top = top - 1
        draw_list(draw_info, {l: draw_info.RED, h: draw_info.GREEN}, True)
        yield True
        draw_list(draw_info, {l: draw_info.RED, h: draw_info.GREEN}, True)
        yield True
        p = partition(draw_info, l, h, ascending)
        draw_list(draw_info, {l: draw_info.RED, h: draw_info.GREEN}, True)
        yield True
        draw_list(draw_info, {l: draw_info.RED, h: draw_info.GREEN}, True)
        yield True

        if p - 1 > l:
            top = top + 1
            stack[top] = l
            top = top + 1
            stack[top] = p - 1

        if p + 1 < h:
            top = top + 1
            stack[top] = p + 1
            top = top + 1
            stack[top] = h


# PARTITION Function is also a part of QUICK SORT
def partition(draw_info, l, h, ascending):
    lst = draw_info.lst
    i = (l - 1)
    x = lst[h]

    if ascending:
        for j in range(l, h):
            if lst[j] <= x:
                i = i + 1
                draw_list(draw_info, {i: draw_info.RED, j: draw_info.GREEN}, True)

                lst[i], lst[j] = lst[j], lst[i]
        draw_list(draw_info, {i + 1: draw_info.RED, h: draw_info.GREEN}, True)

        lst[i + 1], lst[h] = lst[h], lst[i + 1]
        return (i + 1)
    else:
        for j in range(l, h):
            if lst[j] >= x:
                i = i + 1
                draw_list(draw_info, {i: draw_info.RED, j: draw_info.GREEN}, True)

                lst[i], lst[j] = lst[j], lst[i]
        draw_list(draw_info, {i + 1: draw_info.RED, h: draw_info.GREEN}, True)

        lst[i + 1], lst[h] = lst[h], lst[i + 1]
        return (i + 1)


# MERGE SORT
def merge_sort(draw_info, ascending=True):
    lst = draw_info.lst
    width = 1
    n = len(lst)
    while (width < n):
        l = 0;

        while (l < n):
            r = min(l + (width * 2 - 1), n - 1)
            m = min(l + width - 1, n - 1)
            draw_list(draw_info, {l: draw_info.RED, r: draw_info.GREEN}, True)
            yield True
            draw_list(draw_info, {l: draw_info.RED, r: draw_info.GREEN}, True)
            yield True
            merge(lst, l, m, r, ascending)
            draw_list(draw_info, {l: draw_info.RED, r: draw_info.GREEN}, True)
            yield True
            draw_list(draw_info, {l: draw_info.RED, r: draw_info.GREEN}, True)
            yield True
            l += width * 2
        width *= 2

    return lst


# MERGE Function is also a part of MERGE SORT
def merge(lst, l, m, r, ascending=True):
    n1 = m - l + 1
    n2 = r - m
    L = [0] * n1
    R = [0] * n2

    for i in range(0, n1):
        L[i] = lst[l + i]

    for i in range(0, n2):
        R[i] = lst[m + i + 1]

    i, j, k = 0, 0, l

    if ascending:
        while i < n1 and j < n2:
            if L[i] <= R[j]:
                lst[k] = L[i]
                i += 1
            else:
                lst[k] = R[j]
                j += 1
            k += 1

        while i < n1:
            lst[k] = L[i]
            i += 1
            k += 1

        while j < n2:
            lst[k] = R[j]
            j += 1
            k += 1
    else:
        while i < n1 and j < n2:
            if L[i] >= R[j]:
                lst[k] = L[i]
                i += 1
            else:
                lst[k] = R[j]
                j += 1
            k += 1

        while i < n1:
            lst[k] = L[i]
            i += 1
            k += 1

        while j < n2:
            lst[k] = R[j]
            j += 1
            k += 1


# HEAP SORT
def heapify(draw_info, n, i, ascending):
    lst = draw_info.lst

    curr = i
    left = 2 * i + 1
    right = 2 * i + 2

    if ascending:
        if left < n and lst[curr] < lst[left]:
            curr = left

        if right < n and lst[curr] < lst[right]:
            curr = right

    if not ascending:
        if left < n and lst[left] < lst[curr]:
            curr = left

        if right < n and lst[right] < lst[curr]:
            curr = right

    if curr != i:
        (lst[i], lst[curr]) = (lst[curr], lst[i])
        draw_list(draw_info, {i: draw_info.GREEN, curr: draw_info.RED}, True)
        heapify(draw_info, n, curr, ascending)


def heap_sort(draw_info, ascending=True):
    lst = draw_info.lst

    n = len(lst)
    for i in range(n // 2 - 1, -1, -1):
        heapify(draw_info, n, i, ascending)

    for i in range(n - 1, 0, -1):
        (lst[i], lst[0]) = (lst[0], lst[i])
        draw_list(draw_info, {i: draw_info.GREEN, 0: draw_info.RED}, True)
        heapify(draw_info, i, 0, ascending)
        yield True
    return lst





def main():
    run = True
    clock = pygame.time.Clock()

    n = 50
    min_val = 0
    max_val = 100

    lst = generate_starting_list(n, min_val, max_val)
    draw_info = Information(1500, 800, lst)
    sorting = False
    ascending = True

    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None

    while run:
        clock.tick(30)

        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sorting_algo_name, ascending)


        # pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_g:
                lst = generate_starting_list(n,min_val,max_val)
                draw_info.set_list(lst)
                sorting = False
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algo_name = "Insertion Sort"
            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algo_name = "Bubble Sort"
            elif event.key == pygame.K_s and not sorting:
                sorting_algorithm = selection_sort
                sorting_algo_name = "Selection Sort"
            elif event.key == pygame.K_q and not sorting:
                sorting_algorithm = quick_sort
                sorting_algo_name = "Quick Sort"
            elif event.key == pygame.K_m and not sorting:
                sorting_algorithm = merge_sort
                sorting_algo_name = "Merge Sort"
            elif event.key == pygame.K_h and not sorting:
                sorting_algorithm = heap_sort
                sorting_algo_name = "Heap Sort"

    pygame.quit()


if __name__ == "__main__":
    main()