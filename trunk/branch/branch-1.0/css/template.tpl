<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="de">
<head>
<title><§title></title>
<meta http-equiv="content-type" content="text/html; charset=utf-8" />
<link href="./css/style.css" rel="stylesheet" type="text/css" media="screen" />
<link href="./css/print.css" rel="stylesheet" type="text/css" media="print" />
<link rel="shortcut icon" href="./css/img/favicon.ico" type="image/x-icon" />
<script type="text/javascript" src="./jscripts/tiny_mce/tiny_mce.js"></script>
<script src="./jscripts/prototype.js" type="text/javascript"></script>
<script src="./jscripts/scriptaculous.js" type="text/javascript"></script>
<script type="text/javascript">
	function flupp() {
		Effect.DropOut('opt');
	}
	function change(id) {
		pre = 'note-' + id + '-pre';
		full = 'note-' + id + '-full';
		if (document.getElementById(full).style.display == 'none') {
			$(pre).fade();
			$(full).appear();
		} else {
			$(full).fade();
			$(pre).appear();
		}
	}
	tinyMCE.init({
		// General options
		mode : "textareas",
		theme : "advanced",
		theme_advanced_buttons1 : "bold,italic,underline,|,bullist,numlist,|,undo,redo",
		theme_advanced_buttons2 : "",
		theme_advanced_buttons3 : "",
		theme_advanced_buttons4 : "",
		// Example content CSS (should be your site CSS)
		content_css : "css/content.css",
	});
</script>
</head>
<body name="oben" id="oben">
<div id="menue">
<§menue>
</div>
<div id="output">
<div id="opt"><§options> <§bar></div>
<§content>
</div>
</body>
</html>
