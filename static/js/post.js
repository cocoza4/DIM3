
$(document).ready(function(){
	$('.callbacks').colorbox({rel:'callbacks', width:'75%', height:'75%'});
	$('#comment').click(function(){
		$.colorbox({
				width : '600',
				height : '400',
				href: $('#comment_dlg'),
				inline : true
			});
	});
	
	$('#commentBut').click(function(){
		if ($('#text').val() != '')
			$('#commentForm').submit();
		else
			alert('Please add your comment!');
	});
	
});
