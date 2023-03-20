let a = 1;

//now Date
let nowDate = new Date().toISOString().slice(0, 10);
let nowDate_ = new Date()
let nowYear = nowDate_.getFullYear();
let nowMonth = nowDate_.getMonth() + 1;
let nowDay = nowDate_.getDay();

function OpenIncomeWindow()
{
	document.getElementById("ExpenseWindow").style.display = "none";
	document.getElementById("DebtWindow").style.display = "none";
	document.getElementById("open-history-btn").style.display = 'none';

	if(a==1)
	{
		document.getElementById("IncomeWindow").style.display = "block";
		document.getElementById("open-history-btn").style.display = 'none';
		return a = 0;
	}
	else
	{
		document.getElementById("IncomeWindow").style.display = "none";
		document.getElementById("open-history-btn").style.display = 'inline-block';
		return a = 1;

	}

}


function OpenExpenseWindow()
{
	document.getElementById("IncomeWindow").style.display = "none";
	document.getElementById("DebtWindow").style.display = "none";
	document.getElementById("open-history-btn").style.display = 'none';

	if(a==1)
	{
		document.getElementById("ExpenseWindow").style.display = "block";
		document.getElementById("open-history-btn").style.display = 'none';

		return a = 0;
	}
	else
	{
		document.getElementById("ExpenseWindow").style.display = "none";
		document.getElementById("open-history-btn").style.display = 'inline-block';

		return a = 1;

	}

}




function OpenDebtsWindow()
{
	document.getElementById("IncomeWindow").style.display = "none";
	document.getElementById("ExpenseWindow").style.display = "none";
	document.getElementById("open-history-btn").style.display = 'none';

	if(a==1)
	{
		document.getElementById("DebtWindow").style.display = "block";
		document.getElementById("open-history-btn").style.display = 'none';

		return a = 0;
	}
	else
	{
		document.getElementById("DebtWindow").style.display = "none";
		document.getElementById("open-history-btn").style.display = 'inline-block';

		return a = 1;

	}

}

async function income(){
	//Received money
	let amg_js = document.querySelector("#amountOfMoneyGet").value;
	//date
	let date_js_inc = new Date(document.querySelector("#dateInc").value).toISOString().slice(0, 10);


	//tag variables
	let selInc = document.getElementById("inputTagSelectInc").selectedIndex;
	let optionsInc = document.getElementById("inputTagSelectInc").options;
	let tag_inc_js = optionsInc[selInc].text;

	if ((amg_js < 0.01) || (date_js_inc > nowDate)) {

		//show error
		document.getElementById(('alert-money-inc')).style.display = 'block';
		return false;
	}
	else
	{

		//hide error
		document.getElementById('alert-money-inc').style.display = "none";

		//incomes
		eel.incomes_py(tag_inc_js, amg_js, date_js_inc);


	}
}


function expense(){
	//spent money variable
	let ams_js = document.querySelector("#amountOfMoneySpent").value;
	//date
	let date_js_exp = new Date(document.querySelector("#dateExp").value).toISOString().slice(0, 10);




	//tag variables
	let selExp = document.getElementById('inputTagSelectExp').selectedIndex;
	let optionsExp = document.getElementById('inputTagSelectExp').options;
	let tag_exp_js = optionsExp[selExp].text;

	if ((ams_js < 0.01) ||(date_js_exp > nowDate)) {
		//show error
		document.getElementById('alert-money-exp').style.display = "block";
		return false;
	}
	else
	{

		//hide error
		document.getElementById('alert-money-exp').style.display = "none";

		eel.expenses_py(tag_exp_js, ams_js, date_js_exp);

	}
}





function debt(){
	//Received money
	let amount_of_debt_js = document.querySelector('#amount-of-debt').value;
	//date
	let date_js_debt = new Date(document.querySelector("#dateDebt").value).toISOString().slice(0, 10);

	//name variables
	let moneylenders_name_js = document.querySelector('#moneylenders-name').value;


	if ((amount_of_debt_js < 0.01)||(isEmpty(moneylenders_name_js)) || ((date_js_debt > nowDate) && (date_js_debt != null)) ){
		document.getElementById("alert-money-debt").style.display = 'block';
		return false;
	}
	else
	{

		//hide error
		document.getElementById("alert-money-debt").style.display = 'none';

		eel.debts_py(moneylenders_name_js, amount_of_debt_js, date_js_debt)



	}
}


function isEmpty(str){
	if (str.trim() == '')
	{
		return true;
	}
	else
	{
		return false;
	}
}



function clear_values_incomes(){
	document.getElementById('inputTagSelectInc').value = 'Salary';
	document.getElementById('amountOfMoneyGet').value = '';

}

function clear_values_expenses(){
	document.getElementById('inputTagSelectExp').value = 'Other';
	document.getElementById('amountOfMoneySpent').value = '';

}

