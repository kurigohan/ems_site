//
//    Main script of DevOOPS v1.0 Bootstrap Theme
//
"use strict";
/*-------------------------------------------
	Dynamically load plugin scripts
---------------------------------------------*/
//
// Dynamically load Fullcalendar Plugin Script
// homepage: http://arshaw.com/fullcalendar
// require moment.js
//
function LoadCalendarScript(callback){
	function LoadFullCalendarScript(){
		if(!$.fn.fullCalendar){
			$.getScript('plugins/fullcalendar/fullcalendar.js', callback);
		}
		else {
			if (callback && typeof(callback) === "function") {
				callback();
			}
		}
	}
	if (!$.fn.moment){
		$.getScript('plugins/moment/moment.min.js', LoadFullCalendarScript);
	}
	else {
		LoadFullCalendarScript();
	}
}
//
// Dynamically load  OpenStreetMap Plugin
// homepage: http://openlayers.org
//
function LoadOpenLayersScript(callback){
	if (!$.fn.OpenLayers){
		$.getScript('http://www.openlayers.org/api/OpenLayers.js', callback);
	}
	else {
		if (callback && typeof(callback) === "function") {
			callback();
		}
	}
}
//
//  Dynamically load  jQuery Timepicker plugin
//  homepage: http://trentrichardson.com/examples/timepicker/
//
function LoadTimePickerScript(callback){
	if (!$.fn.timepicker){
		$.getScript('plugins/jquery-ui-timepicker-addon/jquery-ui-timepicker-addon.min.js', callback);
	}
	else {
		if (callback && typeof(callback) === "function") {
			callback();
		}
	}
}
//
//  Dynamically load Bootstrap Validator Plugin
//  homepage: https://github.com/nghuuphuoc/bootstrapvalidator
//
function LoadBootstrapValidatorScript(callback){
	if (!$.fn.bootstrapValidator){
		$.getScript('plugins/bootstrapvalidator/bootstrapValidator.min.js', callback);
	}
	else {
		if (callback && typeof(callback) === "function") {
			callback();
		}
	}
}
//
//  Dynamically load jQuery Select2 plugin
//  homepage: https://github.com/ivaynberg/select2  v3.4.5  license - GPL2
//
function LoadSelect2Script(callback){
	if (!$.fn.select2){
		$.getScript('plugins/select2/select2.min.js', callback);
	}
	else {
		if (callback && typeof(callback) === "function") {
			callback();
		}
	}
}
//
//  Dynamically load DataTables plugin
//  homepage: http://datatables.net v1.9.4 license - GPL or BSD
//
function LoadDataTablesScripts(callback){
	function LoadDatatables(){
		$.getScript('plugins/datatables/jquery.dataTables.js', function(){
			$.getScript('plugins/datatables/ZeroClipboard.js', function(){
				$.getScript('plugins/datatables/TableTools.js', function(){
					$.getScript('plugins/datatables/dataTables.bootstrap.js', callback);
				});
			});
		});
	}
	if (!$.fn.dataTables){
		LoadDatatables();
	}
	else {
		if (callback && typeof(callback) === "function") {
			callback();
		}
	}
}
//
//  Dynamically load Widen FineUploader
//  homepage: https://github.com/Widen/fine-uploader  v4.3.1 license - GPL3
//
function LoadFineUploader(callback){
	if (!$.fn.fineuploader){
		$.getScript('plugins/fineuploader/jquery.fineuploader-4.3.1.min.js', callback);
	}
	else {
		if (callback && typeof(callback) === "function") {
			callback();
		}
	}
}

//
//  Dynamically load Fancybox 2 plugin
//  homepage: http://fancyapps.com/fancybox/ v2.1.5 License - MIT
//
function LoadFancyboxScript(callback){
	if (!$.fn.fancybox){
		$.getScript('plugins/fancybox/jquery.fancybox.js', callback);
	}
	else {
		if (callback && typeof(callback) === "function") {
			callback();
		}
	}
}

