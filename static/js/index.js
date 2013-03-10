
$(document).ready(function(){
	$('#create_question_but').click(function() {
		 window.location.href = '/createpost';
	});
	
	$('#headers li').click(function(){
		
		$('#headers li').removeClass('active');
		$(this).addClass('active');
	});
	
});
