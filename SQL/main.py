#  1.
#  Посчитайте, сколько компаний закрылось.

select count(*)
from company
where status = 'closed'


# 2.
# Отобразите количество привлечённых средств для новостных компаний США.
# Используйте данные из таблицы company.
# Отсортируйте таблицу по убыванию значений в поле funding_total .

select funding_total
from company
where category_code = 'news'
    and country_code='USA'
order by funding_total desc


# 3.
# Найдите общую сумму сделок по покупке одних компаний другими в долларах.
# Отберите сделки, которые осуществлялись только за наличные с 2011 по 2013 год включительно.

select sum(price_amount)
from acquisition
where acquired_at::date between '2011-01-01' and '2013-12-31'
and term_code = 'cash'


# 4.
# Отобразите имя, фамилию и названия аккаунтов людей в поле network_username,
# у которых названия аккаунтов начинаются на 'Silver'.

select first_name,
last_name,
twitter_username
from people
where twitter_username like 'Silver%'


# 5.
# Выведите на экран всю информацию о людях,
# у которых названия аккаунтов в поле network_username содержат подстроку
# 'money', а фамилия начинается на 'K'.

select *
from people
where twitter_username like '%money%'
and last_name like 'K%'


# 6.
# Для каждой страны отобразите общую сумму привлечённых инвестиций,
# которые получили компании, зарегистрированные в этой стране.
# Страну, в которой зарегистрирована компания, можно определить по коду страны.
# Отсортируйте данные по убыванию суммы.

select country_code,
sum(funding_total)
from company
group by country_code
order by sum(funding_total) desc


# 7.
# Составьте таблицу, в которую войдёт дата проведения раунда,
# а также минимальное и максимальное значения суммы инвестиций, привлечённых в эту дату.
# Оставьте в итоговой таблице только те записи,
# в которых минимальное значение суммы инвестиций не равно нулю и не равно максимальному значению.

select funded_at::date,
    min(raised_amount),
    max(raised_amount)
from funding_round
group by funded_at::date
having min(raised_amount) <> 0
    and min(raised_amount) <> max(raised_amount)


# 8.
# Создайте поле с категориями:
# Для фондов, которые инвестируют в 100 и более компаний, назначьте категорию high_activity.
# Для фондов, которые инвестируют в 20 и более компаний до 100, назначьте категорию middle_activity.
# Если количество инвестируемых компаний фонда не достигает 20, назначьте категорию low_activity.
# Отобразите все поля таблицы fund и новое поле с категориями.

select *,
CASE
WHEN invested_companies >= 100 THEN 'high_activity'
WHEN invested_companies >= 20 AND invested_companies < 100 THEN 'middle_activity'
WHEN invested_companies < 20 THEN 'low_activity'
END
FROM fund


# 9.
# Для каждой из категорий, назначенных в предыдущем задании,
# посчитайте округлённое до ближайшего целого числа среднее количество инвестиционных раундов,
# в которых фонд принимал участие.
# Выведите на экран категории и среднее число инвестиционных раундов.
# Отсортируйте таблицу по возрастанию среднего.

SELECT CASE
           WHEN invested_companies>=100 THEN 'high_activity'
           WHEN invested_companies>=20 THEN 'middle_activity'
           ELSE 'low_activity'
       END AS activity,
       ROUND(AVG(investment_rounds)) AS avg_r
FROM fund
GROUP BY activity
order by avg_r


# 10.
# Проанализируйте, в каких странах находятся фонды,
# которые чаще всего инвестируют в стартапы.
# Для каждой страны посчитайте минимальное,
# максимальное и среднее число компаний,
# в которые инвестировали фонды этой страны, основанные с 2010 по 2012 год включительно.
# Исключите страны с фондами, у которых минимальное число компаний, получивших инвестиции, равно нулю.
# Выгрузите десять самых активных стран-инвесторов:
# отсортируйте таблицу по среднему количеству компаний от большего к меньшему.
# Затем добавьте сортировку по коду страны в лексикографическом порядке.

select country_code,
min(invested_companies),
max(invested_companies),
avg(invested_companies)
from fund
where founded_at::date between '2010-01-01' and '2012-12-31'
group by country_code
having min(invested_companies) <> 0
order by avg(invested_companies) desc,
country_code asc
limit 10