function clear_values_debts(){
	document.getElementById('moneylenders-name').value = '';
	document.getElementById('amount-of-debt').value = '';

}





function OpenHistoryWindow()
{
	a = 0;
	document.getElementById("Incomes-open").style.display = "none";
	document.getElementById("Expenses-open").style.display = "none";
	document.getElementById("Debts-open").style.display = "none";
	document.getElementById("open-history-btn").style.display = 'none';
	document.getElementById("go-home-btn").style.display = 'block';
	document.getElementById("header").style.display = 'none';

	//history page
	document.getElementById("history").style.display = 'none';


	if(a==1)
	{
		document.getElementById("Incomes-open").style.display = "block";
		document.getElementById("Expenses-open").style.display = "block";
		document.getElementById("Debts-open").style.display = "block";
		document.getElementById("header").style.display = 'block';

		//history page
		document.getElementById("history").style.display = 'none';

		return a = 0;
	}
	else
	{
		document.getElementById("Incomes-open").style.display = "none";
		document.getElementById("Expenses-open").style.display = "none";
		document.getElementById("Debts-open").style.display = "none";
		document.getElementById("header").style.display = 'none';

		//history page
		document.getElementById("history").style.display = 'block';

		return a = 1;

	}

}

function CloseHistoryWindow()
{
	document.getElementById("Incomes-open").style.display = "inline-block";
	document.getElementById("Expenses-open").style.display = "inline-block";
	document.getElementById("Debts-open").style.display = "inline-block";
	document.getElementById("open-history-btn").style.display = 'inline-block';
	document.getElementById("go-home-btn").style.display = 'none';
	document.getElementById("header").style.display = 'block';


	//history page
	document.getElementById("history").style.display = 'none';


	if(a==1)
	{
		document.getElementById("Incomes-open").style.display = "inline-block";
		document.getElementById("Expenses-open").style.display = "inline-block";
		document.getElementById("Debts-open").style.display = "inline-block";
		document.getElementById("open-history-btn").style.display = 'inline-block';
		document.getElementById("header").style.display = 'block';

		//history page
		document.getElementById("history").style.display = 'none';



		return a = 0;
	}
	else
	{
		document.getElementById("Incomes-open").style.display = "none";
		document.getElementById("Expenses-open").style.display = "none";
		document.getElementById("Debts-open").style.display = "none";
		document.getElementById("open-history-btn").style.display = 'none';
		document.getElementById("header").style.display = 'none';

		//history page
		document.getElementById("history").style.display = 'block';


		return a = 1;

	}

}

function CloseLearnMoreWindow(){
	document.getElementById("go-home-btn").style.display = 'block';
	document.getElementById("go-back-btn").style.display = 'none';
	document.getElementById("history").style.display = 'block';
	document.querySelector("#learn-more-incomes").style.display = 'none';
	document.querySelector("#learn-more-expenses").style.display = 'none';
	document.querySelector("#learn-more-debts").style.display = 'none';




}

async function show_monthly_data(){
	let data = await eel.show_monthly_data_py()();
	let profit = data[0];
	let expenses = data[1];
	let rest = data[2];
	let debts = data[3];
	document.getElementById("show-total-month-profit").innerHTML = "Your incomes </br> this month: " + profit.toFixed(2) + " ₽";
	document.getElementById("show-total-mouth-expenses").innerHTML = "Your expenses </br> this month: " + expenses.toFixed(2) + " ₽";
	document.getElementById("show-total-mouth-debts").innerHTML = "Your debts </br> this month: " + debts.toFixed(2) + " ₽";
	if (rest.toFixed(2) < 0) {
		document.getElementById("show-month-rest-money").style.color="#800000";
	}
	else {
		document.getElementById("show-month-rest-money").style.color="#fff";

	}
	document.getElementById("show-month-rest-money").innerHTML = "The rest of the money this year: " + rest.toFixed(2) + " ₽";

}




function learn_more_incomes(){
	document.getElementById("history").style.display = 'none';
	document.getElementById("go-home-btn").style.display = 'none';
	document.getElementById("go-back-btn").style.display = 'block';

	document.querySelector("#learn-more-incomes").style.display = 'block';

}

function learn_more_expenses(){
	document.getElementById("history").style.display = 'none';
	document.getElementById("go-home-btn").style.display = 'none';
	document.getElementById("go-back-btn").style.display = 'block';

	document.querySelector("#learn-more-expenses").style.display = 'block';
}

function learn_more_debts(){
	document.getElementById("history").style.display = 'none';
	document.getElementById("go-home-btn").style.display = 'none';
	document.getElementById("go-back-btn").style.display = 'block';

	document.querySelector("#learn-more-debts").style.display = 'block';
}