/*-------------------------------------------
	Main scripts used by theme
---------------------------------------------*/
//
//  Function for load content from url and put in $('.ajax-content') block
//




function LoadAjaxContent(url){
	$('.preloader').show();
	$.ajax({
		mimeType: 'text/html; charset=utf-8', // ! Need set mimeType only when run from local file
		url: url,
		type: 'GET',
		success: function(data) {
			$('#ajax-content').html(data);
			$('.preloader').hide();
			// Activate any ajax link in the new ajax page
			AjaxContentLinks();
		},
		error: function (jqXHR, textStatus, errorThrown) {
			alert(errorThrown);
		},
		dataType: "html",
		async: false
	});
}


function AjaxContentLinks(){
	$('#ajax-content .ajax-link').click( function (e) {
		e.preventDefault();
		var url;
		if($(this).is('tr')){
			url = $(this).attr('data-href');
		}
		else{
			url = $(this).attr('href');
		}
		window.location.hash = url;
		LoadAjaxContent(url);
	});
}

//
//  Function maked all .box selector is draggable, to disable for concrete element add class .no-drop
//
function WinMove(){
	$( "div.box").not('.no-drop')
		.draggable({
			revert: true,
			zIndex: 2000,
			cursor: "crosshair",
			handle: '.box-name',
			opacity: 0.8
		})
		.droppable({
			tolerance: 'pointer',
			drop: function( event, ui ) {
				var draggable = ui.draggable;
				var droppable = $(this);
				var dragPos = draggable.position();
				var dropPos = droppable.position();
				draggable.swap(droppable);
				setTimeout(function() {
					var dropmap = droppable.find('[id^=map-]');
					var dragmap = draggable.find('[id^=map-]');
					if (dragmap.length > 0 || dropmap.length > 0){
						dragmap.resize();
						dropmap.resize();
					}
					else {
						draggable.resize();
						droppable.resize();
					}
				}, 50);
				setTimeout(function() {
					draggable.find('[id^=map-]').resize();
					droppable.find('[id^=map-]').resize();
				}, 250);
			}
		});
}
//
// Swap 2 elements on page. Used by WinMove function
//
jQuery.fn.swap = function(b){
	b = jQuery(b)[0];
	var a = this[0];
	var t = a.parentNode.insertBefore(document.createTextNode(''), a);
	b.parentNode.insertBefore(a, b);
	t.parentNode.insertBefore(b, t);
	t.parentNode.removeChild(t);
	return this;
};

//
//  Function for create 2 dates in human-readable format (with leading zero)
//
function PrettyDates(){
	var currDate = new Date();
	var year = currDate.getFullYear();
	var month = currDate.getMonth() + 1;
	var startmonth = 1;
	if (month > 3){
		startmonth = month -2;
	}
	if (startmonth <=9){
		startmonth = '0'+startmonth;
	}
	if (month <= 9) {
		month = '0'+month;
	}
	var day= currDate.getDate();
	if (day <= 9) {
		day = '0'+day;
	}
	var startdate = year +'-'+ startmonth +'-01';
	var enddate = year +'-'+ month +'-'+ day;
	return [startdate, enddate];
}
//
//  Function set min-height of window (required for this theme)
//
function SetMinBlockHeight(elem){
	elem.css('min-height', window.innerHeight - 49)
}
//
//  Helper for correct size of Messages page
//
function MessagesMenuWidth(){
	var W = window.innerWidth;
	var W_menu = $('#sidebar-left').outerWidth();
	var w_messages = (W-W_menu)*16.666666666666664/100;
	$('#messages-menu').width(w_messages);
}
//
// Function for change panels of Dashboard
//
function DashboardTabChecker(){
	$('#content').on('click', 'a.tab-link', function(e){
		e.preventDefault();
		$('div#dashboard_tabs').find('div[id^=dashboard]').each(function(){
			$(this).css('visibility', 'hidden').css('position', 'absolute');
		});
		var attr = $(this).attr('id');
		$('#'+'dashboard-'+attr).css('visibility', 'visible').css('position', 'relative');
		$(this).closest('.nav').find('li').removeClass('active');
		$(this).closest('li').addClass('active');
	});
}

