import os.path

from PIL import Image



class q1:
    def files(destdir):
        

        files = [ f for f in os.listdir(destdir) if os.path.isfile(os.path.join(destdir,f)) ]

        print(files)

    def pictures(path1,number, search=-1, w=200, h=300):
        path = 'q1_1/'
        sklad = {1: ['Дайте определение системы m линейных алгебраических уравнений c n неизвестными. Какая СЛАУ называется однородной, неоднородной. Приведите соответствующие примеры. Может ли неоднородная СЛАУ Ax = b быть неопределенной, если столбцы её матрицы линейно независимы (линейно зависимы)? Ответ необходимо обосновать.', 
                    [Image.open(f'{path1}/{path}/1/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/1') if os.path.isfile(os.path.join(f'{path1}/{path}/1', f))]]],
                    2: ['Cформулируйте определение редуцированной ступенчатой формы СЛАУ. Сформулируйте теорему о приведении СЛАУ к редуцированной ступенчатой форме. Может ли неоднородная СЛАУ Ax = b быть совместной (несовмсетной), если соответствующая однородная СЛАУ является определенной (неопределенной)?',
                    [Image.open(f'{path1}/{path}/2/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/2') if os.path.isfile(os.path.join(f'{path1}/{path}/2', f))]]],
                 3: ['Дайте определение ранга матрицы. Сформулируйте теорему Кронекера-Капелли. Совместна или несовместна СЛАУ, если столбцы её расширенной матрицы линейно незавсисимы (линейно зависимы)? Ответ необходимо обосновать.', 
                    [Image.open(f'{path1}/{path}/3/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/3') if os.path.isfile(os.path.join(f'{path1}/{path}/3', f))]]],
                    4: [' Дайте определение фундаментальной системы решений (ФСР) однородной СЛАУ. Сформулируйте теорему об общем виде решения однородной (неоднородной) СЛАУ. Приведите соответствующие примеры. Найдите ФСР однородного уравнения 2x1 + 3x2 −3x3 + 4x4 − 7x5 = 0. ', 
                    [Image.open(f'{path1}/{path}/4/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/4') if os.path.isfile(os.path.join(f'{path1}/{path}/4', f))]]],
                    5: [' Дайте определение матрицы размеры m × n и сформулируйте основные операции над ними. Какие матрицы называются симметрическими, кососимметричсекими? Приведите соответствующие примеры. Можно ли квадратную матрицу представить в виде суммы симметрической и кососимметрической матриц? Ответ необходимо обосновать', 
                    [Image.open(f'{path1}/{path}/5/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/5') if os.path.isfile(os.path.join(f'{path1}/{path}/5', f))]]],
                   6: ['Дайте определение произведения матриц и сформулируйте основные свойства произведения матриц. Существуют ли ненулевые квадратные матрицы A и B такие, что A·B = 0? Ответ необходимо обосновать. Какие матрицы называются коммутирующими? Верно ли равенство (A · B) T = BT · AT ? Ответ необходимо обосновать.', 
                    [Image.open(f'{path1}/{path}/6/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/6') if os.path.isfile(os.path.join(f'{path1}/{path}/6', f))]]],
                    7: ['Дайте определение прямой суммы ⊕ и произведения Кронекера ⊗ для матриц. Приведите соответствующие примеры прямой суммы и произведения Кронекера матриц. Верно ли tr(A ⊗ B) = tr(A) · tr(B)? Ответ необходимо обосновать. ', 
                    [Image.open(f'{path1}/{path}/7/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/7') if os.path.isfile(os.path.join(f'{path1}/{path}/7', f))]]],
                    8: [' Какие матрицы называются обратимыми? Сформулируйте основные свойства для обратных матриц. Докажите', 
                    [Image.open(f'{path1}/{path}/8/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/8') if os.path.isfile(os.path.join(f'{path1}/{path}/8', f))]]],
                    9: ['Сформулируйте понятие элементарной матрицы. Докажите, что P −1 ij = Pij ; Mi(α) −1 = Mi 1 α  ; [Aji(α)]−1 = Aji(−α). Приведите соответствующие примеры', 
                    [Image.open(f'{path1}/{path}/9/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/9') if os.path.isfile(os.path.join(f'{path1}/{path}/9', f))]]],
                    10: ['Сформулируйте алгоритм (с обоснованием) вычисления обратной матрицы (метод ГауссаЖордана). Приведите соответствующий пример', 
                    [Image.open(f'{path1}/{path}/10/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/10') if os.path.isfile(os.path.join(f'{path1}/{path}/10', f))]]],
                    11: ['Сформулируйте критерий обратимости матрицы при помощи произведения элементарных матриц. Приведите соответствующий пример ', 
                    [Image.open(f'{path1}/{path}/11/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/11') if os.path.isfile(os.path.join(f'{path1}/{path}/11', f))]]],
                    12: [' Сформулируйте алгоритм LU разложения обратимой матрицы. Приведите соответствующий пример.', 
                    [Image.open(f'{path1}/{path}/12/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/12') if os.path.isfile(os.path.join(f'{path1}/{path}/12', f))]]],
                    13: ['Приведите определения определителей небольших порядков для матриц (n = 1, 2, 3). Приведите геометрический смысл (с обоснованием) определителей для n = 2 и n = 3.  ', 
                    [Image.open(f'{path1}/{path}/13/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/13') if os.path.isfile(os.path.join(f'{path1}/{path}/13', f))]]],
                    14: [' Дайте определние минора и алгебраического дополнения к элементам матрицы. Приведите кофакторное определение определителя матрицы n-ого порядка. Сформулируйте теорему Лапласа о разложении определителя по строке или столбцу. Найдите (середина 2 картинки) Ответ необходимо обосновать. ', 
                    [Image.open(f'{path1}/{path}/14/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/14') if os.path.isfile(os.path.join(f'{path1}/{path}/14', f))]]],
                    15: ['Приведите формулу для нахождения обратной матрицы через присоединенную матрицу adj(A). Найдите A · adj(A). Ответ необходимо обосновать.', 
                    [Image.open(f'{path1}/{path}/15/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/15') if os.path.isfile(os.path.join(f'{path1}/{path}/15', f))]]],
                    16: ['Приведите основные свойства определителей. Пусть A – кососимметрическая матрица нечетного порядка. Найдите её определитель. Ответ необходимо обосновать.  ', 
                    [Image.open(f'{path1}/{path}/16/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/16') if os.path.isfile(os.path.join(f'{path1}/{path}/16', f))]]],
                    17: [' Сформулируйте и докажите формулы Крамера. ', 
                    [Image.open(f'{path1}/{path}/17/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/17') if os.path.isfile(os.path.join(f'{path1}/{path}/17', f))]]],
                    18: [' Дайте определение минора k-ого порядка. Приведите соответствующие примеры. Пусть A ∈ Mm,n(R). Сколько различных миноров k-ого порядка может быть? Ответ необходимо обосновать. ', 
                    [Image.open(f'{path1}/{path}/18/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/18') if os.path.isfile(os.path.join(f'{path1}/{path}/18', f))]]],
                    19: [' Дайте определение ранга матрицы, используя понятие минора. Какой минор называется базисным? Сформулируйте теорему о базисном миноре. В чем состоит метод окаймляющих миноров? Приведите соответствующий пример. ', 
                    [Image.open(f'{path1}/{path}/19/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/19') if os.path.isfile(os.path.join(f'{path1}/{path}/19', f))]]],
                    20: ['Дайте определение перестановки из n элементов. Сформулируйте понятие инверсии перестановки, сигнатуры перестановки. Какая перестановка называется четной (нечетной)? Приведите соответствующие примеры. ', 
                    [Image.open(f'{path1}/{path}/20/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/20') if os.path.isfile(os.path.join(f'{path1}/{path}/20', f))]]],
                    21: ['Дайте комбинаторно-аналитическое определение определителя n -ого порядка матрицы. Приведите соответствующие примеры с обоснованием формулы определителей для n = 2, n = 3. ', 
                    [Image.open(f'{path1}/{path}/21/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/21') if os.path.isfile(os.path.join(f'{path1}/{path}/21', f))]]],
                    22: ['Дайте определение индекса перестановки. Сформулируйте теоремы Мак-Магона и ФоатаШуценберже. Проиллюстрируйте теоремы на примеры симметрической группы S4.  ', 
                    [Image.open(f'{path1}/{path}/22/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/22') if os.path.isfile(os.path.join(f'{path1}/{path}/22', f))]]],
                    
                 }
        if number == -1:
            numbers = []
            for i, j in sklad.items():
                if search in j[0]:
                    numbers.append(i)
            return 'есть в этих номерах: ', numbers
        print(sklad[number][0])
        new_img = []
        for a in sklad[number][1]:
            #while height > 1000:
            #    width /= 1.5
            #    height /= 1.5
            a = a.resize((w, h))
            new_img.append(a)
        return new_img


