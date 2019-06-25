var standard = { 
    /* Default values and constants.
     * */
    'lookupURL':'lookup/', 'taskColor':'#EFEFEF', 'altTaskColor':'#E0E7EF',
    'altTimeColor':'#E0E7EF', 'taskMinHeight':'30', 'resizeHandles' : 's,se', 
    };
    standard.halfHour = (+standard.taskMinHeight); // + is for type conversion.
    standard.oneHour = standard.halfHour * 2;
    standard.delimiter = '|';
    standard.width = 492;
    standard.autoCompleteOptions = { minChars:2, dataType:'json', parse:parseAutoCompData, formatItem:displayTaskName, };
    standard.daysTaskLookUpURL = 'lookup/daywiseTasks/';
    standard.totalTimeSpent = 'total/timeSpent/';

var closeOverlay = function(){
    $("a[rel]").each(function(){
        $(this).overlay({oneInstance: false, api: true}).close();
        });
}

$(function() {
    /* Instead of $(document).ready(function()){});
     * First set of tasks to be performed once the DOM is loaded.
     * */
    var context = $('#content'); /*A context which can be used as a range for DOM traversals. */
    paintTaskBG();
    $('.time:odd', context).css('background', standard.altTimeColor);
    var resizeWidgets = $('div[id^="task"]', context);
    resizeWidgets.resizable(resizeParams);
    resizeWidgets.find('input')
        .autocomplete(standard.lookupURL, standard.autoCompleteOptions).result(doTaskCRUD)
            .droppable(dropParams);
    $('.ui-widget-content > a', context).click(onTaskDelete);
	//$('.ui-widget-content > input[type="checkbox"]', context).click(onRework);
    $('#datepicker').datepicker(
        {
            buttonImage: '/static/css/images/icon_calendar.gif',
            buttonImageOnly: true,
            showOn: 'both',
            defaultDate : getDefaultDate(), 
            onSelect: redirectPage, 
            maxDate:'+0d', 
            minDate:'-2w', 
    });
    setDaysTasks(context);
    getTotalTimeSpent();
    context.animate({ scrollTop: 570 }, 2000); /*Set scroll at 8:00 a.m.*/
    $('div#set_of_tasks').find('li').draggable({helper: 'clone'});
    //pop up
     $("a[rel]").overlay({ 
         expose: 'transparent', 
         effect: 'apple', 
         onBeforeLoad: function() { 
         	var wrap = this.getContent().find(".contentWrap"); 
         	wrap.load(this.getTrigger().attr("href")); 
            },
         }); 

});

function paintTaskBG(context) {
    /* Paint the background of the task entry screen.
     * Alternate task entry divs will have different backgrounds.
     * */
    $('.ui-widget-content', context)
        .filter(function(i){ return $(this).css('display') != 'none'; })
            .each(function(index){
                if (index % 2 == 0) { $(this).css('background', standard.taskColor); }
                else { $(this).css('background', standard.altTaskColor); }
    });
}

function parseAutoCompData(data) {
    /* Convert the raw data into a more meaningful representation.
     * */
    return $.map(data, function(row) {
        return { data : row, value : row.id, result : row.name };
    });
}

 function displayTaskName(task) {
    /* Returns name of task, which is displayed in the autocomplete dropdown.
     * */
    return task.project+ ' : '+ task.name ;
}

