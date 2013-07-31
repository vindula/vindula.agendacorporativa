
function openDisplayForm(fcevent, event) {
      event.preventDefault();
      event.stopPropagation();

      var url = fcevent['url'],
      	  msg = fcevent['description'];

      var $dialogContent = jq("#event_edit_container");
      $dialogContent.empty();
      // $dialogContent.dialog( "destroy" );

      $dialogContent.append(msg);
      $dialogContent.dialog({
        width: 400,
        autoOpen: true,
        modal: true,
        title: fcevent['title'],
        buttons: {
        	Ok: function() {
        		$j( this ).dialog( "close" );
        	}
    	}
      });

};


$j(document).ready(function() {

	$j('#calendar').fullCalendar({
		header: {
			left: 'prev,next today',
			center: 'title',
			right: 'month,agendaWeek,agendaDay'
		},
		theme: true,
		buttonText: {
			today: 'Hoje',
	        month: 'Mês',
		    week: 'Semana',
		    day: 'Dia',
		},

	  	slotMinutes : 30,
	    firstDay : 1,
	    weekends : true,
	    firstHour : '1',
	    minTime : '0',
	    maxTime : '24',
	    monthNames: ["Janeiro","Fevereiro","Março","Abril","Maio","Junho","Julho","Agosto","Setembro","Outubro","Novembro","Dezembro",],
	    monthNamesShort: ["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez",],
	    dayNames: ["Domingo","Segunda","Terça","Quarta","Quinta","Sexta","Sábado",],
	    dayNamesShort: ["Dom","Seg","Ter","Qua","Qui","Sex","Sab",],
	    columnFormat: {
	    	month: 'ddd',
	    	week: 'ddd M/d',
	    	day: 'dddd M/d'
	    },

	    titleFormat: {
	    	month: 'MMMM yyyy',
	    	week: "MMM d[ yyyy]{ '-'[ MMM] d yyyy}",
	    	day: 'dddd, MMM d, yyyy'
	    },
	    axisFormat: "h(:mm)tt",
	    allDaySlot: true,
	    allDayText: "all-day",

		editable: false,
		ignoreTimezone: false,
		events: url_events,
		eventClick: function(fcevent, event) {
        	openDisplayForm(fcevent, event);
      	}

	});
	
});