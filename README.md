# Модель города Пермь

Данный репозиторий содержит исходный код и материалы для разработки модели города Пермь с использованием библиотеки CityGeoTools. Эта модель предназначена для анализа и визуализации географических данных о городе Пермь, а также для выполнения различных геоинформационных задач.

## Участники

Проект разрабатывается командой из четырех человек:

- Павел Смирнов
- Владислава Вядчинникова
- Илья Гаврилов
- Тимур Юлдашев

## Задание 3: Кластеризация

### Подготовка данных

- Слой со зданиями доступен по [ссылке](https://github.com/smpas/permProject/blob/master/data/buildings.geojson).
- Слой с кварталами доступен по [ссылке](https://github.com/smpas/permProject/blob/master/data/blocks.geojson).
- Слой с городскими сервисами доступен по [ссылке](https://github.com/smpas/permProject/blob/master/data/services.geojson).

### Загрузка слоев в модель города

- Пример кода с загрузкой слоев в модель города доступен в файле [main.py](https://github.com/smpas/permProject/blob/master/main.py).

### Кластеризация кварталов методом SpaceMatrix

- Метод кластеризации SpaceMatrix был применен к кварталам Индустриального района Перми для выявления структурных различий в застройке района.
- Код кластеризации доступен в файле [block_clusters.py](https://github.com/smpas/permProject/blob/master/clusters/code/block_clusters.py).
- Визуализация результатов выполнена при помощи библиотеки Folium и доступна в формате HTML-страницы.

![blocks](https://github.com/smpas/permProject/assets/55205785/be2f773e-e976-4425-8919-4ecbfb7fa656)


### Кластеризация городских сервисов и анализ

- Метод кластеризации городских сервисов был применен для выделения городских подцентров.
- Код кластеризации доступен в [директории](https://github.com/smpas/permProject/tree/master/clusters/code).
- Результаты визуализации в формате HTML-файлов доступны в [директории](https://github.com/smpas/permProject/tree/master/clusters/visualisation).

Общепит:
![изображение](https://github.com/smpas/permProject/assets/55205785/98c5c82b-e0d6-46cb-9da5-1b23c8ab65a9)
  
Здравоохранение:
![изображение](https://github.com/smpas/permProject/assets/55205785/f7b39619-83e1-4749-9384-bc44b8b0d2ee)

Развлечения:
![изображение](https://github.com/smpas/permProject/assets/55205785/5b4feb7a-e0cc-4ea7-b62c-5be92cb5f65f)

Образование:
![изображение](https://github.com/smpas/permProject/assets/55205785/273b0f70-dbca-4ad7-9b93-0d090b709460)

Продукты:
![изображение](https://github.com/smpas/permProject/assets/55205785/2bd3c90e-755c-4db8-9a97-f79d6668df4a)

### Анализ результатов
  Для всех типов сервисов характерна концентрация большинства кластеров на наиболее населенном левом берегу Камы. Наиболее распространенные сервисы - продуктовое снабжение, общепит и образование распределяются более-менее равномерно в соответствии с расселением горожан и формируют три крупных подцентра: исторический центр города и прилегающие территории, Закамск и Орджоникидзевский район. Интересно, что три этих подцентра расположены на значительном расстоянии друг от друга (15-20 км).
  
  Имеются отличия в структуре кластеров питания в разных частях города. Основу этих кластеров в историческом центре города формируют в основном кафе и рестораны, а вот в спальных и отдаленных районах города гораздо более высокую долю составляют заведения фастфуда и бары/пабы.

  Сервисы здравоохранения едва ли выходят за пределы исторического центра города и сконцентрированы именно в нем. Также в зависимости от удаления от исторического центра города меняется и структура кластеров здравоохранения: если в центре города значительную долю составляют больницы, то за пределами центра города они практически не встречаются.
  
  Похожим образом ситуация обстоит и с развлекательными сервисами, которые в основном сконцентрированы в центре города и почти не формируют кластеров за его пределами (за исклочением кластера в районе Гайва). В отдаленных частях города сервисы индустрии развлечения представлены единичными домами культуры.
