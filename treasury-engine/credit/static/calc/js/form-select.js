$(document).ready(function () {
	$('[data-toggle="tooltip"]').tooltip();
	$(".form-control").focusin(function () {
		var input_name = $(this).attr('name')
		var collapsible = $("div[name=" + input_name + "]");
		var expanded = $(collapsible).attr('class');
		if (expanded == "collapse") {
			$(collapsible).collapse('toggle');
		}
	});
	$(".form-control").focusout(function () {
		var input_name = $(this).attr('name')
		var collapsible = $("div[name=" + input_name + "]");
		var expanded = $(collapsible).attr('class');
		if (expanded == "collapse show") {
			setTimeout(function () {
				$(collapsible).collapse('toggle');
			}, 100);

		};
	});

});

/* form submit action */
$("#creditForm").validate({
	submitHandler: function(form) {
		creditFormSubmit()
	},
	ignore: false,
	invalidHandler: function (e, validator) {
		// loop through the errors:
		for (var i = 0; i < validator.errorList.length; i++) {
			// "uncollapse" section containing invalid input/s:
			$(validator.errorList[i].element).closest('.collapse').collapse('show');
		}
	},
	errorElement: "div",
	errorPlacement: function (error, element) {
		// Add the `invalid-feedback` class to the error element
		error.addClass("invalid-feedback");

		//if (element.prop("type") === "checkbox") {
		//	error.insertAfter(element.parent("label"));
		//} else {
		//Some inputs have an append div after -- check if that exists
		//If so, slot the error after the div.  Else put it after the input
		if (element.siblings(".input-group-append").length > 0) {
			var $targetdiv = element.siblings(".input-group-append")
			error.insertAfter($targetdiv);
		} else {
			error.insertAfter(element);
		}

		//}
	},
	/*
	highlight: function (element, errorClass, validClass) {
		$(element).parents(".col-md-7").addClass("invalid-feedback").removeClass("valid-feedback");
	},
	unhighlight: function (element, errorClass, validClass) {
		$(element).parents(".col-md-7").addClass("valid-feedback").removeClass("invalid-feedback");
	}*/
});

/* tag action */
$("#id_principal").keyup(function (event) {

	// skip for arrow keys
	if (event.which >= 37 && event.which <= 40) return;

	// block any non-number
	if ((event.shiftKey || (event.keyCode < 48 || event.keyCode > 57)) && (event.keyCode < 96 || event.keyCode > 105)) {
		event.preventDefault();
	}

	// format number
	$(this).val(function (index, value) {
		return value
			.replace(/\D/g, "")
			.replace(/\B(?=(\d{3})+(?!\d))/g, ",");
	});
});

/* reset action */
$("#reset_defaults").click(function () {
	var principal_default = 100000000;
	var interest_rate_default = 8.5;
	var nb_year_default = 5;
	var nb_payments_year_default = 1;
	var grace_period_in_month_default = 0;
	var amortization_type_default = 1;
    var tax_rate_default = 18.90;

	$("#id_principal").val(principal_default);
	$("#id_interest_rate").val(interest_rate_default);
	$("#id_nb_year").val(nb_year_default);
	$("#id_nb_payments_year").val(nb_payments_year_default);
	$("#id_grace_period_in_month").val(grace_period_in_month_default);
    $("#id_amortization_type").val(amortization_type_default);
    $("#id_tax_rate").val(tax_rate_default);
});