# computer-graphics-python
### 1. Измерение времени выполнения алгоритмов

Для оценки временных характеристик реализации различных алгоритмов растеризации линии и окружности, предлагается использовать следующие начальные и конечные координаты. Для измерения времени работы(в милисекундах) использовал `measure_time`.

### Тесты

| Алгоритм         | Координаты (x1, y1, x2, y2) или (x1, y1, r) |
|------------------|---------------------------------------------|
| Пошаговая линия  | (0, 0, 1000, 1000)                          |
| Линия DDA        | (0, 0, 1000, 1000)                          |
| Линия Брезенхема | (0, 0, 1000, 1000)                          |
| Окружность       | (0, 0, 225)                                 |

 Данные значения представляют стандартные случаи, охватывающие диагональные и симметричные линии и окружность с длиной равной длине линий.

### Замеры времени для данных значений

1. **Пошаговая линия (Step-by-Step Line)**:`~2.94 мс`.
2. **Линия DDA (Digital Differential Analyzer)**:`~0.24 мс`.
3. **Алгоритм Брезенхема для линии**:`~0.21 мс`.
4. **Алгоритм Брезенхема для окружности**:`~0.15 мс`.

### 2. Для чего нужна привязка координат к дискретной сетке?

Во всех приведенных алгоритмах каждый пиксель или точка представляют собой дискретные координаты на двумерной сетке. Алгоритмы DDA и Брезенхема привязывают точки к ближайшим целочисленным координатам, чтобы отобразить линию или окружность на этой сетке.

1. **Привязка к сетке**: 
   1) **Алгоритм DDA** вычисляет координаты точки с использованием дробных значений на каждом шаге. Однако при добавлении точек они округляются до ближайших целых значений, чтобы сохранить их в пределах сетки пикселей. То же самое в пошаговом алгоритме.
   2) **Алгоритм Брезенхема** для линий использует целочисленное округление для каждого шага, что позволяет избегать вычислений с плавающей запятой и получать дискретные целочисленные координаты. За счет использования разностей между текущими и целевыми координатами алгоритм сохраняет направленность линии.
   3) **Алгоритм Брезенхема для окружности** использует целочисленные операции и симметрию окружности, чтобы отобразить пиксели по всей окружности с минимальным количеством вычислений. 

2. **Влияние дискретизации**:
   1) Каждый пиксель на экране связан с целыми числами, что соответствует координатам на графике. Дискретизация приводит к аппроксимации линий и окружностей, делая их похожими на лестницу.
   2) Округление точек при отрисовке обеспечивает соответствие каждому пикселю и упрощает отрисовку на экране.

### Заключение


1) **Пошаговая линия** имеет простую реализацию, но работает медленнее и менее эффективно при работе с пикселями, чем DDA или Брезенхем.
2) **DDA** выполняется быстрее, но использует дробные вычисления, что может быть менее оптимально для графических дисплеев с низким разрешением.
3) **Брезенхем** демонстрирует высокую эффективность, особенно для целочисленных вычислений, обеспечивая более быстрое выполнение на дискретной сетке.
4) **Брезенхем для окружности** довольно быстрый, так как строит окружность симметрично, вычисляя только одну восьмую окружности и отражая остальные точки.