//
//  Helper for open ModalBox with requested header, content and bottom
//
//
function OpenModalBox(header, inner, bottom){
	var modalbox = $('#modalbox');
	modalbox.find('.modal-header-name span').html(header);
	modalbox.find('.devoops-modal-inner').html(inner);
	modalbox.find('.devoops-modal-bottom').html(bottom);
	modalbox.fadeIn('fast');
	$('body').addClass("body-expanded");
}
//
//  Close modalbox
//
//
function CloseModalBox(){
	var modalbox = $('#modalbox');
	modalbox.fadeOut('fast', function(){
		modalbox.find('.modal-header-name span').children().remove();
		modalbox.find('.devoops-modal-inner').children().remove();
		modalbox.find('.devoops-modal-bottom').children().remove();
		$('body').removeClass("body-expanded");
	});
}
//
//  Beauty tables plugin (navigation in tables with inputs in cell)
//  Created by DevOOPS.
//
(function( $ ){
	$.fn.beautyTables = function() {
		var table = this;
		var string_fill = false;
		this.on('keydown', function(event) {
		var target = event.target;
		var tr = $(target).closest("tr");
		var col = $(target).closest("td");
		if (target.tagName.toUpperCase() == 'INPUT'){
			if (event.shiftKey === true){
				switch(event.keyCode) {
					case 37: // left arrow
						col.prev().children("input[type=text]").focus();
						break;
					case 39: // right arrow
						col.next().children("input[type=text]").focus();
						break;
					case 40: // down arrow
						if (string_fill==false){
							tr.next().find('td:eq('+col.index()+') input[type=text]').focus();
						}
						break;
					case 38: // up arrow
						if (string_fill==false){
							tr.prev().find('td:eq('+col.index()+') input[type=text]').focus();
						}
						break;
				}
			}
			if (event.ctrlKey === true){
				switch(event.keyCode) {
					case 37: // left arrow
						tr.find('td:eq(1)').find("input[type=text]").focus();
						break;
					case 39: // right arrow
						tr.find('td:last-child').find("input[type=text]").focus();
						break;
				case 40: // down arrow
					if (string_fill==false){
						table.find('tr:last-child td:eq('+col.index()+') input[type=text]').focus();
					}
					break;
				case 38: // up arrow
					if (string_fill==false){
						table.find('tr:eq(1) td:eq('+col.index()+') input[type=text]').focus();
					}
						break;
				}
			}
			if (event.keyCode == 13 || event.keyCode == 9 ) {
				event.preventDefault();
				col.next().find("input[type=text]").focus();
			}
			if (string_fill==false){
				if (event.keyCode == 34) {
					event.preventDefault();
					table.find('tr:last-child td:last-child').find("input[type=text]").focus();}
				if (event.keyCode == 33) {
					event.preventDefault();
					table.find('tr:eq(1) td:eq(1)').find("input[type=text]").focus();}
			}
		}
		});
		table.find("input[type=text]").each(function(){
			$(this).on('blur', function(event){
			var target = event.target;
			var col = $(target).parents("td");
			if(table.find("input[name=string-fill]").prop("checked")==true) {
				col.nextAll().find("input[type=text]").each(function() {
					$(this).val($(target).val());
				});
			}
		});
	})
};
})( jQuery );
//
// Beauty Hover Plugin (backlight row and col when cell in mouseover)
//
//
(function( $ ){
	$.fn.beautyHover = function() {
		var table = this;
		table.on('mouseover','td', function() {
			var idx = $(this).index();
			var rows = $(this).closest('table').find('tr');
			rows.each(function(){
				$(this).find('td:eq('+idx+')').addClass('beauty-hover');
			});
		})
		.on('mouseleave','td', function(e) {
			var idx = $(this).index();
			var rows = $(this).closest('table').find('tr');
			rows.each(function(){
				$(this).find('td:eq('+idx+')').removeClass('beauty-hover');
			});
		});
	};
})( jQuery );
//
//  Function convert values of inputs in table to JSON data
//
//
function Table2Json(table) {
	var result = {};
	table.find("tr").each(function () {
		var oneRow = [];
		var varname = $(this).index();
		$("td", this).each(function (index) { if (index != 0) {oneRow.push($("input", this).val());}});
		result[varname] = oneRow;
	});
	var result_json = JSON.stringify(result);
	OpenModalBox('Table to JSON values', result_json);
}

