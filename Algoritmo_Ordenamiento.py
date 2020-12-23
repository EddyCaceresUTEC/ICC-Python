import random
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def swap(A, i, j):
    """Función auxiliar para intercambiar elementos i y j de la lista A."""

    if i != j:
        A[i], A[j] = A[j], A[i]


def bubblesort(A):
    """has seleccionado bubblesort."""

    if len(A) == 1:
        return

    swapped = True
    for i in range(len(A) - 1):
        if not swapped:
            break
        swapped = False
        for j in range(len(A) - 1 - i):
            if A[j] > A[j + 1]:
                swap(A, j, j + 1)
                swapped = True
            yield A


def insertionsort(A):
    """has seleccionado insertionsort."""

    for i in range(1, len(A)):
        j = i
        while j > 0 and A[j] < A[j - 1]:
            swap(A, j, j - 1)
            j -= 1
            yield A


def mergesort(A, start, end):
    """has seleccionado Mergesort."""

    if end <= start:
        return

    mid = start + ((end - start + 1) // 2) - 1
    yield from mergesort(A, start, mid)
    yield from mergesort(A, mid + 1, end)
    yield from merge(A, start, mid, end)
    yield A


def merge(A, start, mid, end):
    """Función auxiliar para Mergesort."""

    merged = []
    leftIdx = start
    rightIdx = mid + 1

    while leftIdx <= mid and rightIdx <= end:
        if A[leftIdx] < A[rightIdx]:
            merged.append(A[leftIdx])
            leftIdx += 1
        else:
            merged.append(A[rightIdx])
            rightIdx += 1

    while leftIdx <= mid:
        merged.append(A[leftIdx])
        leftIdx += 1

    while rightIdx <= end:
        merged.append(A[rightIdx])
        rightIdx += 1

    for i, sorted_val in enumerate(merged):
        A[start + i] = sorted_val
        yield A


def quicksort(A, start, end):
    """has seleccionado quicksort."""

    if start >= end:
        return

    pivot = A[end]
    pivotIdx = start

    for i in range(start, end):
        if A[i] < pivot:
            swap(A, i, pivotIdx)
            pivotIdx += 1
        yield A
    swap(A, end, pivotIdx)
    yield A

    yield from quicksort(A, start, pivotIdx - 1)
    yield from quicksort(A, pivotIdx + 1, end)


def selectionsort(A):
    """has seleccionado selectionsort."""
    if len(A) == 1:
        return

    for i in range(len(A)):
        # Encuentre el valor mínimo sin clasificar.
        minVal = A[i]
        minIdx = i
        for j in range(i, len(A)):
            if A[j] < minVal:
                minVal = A[j]
                minIdx = j
            yield A
        swap(A, i, minIdx)
        yield A


if __name__ == "__main__":
    # Obtenga la entrada del usuario para determinar el rango de números enteros (1 a N) y el
    # método de clasificación (algoritmo).
    N = int(input("Ingrese el número de enteros: "))
    method_msg = "Ingrese el método de clasificación:\n(b)ubble\n(i)nsertion\n(m)erge \
        \n(q)uick\n(s)election\n"
    method = input(method_msg)

   # Crear y mezclar aleatoriamente una lista de números enteros.
    A = [x + 1 for x in range(N)]
    random.seed(time.time())
    random.shuffle(A)

    # Obtenga el generador apropiado para suministrar al método matplotlib FuncAnimation.
    if method == "b":
        title = "Bubblesort"
        generator = bubblesort(A)
    elif method == "i":
        title = "Insertionsort"
        generator = insertionsort(A)
    elif method == "m":
        title = "Mergesort"
        generator = mergesort(A, 0, N - 1)
    elif method == "q":
        title = "Quicksort"
        generator = quicksort(A, 0, N - 1)
    else:
        title = "Selectionsort"
        generator = selectionsort(A)

    # Inicializar figura y eje.
    fig, ax = plt.subplots()
    ax.set_title(title)

    # Inicializar un diagrama de barras. Tenga en cuenta que matplotlib.pyplot.bar () devuelve un
    # lista de rectángulos (con cada barra en el gráfico de barras correspondiente
    # a un rectángulo) que almacenamos en bar_rects.
    bar_rects = ax.bar(range(len(A)), A, align="edge")
    #autolabel(bar_rects)
    # Establecer límites de eje. Establezca el límite superior del eje y lo suficientemente alto como para que las
    # las barras no se superpondrán con la etiqueta de texto.
    ax.set_xlim(0, N)
    ax.set_ylim(0, int(1.07 * N))

    # Coloque una etiqueta de texto en la esquina superior izquierda del gráfico para mostrar
    # número de operaciones realizadas por el algoritmo de clasificación (cada "rendimiento"
    # se trata como 1 operación).
    text = ax.text(0.02, 0.95, "", transform=ax.transAxes)

    # Defina la función update_fig () para usar con matplotlib.pyplot.FuncAnimation ().
    # Para rastrear el número de operaciones, es decir, iteraciones a través de las cuales
    # la animación se ha ido, defina una variable "iteración". Esta variable
    # se pasará a update_fig () para actualizar la etiqueta de texto, y también es
    # incrementado en update_fig (). Para que este incremento se refleje en el exterior de
    # la función, hacemos "iteration" una lista de 1 elemento, ya que listas (y
    # otros objetos mutables) se pasan por referencia (pero un entero sería
    # pasado por valor).
    # NOTA: Alternativamente, la iteración podría volver a declararse dentro de update_fig ()
    # con la palabra clave "global" (o palabra clave "no local").
    iteration = [0]

    def update_fig(A, rects, iteration):
        for rect, val in zip(rects, A):
            rect.set_height(val)
        iteration[0] += 1
        text.set_text("# de operaciones: {}".format(iteration[0]))

    anim = animation.FuncAnimation(fig, func=update_fig,
                                   fargs=(
                                       bar_rects, iteration), frames=generator, interval=1,
                                   repeat=False)
    plt.show()