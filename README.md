# FamilyBudgetController
**Приложение для контроля семейного бюджета | Application for family budget control**
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




- `get_num_of_rows` is responsible for outputting rows in the database.
- `get_incomes_from_db` is responsible for receiving all income from the database for the selected month.
- `does_the_match_month` checks whether the selected date matches the current one.
- `incomes_py` sends the selected tag, the amount of income and the date to JS.
- `expenses_py` sends the selected tag, the amount of spending and the date to JS.
- `debts_py` sends to JS the name of the borrower, the amount of the loan and the date.
- `show_monthly_data_py` sends data for the current month to JS: `month_profit`, `month_expenses`, `month_last`, `month_debt`.
- `get_and_show_selected_month_data_py` gets data from JS and adds it to the database by the selected key.
- `show_selected_month_incomes_py` sends revenue data for the current month to JS.
- `show_selected_month_expenses_py` sends spending data for the current month to JS.
- `show_selected_month_debts_py` sends data on loans for the current month to JS.