class q2:
    def pictures(path1,number, search=-1, w=200, h=300):
        path = 'q2_1/'
        sklad = {1: ['Дайте определение комплексного числа в алгебраической форме. Приведите тригонометрическую и показательную формы комплексного числа. Выведите формулу площади параллелограмма с вершинами в точках z1 и z2 комплексной плоскости.', 
                    [Image.open(f'{path1}/{path}/1/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/1') if os.path.isfile(os.path.join(f'{path1}/{path}/1', f))]]],
                 2: ['Выведите формулы для извлечения корня n-ой степени из комплексного числа и приведите геометрическую интерпретацию о расположении n значений корня. Какой корень называется примитивным. Приведите свойства примитивных корней.',
                     [Image.open(f'{path1}/{path}/2/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/2') if os.path.isfile(os.path.join(f'{path1}/{path}/2', f))]]],
                 3: ['(картинок нет)Дайте определение наибольшего общего делителя многочленов, наименьшего общего кратного многочленов. Приведите линейное разложение наибольшего общего делителя. Какие многочлены называются взаимно простыми? Приведите соответствующие примеры. Найдите многочлены u(x) и v(x) такие, что (2x^3 − 7x^2 − 9x + 63)u(x) + (x^3 + x^2 − 19x − 9)v(x) = 1.'+
                     '\n Решение: Наибольшим общим делителем НОД (f, g) = (f, g), где f, g ∈ R[x], называется многочлен d(x) ∈ R[x] максимальной степени, на который делятся (без остатка) оба многочлена.\nОбозначение: d(x) = НОД(f, g) = (f, g).\nОпределение. Наименьшим общим кратным НОК(f,g) = (f,g), где f,g ∈ R[x], называется многочлен L(x) ∈ R[x] наименьшей степени, который де- лится (без остатка) на каждый из многочленов f(x) и g(x).\nОбозначение: L(x) = НОK(f, g). \nТеорема. 1) Для ∀f, g ∈ R[x] найдутся d = НОД(f, g) и L = НОK(f, g).\n2) (The polynomial extended euclidean algorithm) При помощи алгоритма\nЕвклида найдутся многочлены u, v ∈ R[x] такие, что fu + gv = НОД(f, g) = d.\nОпределение. Многочлены f, g ∈ R[x] называются взаимно-простыми, если d = НОД(f,g) = 1.\nПример: Пусть p(x) = x**3 - x**2 + x - 1 ; q(x) = x**3 -x**2 + 1, то НОД(p,q) = 1 => они взаимнопростые',
                     [Image.open(f'{path1}/{path}/3/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/3') if os.path.isfile(os.path.join(f'{path1}/{path}/3', f))]]],
                 4: ['Дайте определение неприводимого многочлена. Будет ли неприводимым многочленом над R многочлен вида x^4 + 4? Ответ необходимо обосновать.'+
                     '\n Решение: Многочлен f ненулевой степени из R[x] (или C[x], в общем слу- чае K[x]) называется неприводимым (или неприводимым над полем K), ес- ли он не делится ни на какой другой многочлен g ∈ R[x] меньшей степени, 0 < deg(g) < deg(f).\nНе будет. Он приводим над R так как он делится на другие многочлены меньшей степени которые принадлежат R, разложение:',
                     [Image.open(f'{path1}/{path}/4/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/4') if os.path.isfile(os.path.join(f'{path1}/{path}/4', f))]]],
                 5: ['Дайте определение алгебраической кратности корня многочлена. Приведите соответствующие примеры. Сформулируйте основную теорему алгебры комплексных чисел. Является ли поле C алгебраически замкнутым? Ответ необходимо обосновать.',
                     [Image.open(f'{path1}/{path}/5/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/5') if os.path.isfile(os.path.join(f'{path1}/{path}/5', f))]]],
                 6: ['Приведите (с выводом) формулы Виета для многочлена f ∈ C[z], deg(f) = n',
                     [Image.open(f'{path1}/{path}/6/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/6') if os.path.isfile(os.path.join(f'{path1}/{path}/6', f))]]],
                 7: ['Приведите свойства (с доказательством) комплексных корней для многочленов с вещественными коэффициентами f ∈ R[z], deg(f) = n. Разложите на множители над R многочлен x^5 − 1 ∈ R[x].',
                     [Image.open(f'{path1}/{path}/7/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/7') if os.path.isfile(os.path.join(f'{path1}/{path}/7', f))]]],
                 8: ['Дайте определение многочлена от нескольких переменных. Какой многочлен называется симметричеcким? Приведите выражения основных симметрических многочленов.',
                     [Image.open(f'{path1}/{path}/8/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/8') if os.path.isfile(os.path.join(f'{path1}/{path}/8', f))]]],
                 9: ['Приведите формулы элементарных симметрических многочленов sk(x1, x2, . . . , xn). Укажите их в явном виде для случая n = 4, k = 4.',
                     [Image.open(f'{path1}/{path}/9/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/9') if os.path.isfile(os.path.join(f'{path1}/{path}/9', f))]]],
                 10: ['Приведите формулы Ньютона, которые связывают многочлены Ньютона (степенные суммы) с элементарными симметрическими многочленами sk(x1, x2, . . . , xn).',
                     [Image.open(f'{path1}/{path}/10/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/10') if os.path.isfile(os.path.join(f'{path1}/{path}/10', f))]]],
                 11: ['Приведите основную теорему симметрических многочленов и проиллюстрируйте её на примере симметрического многочлена f(x1,x2,x3)=x1^3*x2+x2^3*x3+x3^3*x1+x1*x2^3+x2*x3^3+x3*x1^3 представив его в виде явного многочлена от элементарных симметрических многочленов.',
                     [Image.open(f'{path1}/{path}/11/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/11') if os.path.isfile(os.path.join(f'{path1}/{path}/11', f))]]],
                 12: ['Дайте определение дискриминанта мночочлена n-ой степени с комплексными коэффициентами и приведите основные свойства дискриминанта многолена. Приведите формулу для определения дискриминанта многочлена и пользуясь этой формулой найдите дискриминант многочлена f(z) = z^3 + a*z + b.' +
                      '\n Решение: *картинка0* \n 1) Дискриминант равен нулю тогда и только тогда, когда многочлен имеет кратные корни. \n2) Дискриминант является симметрическим многочленом относительно корней многочлена и поэтому является многочленом от его коэффициентов; более того, коэффициенты этого многочлена целые независимо от расширения, в котором берутся корни.\n *картинка1*',
                     [Image.open(f'{path1}/{path}/12/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/12') if os.path.isfile(os.path.join(f'{path1}/{path}/12', f))]]],
                 13: ['Дайте определение результанта двух многочленов n-ой и m-ой степеней. Приведите основные свойства результанта многочленов. Найдите многочлены u(x) и v(x) такие, что f(x)u(x) + g(x)v(x) = Res(f(x); g(x)),где f(x) = x4 − 10x2 + 1, g(x) = x4 − 4√2x3 + 6x2 + 4√2x + 1.',
                     [Image.open(f'{path1}/{path}/13/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/13') if os.path.isfile(os.path.join(f'{path1}/{path}/13', f))]]]}
        if number == -1:
            numbers = []
            for i, j in sklad.items():
                if search in j[0]:
                    numbers.append(i)
            return 'есть в этих номерах: ', numbers
        print(sklad[number][0])
        new_img = []
        for a in sklad[number][1]:
            #while height > 1000:
            #    width /= 1.5
            #    height /= 1.5
            a = a.resize((w, h))
            new_img.append(a)
        return new_img


