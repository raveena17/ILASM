
function addElement(element, type, Id, name)
{
    var element = document.createElement(element);
    element.setAttribute("type", type);
    element.setAttribute("Id", Id);
    element.setAttribute("name", name)
    return element
}

function createOption(value, text)
{
option = document.createElement('option');
option.text = text;
option.value = value;
return option
}

function addRow(rowId, noOfColumns)
{
var newRow = document.createElement('tr')
newRow.id = rowId
for(column = 1; column<=noOfColumns; column++)
{
    tdnew = document.createElement('td');
    tdnew.id = (rowId+"col"+column);
    tdnew.name = 'col'+column;
    newRow.appendChild(tdnew);
}
return newRow
}

function createStageElement()
{
    noOfColumns = 2;
    var Table = document.getElementById('stageTable');
    var FormNoElement = document.getElementById('id_milestone-TOTAL_FORMS');

    var formNo = parseInt(FormNoElement.value); 
    var beforeRow = document.getElementById('row'+formNo);
    newRow = addRow('row'+(formNo+1), noOfColumns);

    StageId = 'milestone-'+ formNo + '-id'
    StageId = addElement("input", "hidden", "id_"+StageId, StageId);
    newRow.childNodes[0].style.width = "60%"
    newRow.childNodes[0].appendChild(StageId);

    stageName = 'milestone-'+ formNo + '-name';
    nameOfStage = addElement("input", "text", "id_"+stageName, stageName);
    nameOfStage.setAttribute("maxlength", "120");
    newRow.childNodes[0].appendChild(nameOfStage);

    stagePercent = 'milestone-'+ formNo + '-percentage';
    percent = addElement("input", "text", "id_"+stagePercent, stagePercent);
    percent.setAttribute("maxlength", "10");
    newRow.childNodes[1].style.width = "20%"
    newRow.childNodes[1].appendChild(percent);

    //stageDEL = 'milestone-'+ formNo + '-DELETE'
    //DEL = addElement("input", "checkbox", "id_"+stageDEL, stageDEL);
    
    //newRow.childNodes[2].style.width = "10%"
    //newRow.childNodes[2].appendChild(DEL);
    newRow.style.width = "100%";

    Table.appendChild(newRow);
    FormNoElement.value = parseInt(formNo) + 1;
}
function createStageElementProject()
{
    noOfColumns = 2;
    var Table = document.getElementById('stageTable');
    var FormNoElement = document.getElementById('id_milestone-TOTAL_FORMS');

    var formNo = parseInt(FormNoElement.value); 
    var beforeRow = document.getElementById('row'+formNo);
    newRow = addRow('row'+(formNo+1), noOfColumns);

    StageId = 'milestone-'+ formNo + '-id'
    StageId = addElement("input", "hidden", "id_"+StageId, StageId);
    newRow.childNodes[0].style.width = "60%"
    newRow.childNodes[0].appendChild(StageId);

    stageName = 'milestone-'+ formNo + '-name';
    nameOfStage = addElement("input", "text", "id_"+stageName, stageName);
    nameOfStage.setAttribute("maxlength", "120");
    newRow.childNodes[0].appendChild(nameOfStage);

    stagePercent = 'milestone-'+ formNo + '-percentage';
    percent = addElement("input", "text", "id_"+stagePercent, stagePercent);
    percent.setAttribute("maxlength", "10");
    newRow.childNodes[1].style.width = "20%"
    newRow.childNodes[1].appendChild(percent);

    //stageDEL = 'milestone-'+ formNo + '-DELETE'
    //DEL = addElement("input", "checkbox", "id_"+stageDEL, stageDEL);
    
    //newRow.childNodes[2].style.width = "10%"
    //newRow.childNodes[2].appendChild(DEL);
    newRow.style.width = "100%";

    Table.appendChild(newRow);
    FormNoElement.value = parseInt(formNo) + 1;
}