# 11.
# Отобразите имя и фамилию всех сотрудников стартапов.
# Добавьте поле с названием учебного заведения, которое окончил сотрудник,
# если эта информация известна.

select first_name,
last_name,
instituition
from people as p
left join education as e on e.person_id =p.id


# 12.
# Для каждой компании найдите количество учебных заведений, которые окончили её сотрудники.
# Выведите название компании и число уникальных названий учебных заведений.
# Составьте топ-5 компаний по количеству университетов.

with uni as
(select *
from company as c left join people as p on p.company_id=c.id
left join education as e on e.person_id =p.id)
select uni.name, count(distinct uni.instituition) as cnt
from uni
group by uni.name
order by cnt desc
limit 5


# 13.
# Составьте список с уникальными названиями закрытых компаний,
# для которых первый раунд финансирования оказался последним.

select distinct c.name
from funding_round as fr
join company as c on fr.company_id=c.id
where c.status = 'closed'
and fr.is_first_round = 1
and fr.is_last_round = 1


# 14.
# Составьте список уникальных номеров сотрудников,
# которые работают в компаниях, отобранных в предыдущем задании.

with camp as
(select distinct c.id
from funding_round as fr
join company as c on fr.company_id=c.id
where c.status = 'closed'
and fr.is_first_round = 1
and fr.is_last_round = 1)
select distinct p.id
from people as p
inner join camp on camp.id=p.company_id


# 15.
# Составьте таблицу, куда войдут уникальные пары с номерами сотрудников из предыдущей задачи и учебным заведением,
# которое окончил сотрудник.

with camp as
(select distinct c.id
from funding_round as fr
join company as c on fr.company_id=c.id
where c.status = 'closed'
and fr.is_first_round = 1
and fr.is_last_round = 1)

select distinct p.id,
e.instituition
from people as p
inner join camp on camp.id=p.company_id
inner join education as e on p.id=e.person_id


# 16.
# Посчитайте количество учебных заведений для каждого сотрудника из предыдущего задания.
# При подсчёте учитывайте, что некоторые сотрудники могли окончить одно и то же заведение дважды.

with camp as
(select distinct c.id
from funding_round as fr
join company as c on fr.company_id=c.id
where c.status = 'closed'
and fr.is_first_round = 1
and fr.is_last_round = 1)

select distinct p.id,
    count(e.instituition)
from people as p
inner join camp on camp.id=p.company_id
inner join education as e on p.id=e.person_id
group by p.id


# 17.
# Дополните предыдущий запрос и выведите среднее число учебных заведений (всех, не только уникальных),
# которые окончили сотрудники разных компаний. Нужно вывести только одну запись, группировка здесь не понадобится.

with camp as

(select p.id,
count(e.instituition)
from people as p

left
join
education as e
on
p.id = e.person_id
where
p.company_id in

(select c.id
from company as c
inner join funding_round as fr on c.id = fr.company_id
and status ='closed'
and is_first_round = 1
and is_last_round = 1
group by c.id)
group
by
p.id
having
count(distinct
e.instituition) > 0)

select
avg(count)
from camp;


# 18.
# Напишите похожий запрос: выведите среднее число учебных заведений (всех, не только уникальных),
# которые окончили сотрудники Facebook*.
# *(сервис, запрещённый на территории РФ)

with camp as
    (select p.id,
    count(e.instituition)
    from education as e

    left
    join
    people as p
    on
    p.id = e.person_id
    where
    p.company_id in
    (select id
    from company
    where name = 'Facebook')

    group
    by
    p.id)

    select
    avg(count)
    FROM
    camp;


# 19.
# Составьте таблицу из полей:
# name_of_fund — название фонда;
# name_of_company — название компании;
# amount — сумма инвестиций, которую привлекла компания в раунде.
# В таблицу войдут данные о компаниях, в истории которых было больше шести важных этапов,
# а раунды финансирования проходили с 2012 по 2013 год включительно.