class q3:
    def pictures(path1,number, search=-1, w=200, h=300):
        path = 'q3_1/'
        sklad = {1: ['Дайте определение линейного пространства и приведите примеры линейных пространств. Является ли линейным пространством V1 = {f ∈ R4[x] : f(5) = 0}, V2 = {f ∈ R4[x] : f(5) = 2}? Ответ необходимо обосновать.', 
                    [Image.open(f'{path1}/{path}/1/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/1') if os.path.isfile(os.path.join(f'{path1}/{path}/1', f))]]],
                 2: ['Дайте определение линейной зависимости и независимости системы векторов. Что называется базисом конечномерного векторного пространства? Как определяется размерность конечномерного векторного пространства. Найдите размерность и какой-нибудь базис линейного пространства V = {f ∈ R4[x] : f(3) = 0}.',
                     [Image.open(f'{path1}/{path}/2/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/2') if os.path.isfile(os.path.join(f'{path1}/{path}/2', f))]]],
                 3: ['Дайте определение матрицы перехода от одного базиса к другому линейного пространства. Сформулируйте основные свойства матрицы перехода. Приведите примеры матрицы перехода.',
                     [Image.open(f'{path1}/{path}/3/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/3') if os.path.isfile(os.path.join(f'{path1}/{path}/3', f))]]],
                 4: ['Дайте определение линейного подпространства. Приведете основные примеры линейных подпространств. Является ли объединение двух линейных подпространств линейным подпространством? Ответ необходимо обосновать.',
                     [Image.open(f'{path1}/{path}/4/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/4') if os.path.isfile(os.path.join(f'{path1}/{path}/4', f))]]],
                 5: ['Дайте определение пересечения, суммы линейных подпространств. Сформулируйте теорему о размерности суммы подпространств. Какая сумма называется прямой? Приведите пример суммы подпространств, которая не является прямой (с обоснованием).',
                     [Image.open(f'{path1}/{path}/5/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/5') if os.path.isfile(os.path.join(f'{path1}/{path}/5', f))]]],
                 6: ['Дайте определение линейного многообразия линейного пространства. Как определяется размерность линейного многообразия? Является ли V = {x ∈ R5: x1 − x2 + x3 − x4 − 5x5 = 0, x2 − x3 + 2x4 + 4x5 = 1} линейным многообразием? Если да, то найдите его размерность.',
                     [Image.open(f'{path1}/{path}/6/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/6') if os.path.isfile(os.path.join(f'{path1}/{path}/6', f))]]],
                 7: ['Дайте определение линейного оператора. Что называется ядром и образом линейного оператора? Как связаны дефект линейного оператора и ранг линейного оператора в конечномерном линейном пространстве.',
                     [Image.open(f'{path1}/{path}/7/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/7') if os.path.isfile(os.path.join(f'{path1}/{path}/7', f))]]],
                 8: ['Дайте определение матрицы линейного оператора. Найдите ранг линейнго оператора, если ϕ : R3 → R3, ϕ(x) = {x1; x1 + x2; x1 + x2 + x3}. Как изменится матрица линейного оператора при переходе к другому базису? Ответ необходимо обосновать.',
                     [Image.open(f'{path1}/{path}/8/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/8') if os.path.isfile(os.path.join(f'{path1}/{path}/8', f))]]],
                 9: ['Дайте определение инвариантного линейного подпространства относительно линейного оператора. Будут ли ядро и образ линейного оператора инвариантными подпространствами? Ответ необходимо обосновать.',
                     [Image.open(f'{path1}/{path}/9/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/9') if os.path.isfile(os.path.join(f'{path1}/{path}/9', f))]]],
                 10: ['Дайте определение собственного вектора и соответствующего собственного значения линейного оператора. Что называется спектром и резольвентой линейного оператора.',
                     [Image.open(f'{path1}/{path}/10/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/10') if os.path.isfile(os.path.join(f'{path1}/{path}/10', f))]]],
                 11: ['Дайте определение характеристического многочлена линейного оператора. Покажите, что характеристический многочлен не зависит от выбора базиса.',
                     [Image.open(f'{path1}/{path}/11/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/11') if os.path.isfile(os.path.join(f'{path1}/{path}/11', f))]]],
                 12: ['Дайте определение собственного подпространства линейного оператора. Как связаны алгебраическая и геометрическая кратности собственного значения. Приведите пример линейного оператора и соответствующего собственного значения, геометрическая кратность которого меньше его алгебраической кратности.',
                     [Image.open(f'{path1}/{path}/12/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/12') if os.path.isfile(os.path.join(f'{path1}/{path}/12', f))]]],
                 13: ['Дайте определение диагонализируемого оператора. Приведите критерий диагонализируемости.',
                     [Image.open(f'{path1}/{path}/13/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/13') if os.path.isfile(os.path.join(f'{path1}/{path}/13', f))]]],
                 14: ['Приведите основные свойства собственных чисел и собственных векторов линейных операторов.',
                     [Image.open(f'{path1}/{path}/14/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/14') if os.path.isfile(os.path.join(f'{path1}/{path}/14', f))]]],
                 15: ['Сформулируйте теорему Гамильтона – Кэли. Приведедите пример, иллюстрирующий теорему Гамильтона – Кэли',
                     [Image.open(f'{path1}/{path}/15/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/15') if os.path.isfile(os.path.join(f'{path1}/{path}/15', f))]]],
                 16: ['Дайте определение минимального многочлена матрицы линейного оператора. Как связаны характеристический и минимальный многочлены? Приведите пример минимального многочлена для матрицы.',
                     [Image.open(f'{path1}/{path}/16/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/16') if os.path.isfile(os.path.join(f'{path1}/{path}/16', f))]]]
                 
                 }
        if number == -1:
            numbers = []
            for i, j in sklad.items():
                if search in j[0]:
                    numbers.append(i)
            return 'есть в этих номерах: ', numbers
        print(sklad[number][0])
        new_img = []
        for a in sklad[number][1]:
            #while height > 1000:
            #    width /= 1.5
            #    height /= 1.5
            a = a.resize((w, h))
            new_img.append(a)
        return new_img