function createSpecificDatesElement()
{
    noOfColumns = 3;
    var Table = document.getElementById('SpecificDatesTable');
    var FormNoElement = document.getElementById('id_specificdates-TOTAL_FORMS');

    var formNo = parseInt(FormNoElement.value); 
    var beforeRow = document.getElementById('rowsd'+formNo);
    newRow = addRow('rowsd'+(formNo+1), noOfColumns);

    specificdatesId = 'specificdates-'+ formNo + '-id';
    specificdatesId = addElement("input", "hidden", "id_"+ specificdatesId, specificdatesId);
    newRow.childNodes[0].style.width = "60%";
    newRow.childNodes[0].appendChild(specificdatesId);

    specificdatesDate = 'specificdates-'+ formNo + '-start_date';
    nameDate = addElement("input", "text", "id_"+specificdatesDate, specificdatesDate);
    nameDate.setAttribute("maxlength", "120");
    nameDate.setAttribute("class", "vDateField");
    newRow.childNodes[0].appendChild(nameDate);

    specificdatesPercent = 'specificdates-'+ formNo + '-percentage';
    percent = addElement("input", "text", "id_"+specificdatesPercent, specificdatesPercent);

    percent.setAttribute("maxlength", "10");
    newRow.childNodes[1].style.width = "20%"
    newRow.childNodes[1].appendChild(percent);

    //specificdatesDEL = 'specificdates-'+ formNo + '-DELETE'
    //DEL = addElement("input", "checkbox", "id_"+ specificdatesDEL, specificdatesDEL);
    
    //newRow.childNodes[2].style.width = "10%"
    //newRow.childNodes[2].appendChild(DEL);
    newRow.style.width = "100%";

    Table.appendChild(newRow);
    FormNoElement.value = parseInt(formNo) + 1;
    DateTimeShortcuts.addCalendar(nameDate);
}

function removeStageElement()
{
    var Table = document.getElementById('stageTable');
    var FormNoElement = document.getElementById('id_milestone-TOTAL_FORMS');
    var formNo = parseInt(FormNoElement.value); 
    var FormCount = document.getElementById('StageFormCount').value;
    var child = document.getElementById('row'+formNo);
    if (formNo > FormCount){
        Table.removeChild(child);
        FormNoElement.value = formNo - 1;
    }
}

function removeSpecificDatesElement()
{    
    var Table = document.getElementById('SpecificDatesTable');
    var FormNoElement = document.getElementById('id_specificdates-TOTAL_FORMS');
    var formNo = parseInt(FormNoElement.value); 
    var FormCount = document.getElementById('SpecificDatesFormCount').value;
    var node = document.getElementById('rowsd'+formNo);
    if (formNo > FormCount){
        Table.removeChild(node);
        FormNoElement.value = parseInt(formNo) - 1;
    }
    
}

function saveProject()
{
	action = "/project/initiation/";
	var formObj = document.getElementById("program");
	var newAttr = document.createAttribute("action");
	newAttr.nodeValue = action;	
	formObj.removeAttributeNode(formObj.getAttributeNode("action"));
	formObj.setAttributeNode(newAttr);
}

function setCancelFormAction(action){
var formObj = document.getElementById("program");
var newAttr = document.createAttribute("action");
newAttr.nodeValue = action;	
formObj.removeAttributeNode(formObj.getAttributeNode("action"));
formObj.setAttributeNode(newAttr);
}

function setNavigation(url, ElementId, SendingName, alertName, action){
    if(url.indexOf('?') >0){ var connector = '&';}else{ var connector = '?';}
    if (ElementId != ''){
        val = document.getElementById(ElementId).value;
    }
    else{
        val = ''
    }
    url = url + connector + SendingName + '=' + val+ '&from=Project';
    if (action == 'update' && val == '0')    {
        alert('please select ' + alertName + ' to Edit');
    }
    else{
        window.location.href = url;
    }
    }
    

 function setFormAction(action){    
var flg = false;
 dateClean('id_planned_start_date');
 dateClean('id_planned_end_date');
flg = true;
var formObj = document.getElementById("program");
var newAttr = document.createAttribute("action");
newAttr.nodeValue = action;	
formObj.removeAttributeNode(formObj.getAttributeNode("action"));
formObj.setAttributeNode(newAttr);
return true; 
}

function createListObjects(options)
{
if (options == 'UsersExternal')
{
    if(document.getElementById("id_externalUsers") != null)
	    availableList = document.getElementById("id_externalUsers");
    if(document.getElementById("id_selectedExternalTeam") != null)
	    selectedList = document.getElementById("id_selectedExternalTeam"); 
}	
else
    {
    if(document.getElementById("id_internalUsers") != null)
	    availableList = document.getElementById("id_internalUsers");
    if(document.getElementById("id_selectedInternalTeam") != null)
	    selectedList = document.getElementById("id_selectedInternalTeam");        
    }	
}


