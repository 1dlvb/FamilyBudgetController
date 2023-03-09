# FamilyBudgetController
** Приложение для контроля семейного бюджета | Application for family budget control **
Приложение написано на Python eel, JS, CSS, HTML.

* `get_num_of_rows` отвечает за вывод строк в базе данных.
* `get_incomes_from_db` отвечает за получение всех доходов из базы за выбраный месяц.
* `does_the_match_month` проверяет совпадает ли выбранная дата с текущей.
* `incomes_py` отправляет в JS выбранный тэг, размер дохода и дату.
* `expenses_py` отправляет в JS выбранный тэг, размер траты и дату.
* `debts_py` отправляет в JS имя дающего взаймы, размер займа и дату.
* `show_monthly_data_py` отправляет в JS данные за текущий месяц: `month_profit`, `month_expenses`, `month_rest`, `month_debt`.
* `get_and_show_selected_month_data_py` получает данные из JS и добавляет в базу данных по выбранному ключу.
* `show_selected_month_incomes_py` отправляет данные по доходам за текущий месяц в JS.
* `show_selected_month_expenses_py` отправляет данные по расходам за текущий месяц в JS.
* `show_selected_month_debts_py` отправляет данные по займам за текущий месяц в JS.