function get_data_from_learn_more_inc(){
	document.getElementById("alert-learn-more-inc").style.display = 'none';
	let date = new Date(document.querySelector("#select-month-income").value);
	let year = date.getFullYear();
	let month = date.getMonth() + 1;
	if (month < 10) {

		month = '0' + month;
	}
	else{
		month = "" + month;
	}

	if ((year > nowYear) || (month < nowMonth && year > nowYear) ||
		(month > nowMonth && year >= nowYear))
	{

		document.getElementById("alert-learn-more-inc").style.display = 'block';
		document.getElementById("show-data-inc").style.display = 'none';


	}
	else {
		document.getElementById("show-data-inc").style.display = 'flex';
		eel.get_and_show_selected_month_data_py(month, year, "inc")
		document.getElementById("alert-learn-more-inc").style.display = 'none';

	}


}
function get_data_from_learn_more_exp(){
	document.getElementById("alert-learn-more-exp").style.display = 'none';
	let date = new Date(document.querySelector("#select-month-expense").value);
	let year = date.getFullYear();
	let month = date.getMonth() + 1;
	if (month < 10) {

		month = '0' + month;
	}
	else{
		month = "" + month;
	}

	if ((year > nowYear) || (month < nowMonth && year > nowYear) ||
		(month > nowMonth && year >= nowYear))
	{

		document.getElementById("alert-learn-more-exp").style.display = 'block';
		document.getElementById("show-data-exp").style.display = 'none';



	}
	else {
		document.getElementById("show-data-exp").style.display = 'flex';
		eel.get_and_show_selected_month_data_py(month, year, "exp");

		document.getElementById("alert-learn-more-exp").style.display = 'none';
	}
}

function get_data_from_learn_more_debt(){
	document.getElementById("alert-learn-more-debt").style.display = 'none';
	let date = new Date(document.querySelector("#select-month-debt").value);
	let year = date.getFullYear();
	let month = date.getMonth() + 1;
	if (month < 10) {

		month = '0' + month;
	}
	else{
		month = "" + month;
	}

	if ((year > nowYear) || (month < nowMonth && year > nowYear) ||
		(month > nowMonth && year >= nowYear))
	{

		document.getElementById("alert-learn-more-debt").style.display = 'block';
		document.getElementById("show-data-debt").style.display = 'none';



	}
	else {
		document.getElementById("show-data-debt").style.display = 'flex';
		eel.get_and_show_selected_month_data_py(month, year, "debt");

		document.getElementById("alert-learn-more-debt").style.display = 'none';
	}
}


async function show_selected_month_incomes(){
	//selected month profit
	let arr =  await eel.show_selected_month_incomes_py()();
	profit = arr[0];
	data = arr[1];
	document.getElementById("show-inc").innerHTML = "All income for the selected month: </br>" + profit.toFixed(2) + " ₽";

	let Salary_sum = 0;
	let Upfront_sum = 0;
	let Pay_debt_sum = 0;
	let Found_sum = 0;
	let Investment_sum = 0;
	i = 0
	let s_data = data.split(";");
	while (i < s_data.length) {
		let s_s_data = s_data[i].split(" ");

		if (s_s_data[0] === ''){
			if (s_s_data[1] === 'Salary'){
				Salary_sum += parseFloat(s_s_data[2]);
			}
			else if (s_s_data[1] === 'Upfront') {
				Upfront_sum += parseFloat(s_s_data[2]);
			}
			else if (s_s_data[1] === 'Pay') {
				Pay_debt_sum += parseFloat(s_s_data[3]);
			}
			else if (s_s_data[1] === 'Found') {
				Found_sum += parseFloat(s_s_data[2]);
			}
			if (s_s_data[1] === 'Investment') {
				Investment_sum += parseFloat(s_s_data[2]);
			}



		}else{
			if (s_s_data[0] === 'Salary'){
				Salary_sum += parseFloat(s_s_data[1]);
			}
			else if (s_s_data[0] === 'Upfront') {
				Upfront_sum += parseFloat(s_s_data[1]);
			}
			else if (s_s_data[0] === 'Pay') {
				Pay_debt_sum += parseFloat(s_s_data[2]);
			}
			else if (s_s_data[0] === 'Found') {
				Found_sum += parseFloat(s_s_data[1]);
			}
			if (s_s_data[0] === 'Investment') {
				Investment_sum += parseFloat(s_s_data[1]);
			}

		}

		i++;
	}
document.getElementById("Salary-tag").innerHTML = "Salary: " + Salary_sum.toFixed(2) + " ₽";
document.getElementById("Upfront-tag").innerHTML = "Upfront: " + Upfront_sum.toFixed(2) + " ₽";
document.getElementById("Pay-debts-tag").innerHTML = "Pay debt: " + Pay_debt_sum.toFixed(2) + " ₽";
document.getElementById("Found-tag").innerHTML = "Found: " + Found_sum.toFixed(2) + " ₽";
document.getElementById("Investment-inc-tag").innerHTML = "Investment: " + Investment_sum.toFixed(2) + " ₽";


}