class q4:
    def pictures(path1,number, search=-1, w=200, h=300):
        path = 'q4_1/'
        sklad = {8: ['Пусть A Найдите такое n ∈ N, чтобы  и используя биномиальную формулу, вычислите An для всех целых положительных n.' +
        '\nИтак, для начала найдём первый n, с которым получается нулевая матрица:'+
        '\nA = Matrix([[1, 0, 1], [-1, 1, Rational(1, 2)], [0, 0, 1]])'+
        '\nI3 = eye(3)'+
        '\nO3 = zeros(3)'+
        '\nfor n in range(100):'+
        '\n\tif (A - I3) ** n == O3:'+
        '\n\t\tprint(n)'+
        '\n\t\tbreak'+
        '\nРезультат: 3 После 3 степени с любым n будет получаться нулевая матрица, потому что можно разложить как (A - I)**3(A-I)**(n-3) для n>=3'+
        '\nТеперь найдём An для всех целых положительных n:',
        [Image.open(f'{path1}/{path}/8/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/8') if os.path.isfile(os.path.join(f'{path1}/{path}/8', f))]]],
        11: ['Представить матрицу в виде суммы симметрической B и кососимметрической C матриц с вещественными коэфициентами.'+
        '\n Пусть A = P + Q Где P - симметрическая, Q - кососимметрическая тогда '+
        '\nA = Matrix([[1, -9, 13], [12, -3, 9], [3, 4, 5]])'+
        '\nP = (A + A.T)/2; Q = (A - A.T)/2'+
        '\nP, Q, P + Q',
        [Image.open(f'{path1}/{path}/11/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/11') if os.path.isfile(os.path.join(f'{path1}/{path}/11', f))]]],
        12: ['Для симметрической матрицы  найдите унипотентную матрицу  и диагональную матрицу  такие, что U.T * A * U = D'+
        '\nu1, u2, u3, d1, d2, d3 = symbols("u1 u2 u3 d1 d2 d3")'+
        "\nA = Matrix(3,3,[11, 33, 5,33, 7, -2,5, -2, 9])"+
        "\nD = Matrix(3,3,[d1, 0, 0, 0, d2, 0, 0, 0, d3])"+
        "\nU = Matrix(3,3,[1, u1, u2, 0, 1, u3, 0, 0, 1])"+
        "\nB = U.T * A * U - D"+
        "\nans = solve(B)"+
        "\nU.subs(ans),D.subs(ans),ans,B",
        [Image.open(f'{path1}/{path}/12/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/12') if os.path.isfile(os.path.join(f'{path1}/{path}/12', f))]]],
        16: ['Пусть A**3 = O а) Покажите, что б) Используя a), найдите (I + A)**-1',
        [Image.open(f'{path1}/{path}/16/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/16') if os.path.isfile(os.path.join(f'{path1}/{path}/16', f))]]],
        19: ['Пусть матрица A ∈ Mn(R) такова, что A**3 = A . Покажите, что матрица (I - 2A**2) обратима и найдите (I - 2A**2)**-1',
        [Image.open(f'{path1}/{path}/19/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/19') if os.path.isfile(os.path.join(f'{path1}/{path}/19', f))]]],
        21: ['Пусть A,B ∈ Mn(R) таковы,что A+B = In  A2 +B2 = On.Покажите,что A и B обратимы, причем (A−1 + B−1)n = 2**n * I',
        [Image.open(f'{path1}/{path}/21/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/21') if os.path.isfile(os.path.join(f'{path1}/{path}/21', f))]]],
        22: ['Пусть A ∈ Mn(R) такова, что A**-1 = In - A. Покажите, что A**6 - In = On.',
        [Image.open(f'{path1}/{path}/22/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/22') if os.path.isfile(os.path.join(f'{path1}/{path}/22', f))]]],
        27: ['Вывести формулу для объема тетраэдра с вершинами A(x1;y1;z1),B(x2;y2;z2),C(x3;y3;z3) и D(x4; y4; z4):',
        [Image.open(f'{path1}/{path}/27/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/27') if os.path.isfile(os.path.join(f'{path1}/{path}/27', f))]]],
        28: ['Не раскрывая определитель слева, покажите, что:',
        [Image.open(f'{path1}/{path}/28/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/28') if os.path.isfile(os.path.join(f'{path1}/{path}/28', f))]]],
        35: ['Пусть  – матрица порядка n, ∆ = det(A) – ее определитель. Пусть adj(A) – присоединенная матрица, , здесь Aij – алгебраическое дополнение к элементу aij . Покажите, что если A – обратима, то справедливо равенство adj(adj(A)) = det**(n-2) * A',
        [Image.open(f'{path1}/{path}/35/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/35') if os.path.isfile(os.path.join(f'{path1}/{path}/35', f))]]],
        37: ['Найдите значения i и k так, чтобы произведение (на фотке) входило в определитель 7-ого порядка со знаком плюс.',
        [Image.open(f'{path1}/{path}/37/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/37') if os.path.isfile(os.path.join(f'{path1}/{path}/37', f))]]],
        39: ['Представьте комплексное число в алгебраической форме, второй пикчей - теория как сделать ешку '+
        '\nf = ((-1+I*sqrt(3))**15)/((1-I*1)**20) + ((-1-I*sqrt(3))**15)/((1+I*1)**20)'+
        '\f.expand()',
        [Image.open(f'{path1}/{path}/39/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/39') if os.path.isfile(os.path.join(f'{path1}/{path}/39', f))]]],
        41: ['номер. Пусть (пикча 0) Покажите, что a и b являются корнями квадратного трехчлена (пикча 1) (первые 2 пикчи - из условия)',
        [Image.open(f'{path1}/{path}/41/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/41') if os.path.isfile(os.path.join(f'{path1}/{path}/41', f))]]],
        43: ['Пусть A и C действительные, а B –комплексные постоянные и пусть AC < |B| 2 . Покажите, что уравнение. является уравнением окружности, а также найти центр этой окружности и её радиус.',
        [Image.open(f'{path1}/{path}/43/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/43') if os.path.isfile(os.path.join(f'{path1}/{path}/43', f))]]],
        45: ['Разделите многочлен f(x) с остатком r(x) на многочлен g(x) и проверьте равенство f(x) = h(x)g(x) + r(x):',
        [Image.open(f'{path1}/{path}/45/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/45') if os.path.isfile(os.path.join(f'{path1}/{path}/45', f))]]],
        47: ['Определить алгебраическую кратность всех корней многочлена f ∈ C[x], где (смотри многочлен в коде)'+
        '\nx = symbols("x", dtype = complex)'+
        '\nf =  x ** 4 + (3 - 8 * I) * x ** 3 - (21 + 18 * I) * x ** 2 - (33 - 20 * I) * x + 6 + 18 * I'+
        '\nci = roots(f, x)'+
        '\nci'+
        '\nФункция roots возвращает словарик типа "корень: кратность". (можете руками отдельно корни переписать или в общем виде по скобочкам разбить)',
        [Image.open(f'{path1}/{path}/47/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/47') if os.path.isfile(os.path.join(f'{path1}/{path}/47', f))]]],
        49: ['Разложить на линейные множители над полем комплексных чисел f(z) = z** 8 − 1 − i.'+
        '\nz = symbols("z", complex=True)'+
        '\nf = x**8 - 1 - I'+
        '\nsolve(f)',
        [Image.open(f'{path1}/{path}/49/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/49') if os.path.isfile(os.path.join(f'{path1}/{path}/49', f))]]],
        51: ['Найдите все значения параметра a ∈ R, при котором уравнение (смотри код) имеет кратные корни.'+
        '\na = symbols("a")'+
        '\nx = symbols("x")'+
        '\nf = x**11 - 2*x**10 + x**9 - 2*x**3 + 11*x**2 - 16*x  + a '+
        '\n[N(i) for i in solve(discriminant(f))] # (многочлен имеет кратные корни если дискриминант = 0)',
        [Image.open(f'{path1}/{path}/51/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/51') if os.path.isfile(os.path.join(f'{path1}/{path}/51', f))]]],
        53: ['Найдите все значения параметра a ∈ R, при котором уравнение (смотри код) имеет кратные корни.'+
        '\nx, y = symbols("x, y")'+
        '\nf = x**2 + (x-4)*y - 2*x + y**2 + 3'+
        '\ng = x**3 - x**2 + (x+7)*y - 5*x + y**3 - 5*y**2 - 3'+
        '\nf, g'+
        '\nY = solve(resultant(f, g))'+
        "\nX = solve(resultant(f, g, y))"+
        "\nY, X",
        [Image.open(f'{path1}/{path}/53/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/53') if os.path.isfile(os.path.join(f'{path1}/{path}/53', f))]]],
        55: ['Разложите на линейные и квадратичные множители над полем вещественных чисел многочлен f(x)=x^12 +x^8 +x^4 +1.'+
        '\nf = x**12 + x**8 + x**4 + 1'+
        '\nf_1 = x**4 + 1'+
        '\ns1 = solve(f1)'+
        '\nf1 = expand((x - s1[0]) * (x - s1[1]))'+
        '\nf2 = expand((x - s1[2]) * (x - s1[3]))'+
        '\n#получается разложим x**8 + 1 аналогично'+
        '\nf_2 = x**4 - sqrt(2) * x**2 + 1'
        '\nf_3 = x**4 + sqrt(2) * x**2 + 1'+
        '\ns2 = solve(f_2)'+
        '\nf3 = expand((x - s2[0]) * (x - s2[1]))'+
        '\nf4 = expand((x - s2[2]) * (x - s2[3]))'+
        '\ns3 = solve(f_3)'+
        '\nf5 = expand((x - s3[0]) * (x - s3[1]))'+
        '\nf6 = expand((x - s3[2]) * (x - s3[3]))'+
        '\nexpand(f1*f2*f3*f4*f5*f6)',
        [Image.open(f'{path1}/{path}/55/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/55') if os.path.isfile(os.path.join(f'{path1}/{path}/55', f))]]],
        57: ['Пусть e1, . . . e4 – стандартный базис V = R4. Пусть векторы e′1, . . . e′4 и x заданы своими координатами в базисе (e): e′1 = {1,2,−1,−2},e′2 = {2,3,0,−1},e′3 = {1,2,1,4},e′4 = {1,3,−1,0}, x = {7, 14, −1, 2}. Покажите, что система e′1, . . . e′4 – также базис пространства V , найдите матрицу пере- хода C = C(e)→(e′). Найдите также координаты вектора x в этом базисе.'+
        '\nm,n = 4,4'+
        '\nV = eye(n)'+
        '\ne_ = Matrix(n,m,[1,2,-1,-2,2,3,0,-1,1,2,1,4,1,3,-1,0]).T'+
        '\nx = Matrix([7, 14, -1, 2]) # линейно независимы => базис'+
        '\ne_.rref()'+
        '\ntransition_vectors = []'+
        '\ne_v = np.array_split(list(e_.T), m)'+
        '\nbasis_e = (np.array_split(list(V), m))[0]'+
        '\nfor i in range(1,m):'+
        '\n\tbasis_e += (np.array_split(list(V), m))[i]'+
        '\nfor i in range(m):'+
        '\n\ttransition_vectors += [e_v[i]/basis_e[i]]'+
        '\ntransition_vectors = np.array(transition_vectors)'+
        '\nC = Matrix(transition_vectors).T'+
        '\nC'+
        '\n# поиск икса в штриховом базисе'+
        '\nx_ = C**-1 * x'+
        '\nx_',
        [Image.open(f'{path1}/{path}/57/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/57') if os.path.isfile(os.path.join(f'{path1}/{path}/57', f))]]],
        59: ['Найдите базис суммы L1 + L2 и пересечения L1 ∩ L2 линейных оболочек L1, L2 систем векторов пространства V'+
        "\nL1 = [[1,2,1,-2], [2,3,1,0], [1,2,2,-3]]"+
        "\nL2 = [[1,1,1,1], [1,0,1,-1], [1,3,0,-4]]"+
        "\nMatrix(L1).T.rank(), Matrix(L2).T.rank()"+
        "\n#rank = 4 => базис L1 пересеч L2 имеет dim 6 -4 = 2:"+
        "\nL1ppL2 = Matrix(L1+L2).T"+
        "\nL1ppL2.rank(),L1ppL2.echelon_form()"+
        "\n#ранк выбранных векторов = 2 значит они линейно независимы => образуют базис"+
        "\nbasis_perese4 = Matrix(2,4,(list(L1[0])+list(L1[1])))"+
        "\nbasis_perese4.rank()"+
        "\n#базис пересечения"+
        "\nbasis_perese4.T"+
        "\n# L1 + L2:"+
        "\nL1ppL2 = Matrix(L1+L2)"+
        "\nL1ppL2.rank(),L1ppL2.echelon_form()"+
        "\nbasis_sum = Matrix(4,4,list(Matrix(L1))+list(L2[1]))"+
        "\nbasis_sum.T",
        "Для нахождения объединения Вы строите такую матрицу: Транспонируете Ваши вектора столбцы в вектора строки. Далее последовательно составляете матрицу 6*3 где i-ая строка отвечает i-ому вектору, а j-столбец j-м координатам соответствующих векторов. Далее, как в методе Гаусса, приводите это дело к диагональному виду откидывая все нулевые строки. Ранг этой матрицы будет отвечать размерности объединения Ваших оболонок. Пересечение находится так: Ваши вектора остаются векторами столбцами. Сначала выбрасываете из ваших линейных оболочек те вектора, которые выражаются через другие, то-есть оставляете только базисные вектора. Пускай это будет x1,x2 и y1,y2 Далее составляете такую матрицу (x1x2|y1y2)Далее с помощью преобразований над столбцами, оставляя скажем левую часть не тронутой, Вы приводите подматрицу справа к виду, как можно близкому к диагональному. Делать это надо до тех пор, пока оставшиеся ненулевые вектора станут линейно независимыми.Количество нулевых векторов, которые в итоге останутся и будет размерностью пересечения.",
        [Image.open(f'{path1}/{path}/59/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/59') if os.path.isfile(os.path.join(f'{path1}/{path}/59', f))]]],
        61: ['Пусть L1 и L2 – подпространства V  Покажите,что V = L1⊕L2 и представьте x = {1,2,3,4} в виде суммы x = y+z,y ∈ L1,z ∈ L2. прямая сумма',
        [Image.open(f'{path1}/{path}/61/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/61') if os.path.isfile(os.path.join(f'{path1}/{path}/61', f))]]],
        63: ['Пусть L = {f R4[x]: f(6) = 0} a) Найдите базис подпространства L; b) Дополните в п. а) базис до базиса всего пространства V = R4[x]; c) Найдите прямое дополнение L2 к L1,т.е. R4[x] = L1 ⊕ L2'+
        '\n',
        [Image.open(f'{path1}/{path}/63/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/63') if os.path.isfile(os.path.join(f'{path1}/{path}/63', f))]]],
        67: ['Выясните, можно ли матрицу A (e) ϕ линейного оператора привести к диагональному виду. Найдите собственные значения, собственный базис, матрицу перехода и соотвествующий вид матрицы линейного оператора в новом базисе. ',
        [Image.open(f'{path1}/{path}/67/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/67') if os.path.isfile(os.path.join(f'{path1}/{path}/67', f))]]],
        34: ["Для матрицы найдите: a) базисный минор с наименьшим значением; б) ранг матрицы, составленный из всех базисных миноров. "
         "#34\n alpha = symbols('alpha')\n beta = symbols('beta')\n a1, a2, a3, a4 = symbols('a1 a2 a3 a4')\n a = [[5*i + j + 1for j in range(5)] for i in range(4)]\n Matrix(a)\n \n Matrix(a).rank() #найдем ранг матрицы чтобы понять размерность базисного минора (размерность будет 2*2)\n arrs = [[0 for i in range(10)] for j in range(6)]\n i, j = -1, -1\n mi = 10**100\n for i1, i2 in sorted(set([tuple(sorted(i)) for i in permutations('1234', r=2)])):\n     i += 1\n     j = -1\n     for j1, j2 in sorted(set([tuple(sorted(i)) for i in permutations('12345', r=2)])):\n         j += 1\n         minor = Matrix([[a[int(i1) - 1][int(j1) - 1], a[int(i1) - 1][int(j2) - 1]], [a[int(i2) - 1][int(j1) - 1], a[int(i2) - 1][int(j2) - 1]]])\n         mi = min(det(minor), mi)\n         arrs[i][j] = det(minor)\n Matrix(arrs).rank(), mi\n",
         [Image.open(f'{path1}/{path}/34/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/34') if os.path.isfile(os.path.join(f'{path1}/{path}/34', f))]]],
    36: ['Найдите число инверсий и определите четность перестановки',
         [Image.open(f'{path1}/{path}/36/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/36') if os.path.isfile(os.path.join(f'{path1}/{path}/36', f))]]],
    38: ['С каким знаком входит в определитель порядка n произведение элементов побочной диагонали? ', [Image.open(f'{path1}/{path}/38/{x}') for x in
        [f for f in os.listdir(f'{path1}/{path}/38') if os.path.isfile(os.path.join(f'{path1}/{path}/38', f))]]],
    40: ['Решить систему уравнений над полем C', [Image.open(f'{path1}/{path}/40/{x}') for x in
        [f for f in os.listdir(f'{path1}/{path}/40') if os.path.isfile(os.path.join(f'{path1}/{path}/40', f))]]],
    42: ['42 номер.Изобразить на комплексной плоскости множество точек, удовлетворяющих условию:', [Image.open(f'{path1}/{path}/42/{x}') for x in
        [f for f in os.listdir(f'{path1}/{path}/42') if os.path.isfile(os.path.join(f'{path1}/{path}/42', f))]]],
    44: ['Принадлежат ли точки  на комплексной плоскости одной окружности, где  Если эти точки лежат на одной окружности, то найдите центр и радиус такой окружности. Берём 3 точки и на 4й проверяем:\n \n x0, y0, r = symbols(x0  y0  r)\n \n \n equations = []\n for x, y in [(-1, 4), (-2, 4), (9, -6)]:\n     equations.append((x-x0)**2 + (y-y0)**2 - r**2)\n equations\n \n \n Решим это с помощью солв:\n \n ans = solve([i for i in equations], (x0, y0, r))\n ans\n \n \n Т.к. радиус не может быть отрицательным, второе решение верное. Если бы точки не принадлежали одной окружности, то решений бы не было. Итак, подставим последнюю точку:\n \n x0, y0, r = ans[1]\n x = -6\n y = 3\n (x-x0)**2 + (y-y0)**2 == r**2\n \n Результат: True\n',
         [Image.open(f'{path1}/{path}/44/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/44') if os.path.isfile(os.path.join(f'{path1}/{path}/44', f))]]],

    48: ['При каких a и b многочлен f(x)=x^5+ax^3+b имеет двойной корень,отличный от нуля?', [Image.open(f'{path1}/{path}/48/{x}') for x in
        [f for f in os.listdir(f'{path1}/{path}/48') if os.path.isfile(os.path.join(f'{path1}/{path}/48', f))]]],
    50: ['Найдите значение симметрического многочлена F от корней  многочлена f(x), если Итак, введём в Жупутор Нотбук наши многочлены:\n \n c1, c2, c3, c4, x = symbols(c1, c2, c3, c4, x)\n F = (c1**5*c2**3 + c1**3*c2**5) +(c1**5*c3**3 + c1**3*c3**5) + (c1**5*c4**3 + c1**3*c4**5) + (c2**5*c3**3 + c2**3*c3**5) +(c2**5*c4**3 + c2**3*c4**5) + (c3**5*c4**3 + c3**3*c4**5)\n f = 3*x**4 + 2*x**3 + 5*x**2 + x + 7\n F, f\n \n \n Теперь найдём корни f (насколько то возможно приближенные по точности):\n \n root = nroots(f)\n root\n \n \n \n Подставим в F значения c1…4 и упростим:\n \n for i, c in zip(range(4), (c1, c2, c3, c4)):\n  F = F.subs(c, root[i])\n \n expand(F)\n \n Ответ: 5.10699588477367\n',
         [Image.open(f'{path1}/{path}/50/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/50') if os.path.isfile(os.path.join(f'{path1}/{path}/50', f))]]],

    52: ['Найти все значения параметра b∈R, при которых многочлены f(x) и g(x) имеют общие корни,если f(x)=x3 −5x2 −7x−1,g(x)=x3 −8x2 +9x+b. x=Symbol(x)\n f=x**3-5*x**2-7*x-1\n g=x**3-8*x**2+9*x+b\n res=factor(resultant(f,g,x)) #результант должен быть равен 0\n solveset(res)\n',
         [Image.open(f'{path1}/{path}/52/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/52') if os.path.isfile(os.path.join(f'{path1}/{path}/52', f))]]],

    54: ['Пусть f(x) = x 4 − 10x 2 + 1 и g(x) = x 4 − 4 √ 2x 3 + 6x 2 + 4√ 2x + 1. Найдите функции u(x) и v(x) такие, что fu + gv = Res(f, g) x = symbols(x, complex=True)\n f = x**4 - 10*x**2 +1\n g = x**4 - 4*(sqrt(2))*x**3 +6*x**2 +4*(sqrt(2))*x+1\n f, g\n \n solve(f)\n \n s2 = solve(g)\n s2\n \n resultant(f, g)\n \n #видим что на первый взгляд корни отличаются но при этом результант равен нулю => общие корни есть, тогда поделим f\n #на произведение корней\n \n expand((x - s2[0]) * (x - s2[1]))\n \n div(f, (x - s2[0])*(x - s2[1]))\n \n # => Пусть x**2 - 2*sqrt(2)*x - 1 = m, а x**2 + 2*sqrt(2)*x - 1 = z, тогда f = m*z, g = m**2 => f*u + g*v = m*z*u + m**2*v = 0\n # => v = z и u = -m\n \n u = x**2 - 2*sqrt(2)*x - 1\n v = -(x**2 + 2*sqrt(2)*x  - 1)\n expand(f * u + g * v)',
         [Image.open(f'{path1}/{path}/54/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/54') if os.path.isfile(os.path.join(f'{path1}/{path}/54', f))]]],

    56: ['Проверьте, что многочлен f(x1, x2, x3) является симметрическим и выразить его в виде многочлена F от элементарных симметрических многочленов, если f(x1, x2, x3) = (3x1 − x2 − x3) (3x2 − x1 − x3) (3x3 − x1 − x2) Воспользуемся функцией симметрайз библиотеки симпай:\n \n x1, x2, x3, x4 = symbols(x1 x2 x3 x4)\n f = (3*x1 - x2 - x3)*(3*x2 - x1 - x3)*(3*x3 - x1 - x2)\n F = symmetrize(f, formal=True)\n F\n \n Результат:\n Список в кортеже это и есть разложение от элементарных симметрических многочленов. \n Проверим:\n \n factor(F[0].subs(F[2]))\n \n Результат: \n',
         [Image.open(f'{path1}/{path}/56/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/56') if os.path.isfile(os.path.join(f'{path1}/{path}/56', f))]]],

    58: ['.Пусть e0 = 1, e1 = x, e2 = x2, e3 = x3, e4 = x4 – стандартный базис пространства многочленов V = R4[x]. Рассмотрим семейство (систему) многочленов e′0, . . . e′4 и P4(x): e′0 =1,e′1 =(x−7),e′2 =(x−7)2,e′3 =(x−7)3,e′4 =(x−7)4, P4(x) = 1+2x−3x2 +4x3 −9x4.Покажите, что система e′0, . . . e′4 – также базис пространства V , найдите матрицу перехода C = C(e)→(e′). Найдите координаты P4(x) в этом базисе. x = symbols(x)\n V = [1,x,x**2,x**3,x**4]\n e = [1,(x-7),(x-7)**2,(x-7)**3,(x-7)**4]\n P = [1,2,-3, 4,-9]\n \n показываем что система также базис\n Matrix(e).T  == Matrix(factor([x for x in (Matrix(V).T * C)])).T\n \n координаты в этом базисе\n P_ = C**-1 * Matrix(P)',
         [Image.open(f'{path1}/{path}/58/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/58') if os.path.isfile(os.path.join(f'{path1}/{path}/58', f))]]],
    60: ['Найдите базис суммы L1 + L2 и пересечения L1 ∩ L2 подпространств L1 , L2 пространства V =R4: L2 = x2 − 3x4 = 0 L1 = (np.array([1,2,1,-2]),np.array([2,3,1,0]),np.array([1,2,2,-3]))\n L2 = (np.array([1,1,1,1]),np.array([1,0,1,-1]),np.array([1,3,0,-4]))\n \n Matrix(L1).T.rank(), Matrix(L2).T.rank()\n \n Пересечение\n #rank = 4 => базис L1 пересеч L2 имеет dim 6 -4 = 2:\n L1ppL2 = Matrix(L1+L2).T\n L1ppL2.rank(),L1ppL2.echelon_form()\n \n #ранк выбранных векторов = 2 значит они линейно независимы => образуют базис\n basis_perese4 = Matrix(2,4,(list(L1[0])+list(L1[1])))\n basis_perese4.rank()\n \n #базис пересечения\n basis_perese4.T\n \n #rank L1 u rank L2 == 3 => все столбцы - базисные\n Matrix(L1).rank(),Matrix(L2).rank()\n \n Сумма\n # L1 + L2:\n L1ppL2 = Matrix(L1+L2)\n L1ppL2.rank(),L1ppL2.echelon_form()\n \n basis_sum = Matrix(4,4,list(Matrix(L1))+list(L2[1]))\n \n basis_sum.T',
         [Image.open(f'{path1}/{path}/60/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/60') if os.path.isfile(os.path.join(f'{path1}/{path}/60', f))]]],
    62: ['Линейное подпространство L ∈ V = R^5 задано в виде  Найдите три подпространства L2, L3, L4 ∈ V , ни одно из которых не равно {0}, такие, что V = L1 ⊕ L2 ⊕ L3 ⊕ L4. x, y, z, u, v = symbols(x, y,z ,u, v)\n a = Matrix([x, y, x+y, x-y, 2*x])\n a1 = a.subs(x, 0).subs(y, 1)\n a2 = a.subs(x, 1).subs(y, 0)\n a1, a2\n \n L2 = Matrix([0, 0, z, 0, 0])\n L3 = Matrix([0, 0, 0, v, 0])\n L4 = Matrix([0, 0, 0, 0, u])\n V = Matrix([[a1, a2, L2, L3, L4]])\n V\n \n V.rref(),',
         [Image.open(f'{path1}/{path}/62/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/62') if os.path.isfile(os.path.join(f'{path1}/{path}/62', f))]]],

    64: [' Пусть прямая L1 в V = R 4 задана в виде Пусть гиперплоскость L2 задана в виде уравнения Покажите, что V = L1 ⊕ L2 и найдите проекции y ∈ L1 и z ∈ L2 вектора x = {1, 2, 3, 4} на эти подпространства при проектировании, параллельном L1 и L2, т.е. представьте x в виде x = y + z, y ∈ L1, z ∈ L2.',
         [Image.open(f'{path1}/{path}/64/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/64') if os.path.isfile(os.path.join(f'{path1}/{path}/64', f))]]],

    68: ['Найдите минимальный многочлен матрицы  l = Symbol(lamda) \n A = Matrix([[-3, 7, -6, -1, 8, -3, -2], [1, -5, 8, -3, -5, 4, -5], [1, 3, -4, 6,\n -2, 0, 8], [-1, 11, -12, 9, 3, -3, 9], [-3, 11, -12, 5, 8, -4, 6], [-3, 2, 1, -4, 4, 1, -7], [1, -5, 6, -2,\n -4, 3, -2]])\n f=factor(A.charpoly().as_expr())\n f\n \n \n A1=A-l*eye(7)\n A1\n',
         [Image.open(f'{path1}/{path}/68/{x}') for x in [f for f in os.listdir(f'{path1}/{path}/68') if os.path.isfile(os.path.join(f'{path1}/{path}/68', f))]]]
        }
        if number == -1:
            numbers = []
            for i, j in sklad.items():
                if search in j[0]:
                    numbers.append(i)
            return 'есть в этих номерах: ', numbers
        print(sklad[number][0])
        new_img = []
        for a in sklad[number][1]:
            #while height > 1000:
            #    width /= 1.5
            #    height /= 1.5
            a = a.resize((w, h))
            new_img.append(a)
        return new_img