function doTaskCRUD(evnt, data) {
    /* Perform Create, Update and Delete actions on timesheet entries.
     * Appropriate action will be taken based on the values of the entry object.
     * If task in entry is left as undefined then the action is assumed to be a delete.
     * Based on the startTime in entry, the action may either be a create or an update. 
     * */
    var inputField = $(this);
    var time = inputField.parent().attr('id').replace('task', '');
    time = time.substr(0,2) + ':' + time.substr(2);
    var taskName = getTaskDescription( inputField.val() );
    var entry = {'task' : undefined, 'startTime' : undefined, 'timeSpent' : undefined,'is_rework' : undefined,'projname' : undefined};
    
    if (data != undefined && inputField.val() != '') {
        entry.task = data.id;
        inputField.attr('id', data.id);
    }
    else if (inputField.val() != '') {
        entry.task = inputField.attr('id'); 
    }
    day = getDefaultDate(); /* getMonth() is a number between 0 and 11. */
    entry.start_time = [ day.getFullYear(), day.getMonth() + 1, day.getDate() ].join('-') + ' ' + time;

    //[entry.time_spent, unused] = calculateTimeSpent( inputField.parent().height() );
    //fixed incorrect left hand side assignment
    
    calculated_timespent = calculateTimeSpent( inputField.parent().height() );
    entry.time_spent = calculated_timespent[0];
//    checkBox = inputField.parent().find('input[name="is_rework"]');
//    if (checkBox.attr('checked')) {
//        entry.is_rework = 1;
//    }
//    else {
//        entry.is_rework = 0;
//    }
    

    //unused = calculated_timespent[1]

// var onCRUDCompletion = function() {
//    		appendInInputField(inputField, entry.time_spent);
//    		getTotalTimeSpent();
//    }
// $.ajax({ type : 'POST', url : '.', data : entry, success : onCRUDCompletion });
   $.post(".", entry,function(data) {
	appendInInputField(inputField, entry.time_spent);
	getTotalTimeSpent();
	if(data == '"Exceeded"'){
		alert("The project has exceeded its alloted time");
	}
	});
}
function getTotalTimeSpent(){
    /* get the total time total spent for the day */
    date = $('input#date').val()
    $.getJSON(standard.totalTimeSpent + '?date=' + date, function(data){ 
       $('#total').html(data['total']);
    }); 
} 

function onTaskDelete(evnt) {
    /* Clear the value of the input field.
     * Resize the div to minimum alloted height.
     * Save the deleted task, by triggering the search event for the input field.
     * */
    var taskDiv = $(this).parent();
    var inputField = taskDiv.find('input');
    inputField.attr('value', '');
    taskDiv.css('height', standard.taskMinHeight + 'px');
    inputField.trigger('search'); //The event that gets triggered at end of auto completion.
    getTotalTimeSpent(); // This function has to be explicitly called. Temporary fix.
    //FIXME: The above function shouldn't have to called explicitly, trigger('search') should take care of it.
//    inputField.parent().find('input[name="is_rework"]').remove();
    evnt.preventDefault();
}
function onResizeStop(evnt, ui) {
    /* Calculate timespent on task.
     * Hide supposedly overlapped divs.
     * Repaint the background for timesheet entry divs.
     * Save the modified timespent value for the task, by triggering the search event for the input field.
     * Correct the height of the div with the error corrected value.
     * */
    var timespent, correctedHeight = 0;

    //[timespent, correctedHeight] = calculateTimeSpent(ui.size.height);
    //fixed incorrect left hand side  assignment error

    var calculated_timespent = calculateTimeSpent(ui.size.height);
    timespent = calculated_timespent[0]
    correctedHeight = calculated_timespent[1]

    var noOfRows = correctedHeight / standard.halfHour;
    //$(this) refers to the div.
    toggleTaskVisibility($(this), ui.originalSize.height, correctedHeight);

    paintTaskBG();

    var inputField = $(this).find('input');
    inputField.trigger('search'); //The event that gets triggered at end of auto completion.

    $(this).css('height', correctedHeight).css('width', standard.width); //For resize error correction.
}

var resizeParams = { 
    /* See jquery-ui resizable documentation.*/
        stop: onResizeStop, handles: standard.resizeHandles,
    }; 
    resizeParams.minHeight = (+standard.taskMinHeight);
    resizeParams.minWidth = resizeParams.maxWidth = standard.width;
    resizeParams.grid = [0, (+standard.taskMinHeight)];
    resizeParams.distance = (+standard.taskMinHeight) / 2;

var dropParams = {
        accept: ".draggable_task",
        activeClass: 'ui-state-hover',
        hoverClass: 'ui-state-active',
        drop: function(ev, ui) {
            var dragged_task = $(ui.draggable); // The object being dragged.
            $(this).attr('id', dragged_task.attr('id'))
                    .attr('value', dragged_task.text())
                     .trigger('search'); //The event that gets triggered at end of auto completion.
    } 
};