jQuery.fn.slugify = function(obj) {
    jQuery(this).data('origquery', this);
    jQuery(this).data('obj', jQuery(obj));
    jQuery(this).keyup(function() {
        var obj = jQuery(this).data('obj');
        var oquery = jQuery(this).data('origquery');
        var vals = [];
        jQuery(oquery).each(function (i) {
            vals[i] = (jQuery(this).val());
        });
        var slug = vals.join(' ').toLowerCase().replace(/\s+/g,'-').replace(/[^a-z0-9\-]/g,'');
        obj.val(slug);
    });
}

jQuery.fn.copy = function(obj) {
    jQuery(this).keyup(function() {
        jQuery(obj).val(jQuery(this).val());
    });
}

function changeFormat(dateValue)
{
    var dateDict = dateValue.split('-')
    if (dateDict.length == 3)
    {
        var month = dateDict[0];
        var dateVal = dateDict[1];
        var year = dateDict[2];
        if (year.length == 4  && month.length < 3 && month.length >0 && dateVal.length < 3 && month.length > 0)
        {
            return year + '-' + month + '-' + dateVal;
        }
    }
}

function internalApprovalBlock()
{
    if($('#id_approval_type_0').attr('checked')){
            $('div.approvalDetails').css('height', '50px');
            $('#id_external_approval_1').attr('checked', false);
            $('#approvalInfo').css('visibility', 'hidden');
            $('#clientDetails').css('visibility', 'hidden');
        }
}

function externalApprovalBlock()
{        
    if($('#id_approval_type_1').attr('checked')){                
            $('div.approvalDetails').css('height', '100px');
            $('#id_approval_type_0').attr('checked', false);
            $('#approvalInfo').css('visibility', 'visible');
            $('#clientDetails').css('visibility', 'visible');
        }
}

function changeFormsetDateFormat()
{    
    $('#id_timebased-0-start_date').val(changeFormat($('#id_timebased-0-start_date').val()));
    $('#id_timebased-0-end_date').val(changeFormat($('#id_timebased-0-end_date').val()));
    for(var each=0; each < parseFloat($('#id_specificdates-TOTAL_FORMS').val()); each++){
        $('#id_specificdates-'+each+'-start_date').val(changeFormat($('#id_specificdates-'+each+'-start_date').val()));
}
}

function getclients(){
//    var form = this;
//    var data = {}
//    getdata = $("#id_customer").val()    
//   $.getJSON("../getclients/?customer="+getdata, 
//	function(json){
//	document.getElementById('id_customer').options.length =0;
//		if (json.length > 0){
//			for (j =json.length-1 ;j >=0;j--)
//			{
//			 if ((/Firefox[\/\s](\d+\.\d+)/.test(navigator.userAgent))||(navigator.appName == "Microsoft Internet Explorer" )) {
//			   newLi = $('<option selected value='+json[j].id+'>'+json[j].name+'</option>');
//				$("#id_customer").prepend(newLi);
//			   }
//			  else {
//			    newLi = $('<option value='+json[j].id+'>'+json[j].name+'</option>');
//				$("#id_customer").prepend(newLi);
//			  }	  
//			}
//		$("#id_customer").prepend($('<option value="">---------</option>'));
//		}
//		else{
//			var newLi = $('<option value="">---------</option>');
//			$("#id_customer").prepend(newLi);
//			}
//	 }
//   );
 }

var closeOverlay = function(){
    $("a[rel]").each(function(){
        $(this).overlay({oneInstance: false, api: true}).close();
        });
}

