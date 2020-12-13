var first_click = true;

function creditFormSubmit() {
	$('.overlay').show();
	$('.credit').remove();
	
	var get_data = {
		'principal': $('#id_principal').val().replace(/,/g, ""),
		'interest_rate': $('#id_interest_rate').val(),
		'nb_year': $('#id_nb_year').val(),
		'nb_payments_year': $('#id_nb_payments_year').val(),
		'grace_period_in_month': $('#id_grace_period_in_month').val(),
		'amortization_type': $('#id_amortization_type').val(),
		'tax_rate': $('#id_tax_rate').val()
	};
	
	$.ajax({
		method: 'GET',
		url: 'stream/',
		data: get_data
		})
	.done(function (data) {
		var get_url = ("?principal=" + get_data['principal'] + "&interest_rate'=" + get_data['interest_rate'] + "&nb_year=" + get_data['nb_year'] + "&nb_payments_year=" + get_data['nb_payments_year'] + "&grace_period_in_month=" + get_data['grace_period_in_month'] + "&amortization_type=" + get_data['amortization_type'] + "&tax_rate=" + get_data['tax_rate']);
		/* history.pushState(state, title [, url]) */
		window.history.pushState("object or string", "credit", "/" + get_url);

		var table_body = $('#tbody');
		var amortization_schedule = data.amortization_schedule;
		$.each(amortization_schedule, function (key, value) {
			var $tr = $("<tr>", {
				'class': 'credit',
				'style': 'display:none;'
			});
			var $td_period = $("<td>", {
				'text': value.period
			});
			var $td_principal_t0 = $("<td>", {
				'text': convertNumberToString(value.principal_t0)
			});
            var $td_principal_t1 = $("<td>", {
				'text': convertNumberToString(value.principal_t1)
			});
			var $td_pmt = $("<td>", {
				'text': convertNumberToString(value.pmt)
			});
			var $td_ppmt = $("<td>", {
				'text': convertNumberToString(value.ppmt)
			});
			var $td_ipmt = $("<td>", {
				'text': convertNumberToString(value.ipmt)
			});
			var $td_tpmt = $("<td>", {
				'text': convertNumberToString(value.tpmt)
			});
			$(table_body).append(($tr)
				.append(($td_period))
				.append(($td_principal_t0))
				.append(($td_principal_t1))
				.append(($td_pmt))
				.append(($td_ppmt))
				.append(($td_ipmt))
                .append(($td_tpmt))
			);

			$($tr).children().each(function () {
				if ($(this).text().indexOf("-") >= 0) {
					$(this).addClass("text-danger");
				};
			});
		});
		
		setTimeout(function () {
			$('.overlay').removeAttr('style');
			$('#thead').fadeIn(1000);
			$(".credit").fadeIn(1000);
		}, 3000);
	});
};

function buildTable(data) {
};

function convertNumberToString(number) {
	try {
		var x = number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
		return x;
	} catch (err) {
		console.log(err);
		return number;
	}
};