/*-------------------------------------------
	Scripts for DataTables page (tables_datatables.html)
---------------------------------------------*/
//
// Function for table, located in element with id = datatable-1
//
function TestTable1(){
	$('#datatable-1').dataTable( {
		"aaSorting": [[ 0, "asc" ]],
		"sDom": "<'box-content'<'col-sm-6'f><'col-sm-6 text-right'l><'clearfix'>>rt<'box-content'<'col-sm-6'i><'col-sm-6 text-right'p><'clearfix'>>",
		"sPaginationType": "bootstrap",
		"oLanguage": {
			"sSearch": "",
			"sLengthMenu": '_MENU_'
		}
	});
}
//
// Function for table, located in element with id = datatable-2
//
function TestTable2(){
	var asInitVals = [];
	var oTable = $('#datatable-2').dataTable( {
		"aaSorting": [[ 0, "asc" ]],
		"sDom": "<'box-content'<'col-sm-6'f><'col-sm-6 text-right'l><'clearfix'>>rt<'box-content'<'col-sm-6'i><'col-sm-6 text-right'p><'clearfix'>>",
		"sPaginationType": "bootstrap",
		"oLanguage": {
			"sSearch": "",
			"sLengthMenu": '_MENU_'
		},
		bAutoWidth: false
	});
	var header_inputs = $("#datatable-2 thead input");
	header_inputs.on('keyup', function(){
		/* Filter on the column (the index) of this element */
		oTable.fnFilter( this.value, header_inputs.index(this) );
	})
	.on('focus', function(){
		if ( this.className == "search_init" ){
			this.className = "";
			this.value = "";
		}
	})
	.on('blur', function (i) {
		if ( this.value == "" ){
			this.className = "search_init";
			this.value = asInitVals[header_inputs.index(this)];
		}
	});
	header_inputs.each( function (i) {
		asInitVals[i] = this.value;
	});
}
//
// Function for table, located in element with id = datatable-3
//
function TestTable3(){
	$('#datatable-3').dataTable( {
		"aaSorting": [[ 0, "asc" ]],
		"sDom": "T<'box-content'<'col-sm-6'f><'col-sm-6 text-right'l><'clearfix'>>rt<'box-content'<'col-sm-6'i><'col-sm-6 text-right'p><'clearfix'>>",
		"sPaginationType": "bootstrap",
		"oLanguage": {
			"sSearch": "",
			"sLengthMenu": '_MENU_'
		},
		"oTableTools": {
			"sSwfPath": "plugins/datatables/copy_csv_xls_pdf.swf",
			"aButtons": [
				"copy",
				"print",
				{
					"sExtends":    "collection",
					"sButtonText": 'Save <span class="caret" />',
					"aButtons":    [ "csv", "xls", "pdf" ]
				}
			]
		}
	});
}

/*-------------------------------------------
	Function for File upload page (form_file_uploader.html)
---------------------------------------------*/
function FileUpload(){
	$('#bootstrapped-fine-uploader').fineUploader({
		template: 'qq-template-bootstrap',
		classes: {
			success: 'alert alert-success',
			fail: 'alert alert-error'
		},
		thumbnails: {
			placeholders: {
				waitingPath: "assets/waiting-generic.png",
				notAvailablePath: "assets/not_available-generic.png"
			}
		},
		request: {
			endpoint: 'server/handleUploads'
		},
		validation: {
			allowedExtensions: ['jpeg', 'jpg', 'gif', 'png']
		}
	});
}