$(document).ready(function(){    
    convertDate('id_approval_date');
    convertDate('id_planned_start_date');
    convertDate('id_planned_end_date');
    convertDate('id_timebased-0-start_date');
    convertDate('id_timebased-0-end_date');
    document.getElementById("id_name").focus();
    if($('#id_id').val() == ''){$('#id_active').attr('checked', true);}
    $('#planned_effort_days').val($('#id_planned_effort').val());
   
    $('input#id_name').slugify('input#id_short_name');
    $('#id_timebased-0-DELETE').css('visibility', 'hidden');
    $('#cancel_bttop').click(function(){ window.location.href = '/project/list/' });
    $('#cancel_bt').click(function(){ window.location.href = '/project/list/' });

    $('#id_timebased-0-start_date').attr('class','vDateField');
    $('#id_timebased-0-end_date').attr('class','vDateField');
    $('#id_timebased-0-invoice_terms').find('option[value="0"], option[value="1"], option[value="6"]').remove()

    $('#id_milestone-TOTAL_FORMS').val($('#StageFormCount').val());
    $('#id_specificdates-TOTAL_FORMS').val($('#SpecificDatesFormCount').val());
    $('#id_resource-TOTAL_FORMS').val($('#NonHumanResourceFormCount').val());

    $('#tabs').tabs();
    if ($('#id_specificdates-INITIAL_FORMS').val() > 0){$('#tabs').tabs('select', 2);}
    else if ($('#id_timebased-INITIAL_FORMS').val() > 0){ $('#tabs').tabs('select', 1);}
    else {$('#tabs').tabs('select', 0);}

    internalApprovalBlock(); externalApprovalBlock();
    $('#id_approval_type_0').click(function(){ internalApprovalBlock() });
    $('#id_approval_type_1').click(function(){ externalApprovalBlock() });    

    $("[id ^='SaveAndContinue']").click(function(){$('#redirectionUrl').val('/project/initiation/');});

    for(var each=0; each<parseFloat($('#id_specificdates-TOTAL_FORMS').val()); each++){
        $('#id_specificdates-'+each+'-start_date').attr('class', 'vDateField');
        convertDate('id_specificdates-'+each+'-start_date');

        };

    $("[id ^='Save']").click(function(){changeFormsetDateFormat() });

    $('#id_planned_effort_unit').change(
        function()
        {
        if( $('#id_planned_effort').val() != '' && $('#id_id').val() != '' )
        {
            if(($('#id_planned_effort_unit').val()) == 'DAYS' )
                {$('#id_planned_effort').val(($('#planned_effort_days').val()/1).toFixed(2));}
            else if(($('#id_planned_effort_unit').val()) == 'MONTHS')
                {$('#id_planned_effort').val(($('#planned_effort_days').val()/12).toFixed(2));}
            else if(($('#id_planned_effort_unit').val()) == 'YEARS')
                {$('#id_planned_effort').val(($('#planned_effort_days').val()/360).toFixed(2));}
        }
        });

    $('#DeleteAllMilestoneDetails').click(function(){
            if (window.confirm('Are you sure you want to delete all milestone?'))
            {
                for(var each=0; each<parseFloat($('#id_milestone-TOTAL_FORMS').val()); each++){
                    $('#id_milestone-'+each+'-DELETE').attr('checked', true);
            };
            $('#redirectionUrl').val('/project/update/?ids='+$('#id_id').val());
            changeFormsetDateFormat();
            $("form:first").submit();
            }
           });
    $('#DeleteAllTimeBasedDetails').click(function(){
        if (window.confirm('Are you sure you want to delete all time-based billing details ?'))
        {
            $('#id_timebased-0-DELETE').attr('checked', true);
            $('#redirectionUrl').val('/project/update/?ids='+$('#id_id').val());
            changeFormsetDateFormat();
            $("form:first").submit();
        }
        });
    
    $('#DeleteAllSpecificDatesDetails').click(function(){
            if (window.confirm('Are you sure you want to delete all specified dates details?'))
            {
                for(var each=0; each<parseFloat($('#id_specificdates-TOTAL_FORMS').val()); each++){
                    $('#id_specificdates-'+each+'-DELETE').attr('checked', true);
            };
            $('#redirectionUrl').val('/project/update/?ids='+$('#id_id').val());
            changeFormsetDateFormat();
            $("form:first").submit();
            }
           });
    
     $("select#id_customer").change(function () {
            getclients();
        })
    $("#id_approval_type_1").attr('checked', true);
    //pop up
     $("a[rel]").overlay({ 
         expose: 'transparent', 
         effect: 'apple', 
         onBeforeLoad: function() { 
         	var wrap = this.getContent().find(".contentWrap"); 
         	wrap.load(this.getTrigger().attr("href")); 
            },
         }); 
            
      $('input[id^="domain_add"]').overlay({ 
            autoOpen: false,
            expose: { color: '#333', loadSpeed: 200, opacity: 0.9 },
            closeOnClick: true 
            });
      $('input[id^="domain_add"]').click(function() {
            var element_id = $(this).attr('id');
            $('input#select_box_id').attr('value', $('#role' + $(this).attr('name')).find('select').attr('id'));
            });
      $('#id_apex_body_owner').val($('#logged_in_user').val());
	//});
       });
   $(window).load(function() {
    getclients(); 
    });
	  
	function saveProject() { 
	   if(!isBetweenDate(document.getElementById("id_planned_start_date").value, document.getElementById("id_planned_end_date").value)) {
       	 	alert ('Planned end date occurs before the planned start date');
    		document.getElementById('id_planned_end_date').focus();
    		return false;
     	}    
        else {
             document.program.action = '/project/initiation/';
             return true;
       	}
}