select f.name,
c.name,
fr.raised_amount
from investment as i
inner join company as c on c.id = i.company_id
inner join fund as f on i.fund_id = f.id
inner join funding_round as fr on fr.id = i.funding_round_id
where c.milestones > 6
and fr.funded_at between '2012-01-01' and '2013-12-31';


# 20.
# Выгрузите таблицу, в которой будут такие поля:
# название компании-покупателя;
# сумма сделки;
# название компании, которую купили;
# сумма инвестиций, вложенных в купленную компанию;
# доля, которая отображает, во сколько раз сумма покупки превысила сумму вложенных в компанию инвестиций,
# округлённая до ближайшего целого числа.
# Не учитывайте те сделки, в которых сумма покупки равна нулю.
# Если сумма инвестиций в компанию равна нулю, исключите такую компанию из таблицы.
# Отсортируйте таблицу по сумме сделки от большей к меньшей,
# а затем по названию купленной компании в лексикографическом порядке. Ограничьте таблицу первыми десятью записями.

with
s as
(select c.name as sell,
c.funding_total as investment,
a.id as id_s
from acquisition as a
left join company as c on a.acquired_company_id = c.id
where c.funding_total > 0),

b as
(select c.name as buy,
a.price_amount as price,
a.id as id_b
from acquisition as a
left join company as c on a.acquiring_company_id = c.id
where a.price_amount > 0)

select b.buy,
    b.price,
    s.sell,
    s.investment,
    ROUND(b.price / s.investment)
from s
inner join b on s.id_s = b.id_b
order by price desc, sell
limit 10


# 21.
# Выгрузите таблицу, в которую войдут названия компаний из категории social,
# получившие финансирование с 2010 по 2013 год включительно.
# Проверьте, что сумма инвестиций не равна нулю.
# Выведите также номер месяца, в котором проходил раунд финансирования.

select  c.name,
extract(month from fr.funded_at::date)
from company as c
left join funding_round as fr on c.id = fr.company_id
where c.category_code = 'social'
and fr.funded_at between '2010-01-01' and '2013-12-31'
and fr.raised_amount <> 0


# 22.
# Отберите данные по месяцам с 2010 по 2013 год, когда проходили инвестиционные раунды.
# Сгруппируйте данные по номеру месяца и получите таблицу, в которой будут поля:
# номер месяца, в котором проходили раунды;
# количество уникальных названий фондов из США, которые инвестировали в этом месяце;
# количество компаний, купленных за этот месяц;
# общая сумма сделок по покупкам в этом месяце.

with
first as
(select extract(month from fr.funded_at::date) as mnth_fir,
count(distinct f.id) as cnt_fir
from fund as f
inner join investment as i ON f.id = i.fund_id
inner join funding_round as fr ON i.funding_round_id = fr.id
where f.country_code = 'USA'
and fr.funded_at::date between '2010-01-01' and '2013-12-31'
group by mnth_fir),

second as
(select  extract(month from acquired_at::date) as mnth_ses,
count(acquired_company_id) as cnt_sec,
sum(price_amount) sum_sec
from acquisition
where acquired_at::date between '2010-01-01' and '2013-12-31'
group by mnth_ses)

select first.mnth_fir, first.cnt_fir, second.cnt_sec, second.sum_sec
from first
inner join second ON first.mnth_fir = second.mnth_ses;


# 23.
# Составьте сводную таблицу и выведите среднюю сумму инвестиций для стран,
# в которых есть стартапы, зарегистрированные в 2011, 2012 и 2013 годах.
# Данные за каждый год должны быть в отдельном поле.
# Отсортируйте таблицу по среднему значению инвестиций за 2011 год от большего к меньшему.

with first as
(select country_code, avg(funding_total) as first_total
from company
where founded_at::date between '2011-01-01' and '2011-12-31'
group by country_code),

second as
(select country_code, avg(funding_total) as second_total
from company
where founded_at::date between '2012-01-01' and '2012-12-31'
group by country_code),

third as
(select country_code, avg(funding_total) as third_total
from company
where founded_at::date between '2013-01-01' and '2013-12-31'
group by country_code)

SELECT first.country_code, first_total, second_total, third_total
FROM first
JOIN second ON first.country_code = second.country_code
JOIN third ON second.country_code = third.country_code
ORDER BY first_total DESC;