async function show_selected_month_expenses(){
	//selected month cost
	let arr = await eel.show_selected_month_expenses_py()();
	console.log(arr)
	let cost = arr[0];
	let data = arr[1];
	document.getElementById("show-exp").innerHTML = "All expenses for the selected month: </br>" + cost.toFixed(2) + " ₽";
	let Other_sum = 0;
	let Credits_sum = 0;
	let Utility_bills_sum = 0;
	let Snacks_sum = 0;
	let Food_sum = 0;
	let Medical_sum = 0;
	let Investment_sum = 0;
	let Sport_sum = 0;


	i = 0
	let s_data = data.split(";");
	while (i < s_data.length) {
		let s_s_data = s_data[i].split(" ");
		if (s_s_data[0] === ''){
			if (s_s_data[1] === 'Other'){
				Other_sum += parseFloat(s_s_data[2]);
			}
			else if (s_s_data[1] === 'Credits') {
				Credits_sum += parseFloat(s_s_data[2]);
			}
			else if (s_s_data[1] === 'Utility'){
				Utility_bills_sum += parseFloat(s_s_data[3]);

			}
			else if (s_s_data[1] === 'Snacks'){
				Snacks_sum += parseFloat(s_s_data[2]);

			}
			else if (s_s_data[1] === 'Food'){
				Food_sum += parseFloat(s_s_data[2]);

			}
			else if (s_s_data[1] === 'Medical'){
				Medical_sum += parseFloat(s_s_data[2]);

			}
			else if (s_s_data[1] === 'Investment'){
				Investment_sum += parseFloat(s_s_data[2]);

			}

			else if (s_s_data[1] === 'Sport'){
				Sport_sum += parseFloat(s_s_data[2]);

			}
		}else{
			if (s_s_data[0] === 'Other'){
				Other_sum += parseFloat(s_s_data[1]);

			}
			else if (s_s_data[0] === 'Credits') {
				Credits_sum += parseFloat(s_s_data[1]);
			}
			else if (s_s_data[0] === 'Utility'){
				Utility_bills_sum += parseFloat(s_s_data[2]);

			}
			else if (s_s_data[0] === 'Snacks'){
				Snacks_sum += parseFloat(s_s_data[1]);

			}
			else if (s_s_data[0] === 'Food'){
				Food_sum += parseFloat(s_s_data[1]);

			}
			else if (s_s_data[0] === 'Medical'){
				Medical_sum += parseFloat(s_s_data[1]);

			}
			else if (s_s_data[0] === 'Investment'){
				Investment_sum += parseFloat(s_s_data[1]);

			}

			else if (s_s_data[0] === 'Sport'){
				Sport_sum += parseFloat(s_s_data[1]);

			}
		}
		
		i++;
	}

	document.getElementById("Other-tag").innerHTML = "Other: " + Other_sum.toFixed(2) + " ₽";
	document.getElementById("Credits-tag").innerHTML = "Credits: " + Credits_sum.toFixed(2) + " ₽";
	document.getElementById("Utility-bills-tag").innerHTML = "Utility bills: " + Utility_bills_sum.toFixed(2) + " ₽";
	document.getElementById("Snacks-tag").innerHTML = "Snacks: " + Snacks_sum.toFixed(2) + " ₽";
	document.getElementById("Food-tag").innerHTML = "Food: " + Food_sum.toFixed(2) + " ₽";
	document.getElementById("Medical-tag").innerHTML = "Medical: " + Medical_sum.toFixed(2) + " ₽";
	document.getElementById("Investment-exp-tag").innerHTML = "Investment: " + Investment_sum.toFixed(2) + " ₽";
	document.getElementById("Sport-tag").innerHTML = "Sport: " + Sport_sum.toFixed(2) + " ₽";



}

async function show_selected_month_debts(){

	//selected month debts
	let arr = await eel.show_selected_month_debts_py()();
	let list = document.getElementById('lenders-name');
	let counter = 0;
	document.getElementById('by-names').innerText = '';


	let total_debt = arr[0];
	let data = arr[1].split(";");
    document.getElementById("show-debt").innerHTML = "All debts for the selected month: </br>" + total_debt.toFixed(2) + " ₽";
    i = 0;
    while (i < data.length - 1) {
		s_data = data[i].split('|')
    	console.log(s_data);

		document.getElementById('by-names').innerHTML += `<p id="lenders-name">${s_data[0]}  ${s_data[1]} ₽</p>`;
		document.getElementById('by-names').innerHTML += `</br>`;
		i++;
	}
}