class q6:
    def pictures(number, search=-1):
        sklad = {1: ['На двумерной координатной плоскости заданы точки: A(25, 48), B(2, 34) и C(32,7). Пусть D(X,Y) - ближайшая к А точка прямой ВС. Найдите точку D и расстояние R от А до D. Укажите в ответе: 1) X, первую координату точки D; 2) Y, вторую координату точки D; 3) R, расстояние от А до D.', 
                    'Решение: *тут должна была быть картинка с рисункам по координатам, просто проведи высоту на противолежащую сторону*, тк AD _|_ BC => векторы AD*BC = 0.'+
                    '\n Наш путь: найдём |AD|, потом решим систему, где 1 урав - произ векторов, а 2 - формула |AD|. Код:'+
                    '\nA = (25, 48); B = (2, 34); C = (32, 7)'+
                    '\nAB = sqrt((A[0] - B[0]) ** 2 + (A[1] - B[1]) ** 2)'+
                    '\nBC = sqrt((C[0] - B[0]) ** 2 + (C[1] - B[1]) ** 2)'+
                    '\nAC = sqrt((A[0] - C[0]) ** 2 + (A[1] - C[1]) ** 2)'+
                    '\ncosA = -(AB ** 2 - AC ** 2 - BC ** 2)/(2 * AC * BC)'+
                    '\nDC = cosA * AC'+
                    '\nAD = sqrt(AC ** 2 - DC ** 2)'+
                    '\nx, y = symbols("x y")'+
                    '\nADv = Matrix([x - 25, y - 48]); BCv = Matrix([B[0] - C[0], B[1] - C[1]])'+
                    '\n# Av*Bv = xa*ya + xb*yb, у нас ADv * BCv = 0 тк угол 90 градусов, DC **2 = (x - C[0]) ** 2 + (y - C[1]) ** 2'+
                    '\nsolve((ADv.T * BCv, (x - A[0]) ** 2 + (y - A[1]) ** 2 - AD ** 2), (x, y))'+
                    '\n(выведет коорды, посмотреть, какая подходит по рисунку)'],
                 2: ['Для каждого k = 1,… п обозначим с, вектор-столбец размерности п, такой, что его элемент с номером к равен 1, а все остальные элементы равны 0. Пусть о : {1,…n} -> {1,…n} - некоторая перестановка первых п натуральных чисел. Матрица А однозначно определяется условиями: = Ca(k), k = 1,…п. Известно, что п = 12 и результатом применения о к последовательности 1,…, 12 будет следующий ряд чисел: 4, 3, 9, 6, 5, 2, 8, 1, 7, 12, 11, 10. Найдите: 1) след матрицы А°; 2) наименьшеенатуральное т, такое, что след матрицы А" равен 12.', 
                    '\narr = [0] * 12'+
                    '\narr[4-1] = 1'+
                    '\na = Matrix(arr)'+
                    '\nfor i in [3, 9, 6, 5, 2, 8, 1, 7, 12, 11, 10]:'+
                    '\n    arr = [0] * 12'+
                    '\n    arr[i - 1] = 1'+
                    '\n    a = Matrix.hstack(a, Matrix(arr))'+
                    '\ntrace(a**6) # первый ответ: 4'+
                    '\nfor m in range(1, 1000):'+
                    '\n    if trace(a ** m) == 12:'+
                    '\n        print(m) # второй ответ: 8'+
                    '\n        break'],
                 3: ['Дана матрица: A = [12 11 21, 26 10 22, 19 23 29] . Пусть Z - собственное значение матрицы A с  наибольшей мнимой частью. Найдите Z и соответствующий этому собственному значению собственный вектор X, первая координата которого равна 1, X = (1,U, V). В ответе укажите: 1) мнимую часть Z; 2) действительную часть U.', 
                    '\nA = Matrix([[12, 11, 21], [26, 10, 22], [19, 23, 29]])'+
                    '\nznachs = list(map(N, A.eigenvals()))'+
                    '\n# вывод [58.9947386052553, −3.99736930262764+4.76115037493966i, −3.99736930262764−4.76115037493966i]'+
                    '\n# наш выбор - −3.99736930262764+4.76115037493966i (=Z) => 1) 4.76115037493966'+
                    '\nz = znachs[1]'+
                    '\nU, V = symbols("U V")'+
                    '\nx = Matrix([1, U, V])'+
                    '\nx = A * x - z * x'+
                    '\nsolve((x[0], x[1]), (U, V))'+
                    '\n# вывод: {U:0.0309239709647818−1.95695215731744i, V:−0.777977761106676+1.25179162406817i} 2) 0.0309239709647818'],
                 4: ['Для многочлена (x) = x1 2x13 2x12 - 2x11 2x -x - 2x - x 2x - x3 - 2x2 - x 2 найдите все его 14 корней: z1, …, z14 € С. В ответе укажите: 1) сумму модулей |z1| + …+ |z14|; 2) действительную часть корня, у которого эта действительная часть максимальна.', 
                    '\nx = symbols("x", dtype = complex)'+
                    '\nf = x ** 14 + 2 * x ** 13 + 2 * x ** 12 - 2 * x ** 11 + 2 * x ** 9 - x ** 8 - 2 * x ** 7 + x ** 6 + 2 * x ** 5 - x ** 3 - 2 * x ** 2 - x + 2'+
                    '\nroo = nroots(f)'+
                    '\nsum(map(abs, roo)), max(map(re, roo)) # (15.242608647068, 0.813384084227709)'],
                 5: ['Пусть lambda - комплексный корень из 1 степени 5, такой, что его мнимая часть больше 0, а действительная часть максимальна среди подобных корней с положительной мнимой частью. Даны матрицы: I = eye(2), A = (9 8, 5 5). Найдите определитель матрицы А - lambda*I и укажите в ответе: 1) действительную часть этого определитля; 2) его мнимую часть.', 
                    '\n# корни'+
                    '\nroots5 = solve(x ** 5 - 1)'+
                    '\nfor elem in roots5:'+
                    '\n  if re(elem) > re(mx) and im(elem) > 0:'+
                    '\n    mx = elem'+
                    '\nmx # (0.30901699437494745+0.9510565162951535j)'+
                    '\nA = Matrix([[9, 8], [5, 5]])'+
                    '\ndet(A + mx*eye(2))'],
                 
                 }
        if number == -1:
            numbers = []
            for i, j in sklad.items():
                if search in j[0]:
                    numbers.append(i)
            return 'есть в этих номерах: ', numbers
        print(sklad[number][0])
        print(sklad[number][1])