//
// Function for Dynamically Change input size on Form Layout page
//
function FormLayoutExampleInputLength(selector){
	var steps = [
		"col-sm-1",
		"col-sm-2",
		"col-sm-3",
		"col-sm-4",
		"col-sm-5",
		"col-sm-6",
		"col-sm-7",
		"col-sm-8",
		"col-sm-9",
		"col-sm-10",
		"col-sm-11",
		"col-sm-12"
	];
	selector.slider({
	   range: 'min',
		value: 1,
		min: 0,
		max: 11,
		step: 1,
		slide: function(event, ui) {
			if (ui.value < 1) {
				return false;
			}
			var input = $("#form-styles");
			var f = input.parent();
			f.removeClass();
			f.addClass(steps[ui.value]);
			input.attr("placeholder",'.'+steps[ui.value]);
		}
	});
}

/*-------------------------------------------
	Function for jQuery-UI page (ui_jquery-ui.html)
---------------------------------------------*/
//
// Function for make all Date-Time pickers on page
//
function AllTimePickers(){
	$('#datetime_example').datetimepicker({});
	$('#time_example').timepicker({
		hourGrid: 4,
		minuteGrid: 10,
		timeFormat: 'hh:mm tt'
	});
	$('#date3_example').datepicker({ numberOfMonths: 3, showButtonPanel: true});
	$('#date3-1_example').datepicker({ numberOfMonths: 3, showButtonPanel: true});
	$('#date_example').datepicker({});
}
/*-------------------------------------------
	Function for Calendar page (calendar.html)
---------------------------------------------*/
//
// Example form validator function
//
function DrawCalendar(){
	/* initialize the external events
	-----------------------------------------------------------------*/
	$('#external-events div.external-event').each(function() {
		// create an Event Object (http://arshaw.com/fullcalendar/docs/event_data/Event_Object/)
		var eventObject = {
			title: $.trim($(this).text()) // use the element's text as the event title
		};
		// store the Event Object in the DOM element so we can get to it later
		$(this).data('eventObject', eventObject);
		// make the event draggable using jQuery UI
		$(this).draggable({
			zIndex: 999,
			revert: true,      // will cause the event to go back to its
			revertDuration: 0  //  original position after the drag
		});
	});
	/* initialize the calendar
	-----------------------------------------------------------------*/
	var calendar = $('#calendar').fullCalendar({
		header: {
			left: 'prev,next today',
			center: 'title',
			right: 'month,agendaWeek,agendaDay'
		},
		selectable: true,
		selectHelper: true,
		select: function(start, end, allDay) {
			var form = $('<form id="event_form">'+
				'<div class="form-group has-success has-feedback">'+
				'<label">Event name</label>'+
				'<div>'+
				'<input type="text" id="newevent_name" class="form-control" placeholder="Name of event">'+
				'</div>'+
				'<label>Description</label>'+
				'<div>'+
				'<textarea rows="3" id="newevent_desc" class="form-control" placeholder="Description"></textarea>'+
				'</div>'+
				'</div>'+
				'</form>');
			var buttons = $('<button id="event_cancel" type="cancel" class="btn btn-default btn-label-left">'+
							'<span><i class="fa fa-clock-o txt-danger"></i></span>'+
							'Cancel'+
							'</button>'+
							'<button type="submit" id="event_submit" class="btn btn-primary btn-label-left pull-right">'+
							'<span><i class="fa fa-clock-o"></i></span>'+
							'Add'+
							'</button>');
			OpenModalBox('Add event', form, buttons);
			$('#event_cancel').on('click', function(){
				CloseModalBox();
			});
			$('#event_submit').on('click', function(){
				var new_event_name = $('#newevent_name').val();
				if (new_event_name != ''){
					calendar.fullCalendar('renderEvent',
						{
							title: new_event_name,
							description: $('#newevent_desc').val(),
							start: start,
							end: end,
							allDay: allDay
						},
						true // make the event "stick"
					);
				}
				CloseModalBox();
			});
			calendar.fullCalendar('unselect');
		},
		editable: true,
		droppable: true, // this allows things to be dropped onto the calendar !!!
		drop: function(date, allDay) { // this function is called when something is dropped
			// retrieve the dropped element's stored Event Object
			var originalEventObject = $(this).data('eventObject');
			// we need to copy it, so that multiple events don't have a reference to the same object
			var copiedEventObject = $.extend({}, originalEventObject);
			// assign it the date that was reported
			copiedEventObject.start = date;
			copiedEventObject.allDay = allDay;
			// render the event on the calendar
			// the last `true` argument determines if the event "sticks" (http://arshaw.com/fullcalendar/docs/event_rendering/renderEvent/)
			$('#calendar').fullCalendar('renderEvent', copiedEventObject, true);
			// is the "remove after drop" checkbox checked?
			if ($('#drop-remove').is(':checked')) {
				// if so, remove the element from the "Draggable Events" list
				$(this).remove();
			}
		},
		eventRender: function (event, element, icon) {
			if (event.description != "") {
				element.attr('title', event.description);
			}
		},
		eventClick: function(calEvent, jsEvent, view) {
			var form = $('<form id="event_form">'+
				'<div class="form-group has-success has-feedback">'+
				'<label">Event name</label>'+
				'<div>'+
				'<input type="text" id="newevent_name" value="'+ calEvent.title +'" class="form-control" placeholder="Name of event">'+
				'</div>'+
				'<label>Description</label>'+
				'<div>'+
				'<textarea rows="3" id="newevent_desc" class="form-control" placeholder="Description">'+ calEvent.description +'</textarea>'+
				'</div>'+
				'</div>'+
				'</form>');
			var buttons = $('<button id="event_cancel" type="cancel" class="btn btn-default btn-label-left">'+
							'<span><i class="fa fa-clock-o txt-danger"></i></span>'+
							'Cancel'+
							'</button>'+
							'<button id="event_delete" type="cancel" class="btn btn-danger btn-label-left">'+
							'<span><i class="fa fa-clock-o txt-danger"></i></span>'+
							'Delete'+
							'</button>'+
							'<button type="submit" id="event_change" class="btn btn-primary btn-label-left pull-right">'+
							'<span><i class="fa fa-clock-o"></i></span>'+
							'Save changes'+
							'</button>');
			OpenModalBox('Change event', form, buttons);
			$('#event_cancel').on('click', function(){
				CloseModalBox();
			});
			$('#event_delete').on('click', function(){
				calendar.fullCalendar('removeEvents' , function(ev){
					return (ev._id == calEvent._id);
				});
				CloseModalBox();
			});
			$('#event_change').on('click', function(){
				calEvent.title = $('#newevent_name').val();
				calEvent.description = $('#newevent_desc').val();
				calendar.fullCalendar('updateEvent', calEvent);
				CloseModalBox()
			});
		}
		});
		$('#new-event-add').on('click', function(event){
			event.preventDefault();
			var event_name = $('#new-event-title').val();
			var event_description = $('#new-event-desc').val();
			if (event_name != ''){
			var event_template = $('<div class="external-event" data-description="'+event_description+'">'+event_name+'</div>');
			$('#events-templates-header').after(event_template);
			var eventObject = {
				title: event_name,
				description: event_description
			};
			// store the Event Object in the DOM element so we can get to it later
			event_template.data('eventObject', eventObject);
			event_template.draggable({
				zIndex: 999,
				revert: true,
				revertDuration: 0
			});
			}
		});
}
//
// Load scripts and draw Calendar
//
function DrawFullCalendar(){
	LoadCalendarScript(DrawCalendar);
}
//////////////////////////////////////////////////////
//////////////////////////////////////////////////////
//
//      MAIN DOCUMENT READY SCRIPT OF DEVOOPS THEME
//
//      In this script main logic of theme
//
//////////////////////////////////////////////////////
//////////////////////////////////////////////////////
$(document).ready(function () {
	$('.show-sidebar').on('click', function () {
		$('div#main').toggleClass('sidebar-show');
		setTimeout(MessagesMenuWidth, 250);
	});
	var ajax_url = location.hash.replace(/^#/, '');
	if (ajax_url.length < 1) {
		ajax_url = "/home/";
	}
	LoadAjaxContent(ajax_url);
	$('.main-menu').on('click', 'a', function (e) {
		var parents = $(this).parents('li');
		var li = $(this).closest('li.dropdown');
		var another_items = $('.main-menu li').not(parents);
		another_items.find('a').removeClass('active');
		another_items.find('a').removeClass('active-parent');
		if ($(this).hasClass('dropdown-toggle') || $(this).closest('li').find('ul').length == 0) {
			$(this).addClass('active-parent');
			var current = $(this).next();
			if (current.is(':visible')) {
				li.find("ul.dropdown-menu").slideUp('fast');
				li.find("ul.dropdown-menu a").removeClass('active')
			}
			else {
				another_items.find("ul.dropdown-menu").slideUp('fast');
				current.slideDown('fast');
			}
		}
		else {
			if (li.find('a.dropdown-toggle').hasClass('active-parent')) {
				var pre = $(this).closest('ul.dropdown-menu');
				pre.find("li.dropdown").not($(this).closest('li')).find('ul.dropdown-menu').slideUp('fast');
			}
		}
		if ($(this).hasClass('active') == false) {
			$(this).parents("ul.dropdown-menu").find('a').removeClass('active');
			$(this).addClass('active')
		}
		if ($(this).hasClass('ajax-link')) {
			e.preventDefault();
			if ($(this).hasClass('add-full')) {
				$('#content').addClass('full-content');
			}
			else {
				$('#content').removeClass('full-content');
			}
			var url = $(this).attr('href');
			window.location.hash = url;
			LoadAjaxContent(url);
		}
		if ($(this).attr('href') == '#') {
			e.preventDefault();
		}
	});
	var height = window.innerHeight - 49;
	$('#main').css('min-height', height)
		.on('click', '.expand-link', function (e) {
			var body = $('body');
			e.preventDefault();
			var box = $(this).closest('div.box');
			var button = $(this).find('i');
			button.toggleClass('fa-expand').toggleClass('fa-compress');
			box.toggleClass('expanded');
			body.toggleClass('body-expanded');
			var timeout = 0;
			if (body.hasClass('body-expanded')) {
				timeout = 100;
			}
			setTimeout(function () {
				box.toggleClass('expanded-padding');
			}, timeout);
			setTimeout(function () {
				box.resize();
				box.find('[id^=map-]').resize();
			}, timeout + 50);
		})
		.on('click', '.collapse-link', function (e) {
			e.preventDefault();
			var box = $(this).closest('div.box');
			var button = $(this).find('i');
			var content = box.find('div.box-content');
			content.slideToggle('fast');
			button.toggleClass('fa-chevron-up').toggleClass('fa-chevron-down');
			setTimeout(function () {
				box.resize();
				box.find('[id^=map-]').resize();
			}, 50);
		})
		.on('click', '.close-link', function (e) {
			e.preventDefault();
			var content = $(this).closest('div.box');
			content.remove();
		});
	$('body').on('click', 'a.close-link', function(e){
		e.preventDefault();
		CloseModalBox();
	});
	$('#top-panel').on('click','a', function(e){
		if ($(this).hasClass('ajax-link')) {
			e.preventDefault();
			if ($(this).hasClass('add-full')) {
				$('#content').addClass('full-content');
			}
			else {
				$('#content').removeClass('full-content');
			}
			var url = $(this).attr('href');
			window.location.hash = url;
			LoadAjaxContent(url);
		}
	});

});


