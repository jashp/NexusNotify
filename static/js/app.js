function emailValid(email) {
	var regex = /^([a-zA-Z0-9_\.\-\+])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
	return regex.test(email);
}
function subscribeValid() {
	var valid = true;
	var errorMsg = "";
	var lineBreak = "\n";

	if (!emailValid($("#register-form #email").val())) {
		valid = false;
		errorMsg = errorMsg + "Please enter a valid email address." + lineBreak;
	}
	
	if (!($('#versions-0').prop('checked') || $('#versions-1').prop('checked') || $('#versions-2').prop('checked'))) {
		valid = false;
		errorMsg = errorMsg + "You must select at least one device." + lineBreak;
	}
	

	if (!valid) {
		showAlert($("#info-error"), errorMsg);
		return false;
	} else {
		return true;
	}		
}		
function showAlert(alertBox, message) {
	$(".alert").hide();
	alertBox.text(message);
	alertBox.show();
}
$("#register-form").submit(function(event){
	event.preventDefault();
	if (!subscribeValid()) {
		return;
	}
	var $form = $(this);
	$inputs = $form.find("input, select, button, textarea");
	var serializedData = $form.serialize();
	$inputs.attr("disabled", "disabled");
	ajaxRequest = $.ajax({
		url: "add",
		type: "post",
		data: serializedData,
		success: function(response, textStatus, jqXHR){
			showAlert($("#info-success"), "It worked! We'll let you know when the Nexus 4 is back in stock.");
			$form.hide();
		},
		error: function(jqXHR, textStatus, errorThrown){
			showAlert($("#info-error"), "Something went wrong. Maybe you entered the captcha incorrectly?");
			$inputs.removeAttr("disabled");
		},
	});
});

function unsubscribeValid() {
	if (!emailValid($("#unsubscribe-form #email").val())) {
		showAlert($("#info-error-modal"), "Please enter a valid email address.");
		return false;
	} else {
		return true;
	}
}


$("#unsubscribe-submit").click(function(){
	$("#unsubscribe-form").submit();
});

$("#unsubscribe-cancel").click(function(){
	ajaxRequest.abort();
	$("#unsubscribe-form, #unsubscribe-submit").find("input, select, button, textarea").removeAttr("disabled");
});
$("#unsubscribe-form").submit(function(event){
	event.preventDefault();
	if (!unsubscribeValid()) {
		return;
	}
	$inputs = $("#unsubscribe-form, #unsubscribe-submit").find("input, select, button, textarea");
	var serializedData = $(this).serialize();
	$inputs.attr("disabled", "disabled");
	ajaxRequest = $.ajax({
		url: "/remove",
		type: "post",
		data: serializedData,
		success: function(response, textStatus, jqXHR){
			$('#unsubscribe-modal').modal('hide');
			showAlert($("#info-success"), "It worked! You've been unsubscribed.");
			$inputs.removeAttr("disabled");
			
		},
		error: function(jqXHR, textStatus, errorThrown){
			showAlert($("#info-error-modal"), jqXHR.responseText);
			$inputs.removeAttr("disabled");
		},
	});
});	