class q5:
    def pictures(number, search=-1):
        sklad = {1: ['Матрица A = (ai,j ) имеет размер n × n, где n = 80000. Известно, что ее диагональные элементы образуют арифметическую прогрессию с начальным элементом a1,1 = 0,99 и конечным элементом an,n = 1,01. Также известно, что все элементы матрицы A, расположенные вне главной диагонали, равны нулю за исключением двух элементов: a1,2 = 0,57 и a2,1 = 0,03. Найдите: 1) определитель матрицы A; 2) след матрицы, обратной к A.',
                    '\nn = 80000'+
                    '\nan = 1.01'+
                    '\na1 = 0.99'+
                    '\nd = (an - a1) / (n - 1)'+
                    '\nprogression = [a1 + d * i for i in range(n)]'+
                    '\na12 = 0.57; a21 = 0.03'+
                    '\nded = 1'+
                    '\nfor i in progression[2:]:'+
                    '\n\tded *= i'+
                    '\nans1 = ded * (progression[0] * progression[1] - a12*a21)'+
                    '\nans2 = progression[1]/(progression[0]*progression[1] - a12*a21) + progression[0]/(progression[0]*progression[1] - a12*a21) + sum(map(lambda x: x ** -1, progression[2:]))'+
                    '\nans1, ans2' ],
                 2: ['Матрица A = (ai,j ) имеет размер n × n, где n = 43000. Известно, что: 1) диагональные элементы образуют геометрическую прогрессию с начальным элементом a1,1 = 1 и конечным элементом an,n = 1,07; 2) элементы первой строки образуют арифметическую прогрессию с конечным элементом a1,n = 1,10; 3) все элементы матрицы A, расположенные вне главной диагонали и вне первой строки, равны нулю. Найдите обратную матрицу B = A−1 и укажите в ответе: 1) наименьший элемент матрицы B; 2) сумму элементов матрицы B.',
                 '\na11 = 1; ann = 1.07; a1n = 1.1; n = 43000'+
                 '\nda = (a1n - a11)/(n - 1)'+
                 '\naprog = [a11 + da * i for i in range(n)]'+
                 '\ndg = (ann / a11) ** (1 /(n - 1))'+
                 '\ndprog = [a11 * dg ** i for i in range(n)]'+
                 '\naprogB = [aprog[0] ** -1] + list(map(lambda x: -x/(aprog[0]*dprog[aprog.index(x)]), aprog[1:]))'+
                 '\ndprogB = list(map(lambda x: x ** -1, dprog))'+
                 '\nmin(dprogB + aprogB), sum(dprogB + aprogB[1:])' ],
                 3: ['Даны матрицы: I = (1 0 0 1), A = (7γ 14γ 9γ 1γ), где γ = 0,057. Пусть СУММА (n i=m) A^i, Bm = (I − A)^−1*A^m. 1) Найдите наибольший элемент матрицы S = S4,70. 2) Найдите наибольший элемент матрицы B = B4. 3) Найдите наименьшее k, такое, что при любом n > k наибольший элемент матрицы Sk,n меньше 0,0002.',
                 '\ng = 0.057'+
                 '\nA = Matrix([[7*g, 14*g], [9*g, g]])'+
                 '\ndef s(m, n, A):'+
                 '\n\tmatrixs =  [A ** i for i in range(m, n)]'+
                 '\n\tsu = zeros(2)'+
                 '\n\tfor i in matrixs:'+
                 '\n\t\tsu += i'+
                 '\n\treturn su'+
                 '\nsumma = s(4, 70, A)'+
                 '\nprint(max(summa))'+
                 '\nB = (eye(2) - A) ** -1 * A ** 4'+
                 '\nprint(max(B))'+
                 '\nfor k in range(100):'+
                 '\n\tif all(max(s(k, n, A)) < 0.0002 for n in range(k + 1, k + 100)):'+
                 '\n\t\tprint(k)'+
                 '\n\t\tbreak']

                 
                 
                 }
        if number == -1:
            numbers = []
            for i, j in sklad.items():
                if search in j[0]:
                    numbers.append(i)
            return 'есть в этих номерах: ', numbers
        print(sklad[number][0])
        print(sklad[number][1])
        
