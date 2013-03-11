
$(document).ready(function(){
	
	// $('#loginBut').click(function(){
		// $.post('/login/',
		// {
			// username:$('#usernametxt').val(),
			// passwd:$('#passwdtxt').val()
		// }, function(response){
			// if (response['status']){
				// //window.location.href = '/mainview/';
				// $('#loginForm').append('<form action="/homeview/" method="post" style = "display:hidden;">' +
						// '<input type="hidden" name = "username"  value="' + $('#loginUsername').val() + '"/></form>');
				// $('#loginForm form').submit();
// 				
			// }else{
			    // alert(response['status']);
// 				
			// }	
		// });
	// });
	
	$('#searchBut').click(function(){
		var keyword = $('#searchtxt').val();
		var categoriesChecked = $('input:checkbox:checked');
		var query = [];
		$.each(categoriesChecked, function(index, value){
			query.push(value.value);
		});
		window.location.href = '/?search=' + keyword + '&cat=' + query;
	});

	$("ul.subnav").parent().append("<span></span>"); //Only shows drop down trigger when js is enabled (Adds empty span tag after ul.subnav*)
	// ul.topnav li span
	$("#searchtxt").click(function() { //When trigger is clicked...
		// alert('fuck');
		//Following events are applied to the subnav itself (moving subnav up and down)
		$(this).parent().find("ul.subnav").slideDown('fast').show(); //Drop down the subnav on click

		$(this).parent().hover(function() {
		}, function(){	
			$(this).parent().find("ul.subnav").slideUp('slow'); //When the mouse hovers out of the subnav, move it back up
		});
		return true;
		//Following events are applied to the trigger (Hover events for the trigger)
		}).hover(function() { 
			$(this).addClass("subhover"); //On hover over, add class "subhover"
		}, function(){	//On Hover Out
			$(this).removeClass("subhover"); //On hover out, remove class "subhover"
			$('.category').checked = false;
	});

});