function calculateTimeSpent(height) {
    /* Calculate the timespent from the height of the resized task div.
     * Also provides a error corrected value of height.
     * */
    var correctedHeight = Math.round( height/standard.halfHour ) * standard.halfHour;
    return [ correctedHeight/standard.oneHour, correctedHeight ];
}

function calculateHeight(timespent) {
    /* Calculate the height in pixels of the task div for which the timespent is specified.
     * */
    return timespent * standard.oneHour;
}

function toggleTaskVisibility(element, originalHeight, newHeight) { //TODO: Work on logic.
    /* Hides divs, to bring illusion of overlapping.
     * */
    var noOfTasks = Math.abs( originalHeight - newHeight) / standard.halfHour;
    var taskDivs = [ element ];
    for (i = 0; i < noOfTasks; i++) {
       taskDivs.push( element.next() );
       element = element.next();
    }
    for (i = 0; i < noOfTasks; i++) {
        taskDivs.pop().toggle();
    }
}


function appendInInputField(inputField, timespent) {
    /* Appends the timespent text with the task name.
     * */
    var description = getTaskDescription(inputField.val());
    var message = standard.delimiter + ' Time spent : ' + timespent + ' hour(s)';
//    var checkbox = $('<input type="checkbox" />').attr('name', 'is_rework');
//    var checkbox = document.createElement("input"); 
//    checkbox.type = "checkbox";
//    checkbox.name = "is_rework";
//    checkbox.id = "chk"+ inputField[0].id;
    if (description != '') {
        inputField.val( description + message);
//       if (inputField.parent().find('input[name="is_rework"]').length < 1) {
//		var id=$('#'+inputField[0].id).attr('id');
//		inputField.after(checkbox);	
//       }
    }
}

function getTaskDescription(description) {
    /* Returns the task name alone, after stripping of any timespent suffix text.
     * */
    if(description.indexOf(standard.delimiter) > -1) { 
        return description.substring(0, description.indexOf(standard.delimiter));
    }
    return description;
}

function redirectPage(dateText, inst) {
    /* Redirect the URL. To load the tasks from a different date.
     * TODO: Replace the need for this, with ajax calls.
     * */
    window.location = '/timesheet?date=' + dateText;
}

function getDefaultDate() {
    /* Default date is the date which should be shown as selected in the calender.
     * This is specified from the web server by placing it in a hidden text field.
     * */
    var dateText = $('input#date').val();
    var today = new Date();
    if( dateText == undefined) {
        return today;
    }
    dateSplit = dateText.split('/');
    if(dateSplit.length < 3) {
        return today;
    }
    //[ month, day, year ] = dateSplit;
    //fixed incorrect left hand side assignment

    month = dateSplit[0]
    day = dateSplit[1]
    year = dateSplit[2]
    return new Date(year, month - 1, day);
}

function setDaysTasks(context) {var timespent, correctedHeight = 0;
    /* Pulls out task performed on a given day (using ajax) 
     * and writes them on to the input fields in the timesheet entry divs.
     * */
    var selDate = $('input#date').val();
    $.getJSON(standard.daysTaskLookUpURL + '?date=' + selDate, function(data) { 
        $.each(data, function(i, item) { 
            var div = $('#task' + item.start_time, context);
            var inputField = div.find('input[type="text"]');
	    if(item.projname == null){ 
		inputField.val("Non Project Task  : " + item.name);
	    }
	    else { 
            inputField.val(item.projname + "  : " + item.name);
	    }
            inputField.attr('id', item.id);
            element_height = calculateHeight(item.time_spent)
            div.css('height', element_height  + 'px');
            toggleTaskVisibility(div, standard.taskMinHeight, element_height)
            appendInInputField(inputField, item.time_spent);
//	    var checkBox = div.find('input[type="checkbox"]');
//	    checkBox.attr('checked', item.is_rework);
        });
    });
}
