
function addElement(element, type, Id, name)
{
    var element = document.createElement(element);
    element.setAttribute("type", type);
    element.setAttribute("Id", Id);
    element.setAttribute("name", name);
    // element.setAttribute("value", "dssdsdsds");
    return element
}


// function addElement(element, type, Id, name)
// {
//     var element = document.createElement(element);
//     element.setAttribute("type", type);
//     element.setAttribute("Id", Id);
//     element.setAttribute("name", name)
//     return element
// }

// function removeElement(element, type, Id, name)
// {
//     var element = document.removeElement(element);
//     element.setAttribute("type", type);
//     element.setAttribute("Id", Id);
//     element.setAttribute("name", name)
//     return element
// }


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
    noOfColumns = 4;
    var Table = document.getElementById('stageTable');
    var FormNoElement = document.getElementById('id_milestone-TOTAL_FORMS');
    

    // var example =0;     
    // if (FormNoElement==null){       
    //     example =1;     
    // }       
    // else{       
    //     example=FormNoElement.value;        
    // }       
                  
    // var formNo = parseInt(example); 


    var formNo = parseInt(FormNoElement.value); 
    var beforeRow = document.getElementById('row'+formNo);
    newRow = addRow('row'+(formNo+1), noOfColumns);

    StageId = 'milestone-'+ formNo + '-id'
    StageId = addElement("input", "hidden", "id_"+StageId, StageId);
    newRow.childNodes[0].style.width = "95%"
    newRow.childNodes[0].appendChild(StageId);
    
    stagePlanned = 'milestone-'+ formNo + '-planned_days';
    planned = addElement("input", "text", "id_"+stagePlanned, stagePlanned);
    planned.setAttribute("maxlength", "120");
    newRow.childNodes[0].appendChild(planned);

    stageName = 'milestone-'+ formNo + '-milestone';
    nameOfStage = addElement("input", "text", "id_"+stageName, stageName);
    nameOfStage.setAttribute("maxlength", "120");
    newRow.childNodes[0].appendChild(nameOfStage);

    stageDate = 'milestone-'+ formNo + '-from_date';
    nameDate = addElement("input", "text", "id_"+stageDate, stageDate);
    nameDate.setAttribute("maxlength", "120");
    nameDate.setAttribute("class", "vDateField");
    newRow.childNodes[0].appendChild(nameDate);
    FormNoElement.value = parseInt(formNo) + 1;
    DateTimeShortcuts.addCalendar(nameDate);

    stagePercent = 'milestone-'+ formNo + '-percentage';
    percent = addElement("input", "text", "id_"+stagePercent, stagePercent);
    percent.setAttribute("maxlength", "100");
    newRow.childNodes[0].appendChild(percent);
    

    var btn = document.createElement("BUTTON");
    var t = document.createTextNode(" - ");
    btn.appendChild(t);
    btn.onclick = function(){
        removeStageElement(this);
    };
    newRow.childNodes[0].appendChild(btn);

    Table.appendChild(newRow);
    FormNoElement.value = parseInt(formNo) + 1;
    // DateTimeShortcuts.addCalendar(nameDate);
}


function removeStageElement(id)
{
    alert('remove');
    var Table = document.getElementById('stageTable');
    var FormNoElement = document.getElementById('id_milestone-TOTAL_FORMS');
    var formNo = parseInt(FormNoElement.value); 
    var FormCount = document.getElementById('StageFormCount').value;
    // var child = document.getElementById('row'+formNo);
    var p=id.parentNode.parentNode;
    p.parentNode.removeChild(p);
    // if (formNo >= FormCount){
    //     Table.removeChild(child);
    //     FormNoElement.value = formNo - 1;
    // }
}


function createTimeBasedElement()
{
    noOfColumns = 3;
    var Table = document.getElementById('id_invoice_date');
    var FormNoElement = document.getElementById('id_timebased-TOTAL_FORMS');

    // var example =0;     
    // if (FormNoElement==null){       
    //     example =1;     
    // }       
    // else{       
    //     example=FormNoElement.value;        
    // }       
                  
    // var formNo = parseInt(example); 

    var formNo = parseInt(FormNoElement.value); 
    var beforeRow = document.getElementById('rowsd'+formNo);
    newRow = addRow('rowsd'+(formNo+1), noOfColumns);

    timebasedId = 'timebased-'+ formNo + '-id';
    timebasedId = addElement("input", "hidden", "id_"+ timebasedId, timebasedId);
    newRow.childNodes[0].style.width = "95%";
    newRow.childNodes[0].appendChild(timebasedId);

    timebasedDate = 'timebased-'+ formNo + '-from_date';
    nameDate = addElement("input", "text", "id_"+timebasedDate, timebasedDate);
    nameDate.setAttribute("maxlength", "120");
    nameDate.setAttribute("class", "vDateField");
    newRow.childNodes[0].appendChild(nameDate);
    FormNoElement.value = parseInt(formNo) + 1;
    DateTimeShortcuts.addCalendar(nameDate);

    timebasedDate = 'timebased-'+ formNo + '-to_date';
    nameDate = addElement("input", "text", "id_"+timebasedDate, timebasedDate);
    nameDate.setAttribute("maxlength", "120");
    nameDate.setAttribute("class", "vDateField");
    newRow.childNodes[0].appendChild(nameDate);

    stagecategory = 'timebased-'+ formNo + '-category';
    category = addElement("select", "dropdown", "id_"+stagecategory, stagecategory);

    

    category.setAttribute("maxlength", "120");
    newRow.childNodes[0].appendChild(category);



    var btn = document.createElement("BUTTON");
    var t = document.createTextNode(" - ");
    btn.appendChild(t);
    btn.onclick = function(){
        removeTimeBasedElement(this);
    };
    newRow.childNodes[0].appendChild(btn);


    Table.appendChild(newRow);
    FormNoElement.value = parseInt(formNo) + 1;
    DateTimeShortcuts.addCalendar(nameDate);

    var select = document.getElementById('id_'+ stagecategory);
    var options = ["---------", "Monthly", "Bi-Monthly"];
    for(var i = 0; i < options.length; i++) {
        var opt = options[i];
        var el = document.createElement("option");
        el.textContent = opt;
        el.value = opt;
        select.appendChild(el);
    }


}



function removeTimeBasedElement(id)
{
    var Table = document.getElementById('id_invoice_date');
    var FormNoElement = document.getElementById('id_timebased-TOTAL_FORMS');
    var formNo = parseInt(FormNoElement.value); 
    var FormCount = document.getElementById('TimebasedFormCount').value;
    var p=id.parentNode.parentNode;
    p.parentNode.removeChild(p);
}





function addClassRow(className, appendTo){
    console.log()
    var rows = document.getElementsByClassName(className);
    alert(rows)
    var cloned = $('#' + rows[0].id).clone();
    cloned.id = "row" + (rows.length - 1);
    $( "#" + rows[rows.length - 1].id ).after( cloned );
}



function createSpecificDatesElement()
{
    noOfColumns = 3;
    console.log()
    var Table = document.getElementById('SpecificDatesTable');
    var rowCount = Table.rows.length; 
    var formNo;
    var FormNoElement;
    if(rowCount > 0) {
        rowCount = rowCount -2
        formNo=rowCount;
        FormNoElement = formNo; 
    }
    else{
      FormNoElement = document.getElementById('id_specificdates-TOTAL_FORMS');  
      formNo = parseInt(FormNoElement.value); 
    }
    

    // var example =0;     
    // if (FormNoElement==null){       
    //     example =1;     
    // }       
    // else{       
    //     example=FormNoElement.value;        
    // }       
                  
    // var formNo = parseInt(example); 
    
    var beforeRow = document.getElementById('rowsd'+formNo);
    newRow = addRow('rowsd'+(formNo+1), noOfColumns);

    specificdatesId = 'specificdates-'+ formNo + '-id';
    specificdatesId = addElement("input", "hidden", "id_"+ specificdatesId, specificdatesId);
    newRow.childNodes[0].style.width = "95%";
    newRow.childNodes[0].appendChild(specificdatesId);

    specificdatesDate = 'specificdates-'+ formNo + '-from_date';
    nameDate = addElement("input", "text", "id_"+specificdatesDate, specificdatesDate);
    nameDate.setAttribute("maxlength", "120");
    nameDate.setAttribute("class", "vDateField");
    newRow.childNodes[0].appendChild(nameDate);
    FormNoElement.value = parseInt(formNo) + 1;
    DateTimeShortcuts.addCalendar(nameDate);

    specificdatesDate = 'specificdates-'+ formNo + '-to_date';
    nameDate = addElement("input", "text", "id_"+specificdatesDate, specificdatesDate);
    nameDate.setAttribute("maxlength", "120");
    nameDate.setAttribute("class", "vDateField");
    newRow.childNodes[0].appendChild(nameDate);

    // var btn = document.createElement("BUTTON");
    // var t = document.createTextNode(" - ");
    // btn.appendChild(t);
    // newRow.childNodes[0].appendChild(btn);

    // specificdatesDEL = 'specificdates-'+ formNo + '-DELETE'
    // DEL = addElement("input", "checkbox", "id_"+ specificdatesDEL, specificdatesDEL);
    
    // newRow.childNodes[2].style.width = "10%"
    // newRow.childNodes[2].appendChild(DEL);
    // newRow.style.width = "50%";

    // """support filed incremented"""


    var btn = document.createElement("BUTTON");
    var t = document.createTextNode(" - ");
    btn.appendChild(t);
    btn.onclick = function(){
        removeSpecificDatesElement(this);
    };
    newRow.childNodes[0].appendChild(btn);



    Table.appendChild(newRow);
    FormNoElement.value = parseInt(formNo) + 1;
    DateTimeShortcuts.addCalendar(nameDate);
}


function removeSpecificDatesElement(id)
{
    var Table = document.getElementById('SpecificDatesTable');
    var FormNoElement = document.getElementById('id_specificdates-TOTAL_FORMS');
    var formNo = parseInt(FormNoElement.value); 
    var FormCount = document.getElementById('SpecificDatesFormCount').value;
    var p=id.parentNode.parentNode;
    p.parentNode.removeChild(p);
}












// function removeStageElement()
// {
//     var Table = document.getElementById('stageTable');
//     var FormNoElement = document.getElementById('id_milestone-TOTAL_FORMS');
//     var formNo = parseInt(FormNoElement.value); 
//     var FormCount = document.getElementById('StageFormCount').value;
//     var child = document.getElementById('row'+formNo);
//     if (formNo > FormCount){
//         Table.removeChild(child);
//         FormNoElement.value = formNo - 1;
//     }
// }

function removeTimeBasedElement1()
{
    var Table = document.getElementById('id_invoice_date');
    var FormNoElement = document.getElementById('id_timebased-TOTAL_FORMS');
    var formNo = parseInt(FormNoElement.value); 
    var FormCount = document.getElementById('TimebasedFormCount').value;
    // var child = document.getElementById('rows'+formNo);
    // if (formNo > FormCount){
    //     Table.removeChild(child);
    //     FormNoElement.value = formNo - 1;
    // }

    var node = document.getElementById('rows'+formNo);
    if (formNo > FormCount){
        Table.removeChild(node);
        FormNoElement.value = parseInt(formNo) - 1;
    }

}


function removeSpecificDatesElement1()
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
    // var child = document.getElementById('rowsd'+formNo);
    // if (formNo > FormCount){
    //     Table.removeChild(child);
    //     FormNoElement.value = formNo - 1;
    // }
    
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
 dateClean('id_from_date');
 dateClean('id_to_date');
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
    var dateDict = dateValue.split('-');
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
    $('#id_timebased-0-from_date').val(changeFormat($('#id_timebased-0-from_date').val()));
    $('#id_timebased-0-to_date').val(changeFormat($('#id_timebased-0-to_date').val()));
    
    for(var each=0; each < parseFloat($('#id_specificdates-TOTAL_FORMS').val()); each++){
        $('#id_specificdates-'+each+'-from_date').val(changeFormat($('#id_specificdates-'+each+'-from_date').val()));
        // $('#id_specificdates-'+each+'-to_date').val(changeFormat($('#id_specificdates-'+each+'-to_date').val()));
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
    convertDate('id_from_date');
    convertDate('id_to_date');
    convertDate('id_timebased-0-from_date');
    convertDate('id_timebased-0-to_date');
    document.getElementById("id_name").focus();
    if($('#id_id').val() == ''){$('#id_active').attr('checked', true);}
    $('#planned_effort_days').val($('#id_planned_effort').val());
   
    $('input#id_name').slugify('input#id_short_name');
    $('#id_timebased-0-DELETE').css('visibility', 'hidden');
    $('#cancel_bttop').click(function(){ window.location.href = '/project/list/' });
    $('#cancel_bt').click(function(){ window.location.href = '/project/list/' });


    


    $('#id_milestone-TOTAL_FORMS').val($('#StageFormCount').val());
    $('#id_timebased-TOTAL_FORMS').val($('#TimebasedFormCount').val());
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
        $('#id_specificdates-'+each+'-from_date').attr('class', 'vDateField');
        convertDate('id_specificdates-'+each+'-from_date');
        $('#id_specificdates-'+each+'-to_date').attr('class', 'vDateField');
        convertDate('id_specificdates-'+each+'-to_date');

        };
    // for(var each=0; each<parseFloat($('#id_specificdates-TOTAL_FORMS').val()); each++){
    //     $('#id_specificdates-'+each+'-to_date').attr('class', 'vDateField');
    //     convertDate('id_specificdates-'+each+'-to_date');

    //     };


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
    
    



    $('#id_timebased-0-from_date').attr('class','vDateField');
    $('#id_timebased-0-to_date').attr('class','vDateField');
    $('#id_timebased-1-from_date').attr('class','vDateField');
    $('#id_timebased-1-to_date').attr('class','vDateField');
    $('#id_timebased-2-from_date').attr('class','vDateField');
    $('#id_timebased-2-to_date').attr('class','vDateField');
    $('#id_timebased-3-from_date').attr('class','vDateField');
    $('#id_timebased-3-to_date').attr('class','vDateField');
    $('#id_timebased-4-from_date').attr('class','vDateField');
    $('#id_timebased-4-to_date').attr('class','vDateField');
    $('#id_timebased-5-from_date').attr('class','vDateField');
    $('#id_timebased-5-to_date').attr('class','vDateField');
    $('#id_timebased-6-from_date').attr('class','vDateField');
    $('#id_timebased-6-to_date').attr('class','vDateField');
    $('#id_timebased-7-from_date').attr('class','vDateField');
    $('#id_timebased-7-to_date').attr('class','vDateField');
    $('#id_timebased-8-from_date').attr('class','vDateField');
    $('#id_timebased-8-to_date').attr('class','vDateField');
    $('#id_timebased-9-from_date').attr('class','vDateField');
    $('#id_timebased-9-to_date').attr('class','vDateField');
    $('#id_timebased-10-from_date').attr('class','vDateField');
    $('#id_timebased-10-to_date').attr('class','vDateField');
    $('#id_timebased-11-from_date').attr('class','vDateField');
    $('#id_timebased-11-to_date').attr('class','vDateField');
    $('#id_timebased-12-from_date').attr('class','vDateField');
    $('#id_timebased-12-to_date').attr('class','vDateField');
    $('#id_timebased-0-category').find('option[value="0"], option[value="1"], option[value="6"]').remove()


    $('#id_milestone-0-from_date').attr('class','vDateField');
    $('#id_milestone-1-from_date').attr('class','vDateField');
    $('#id_milestone-2-from_date').attr('class','vDateField');
    $('#id_milestone-3-from_date').attr('class','vDateField');
    $('#id_milestone-4-from_date').attr('class','vDateField');
    $('#id_milestone-5-from_date').attr('class','vDateField');
    $('#id_milestone-6-from_date').attr('class','vDateField');
    $('#id_milestone-7-from_date').attr('class','vDateField');
    $('#id_milestone-8-from_date').attr('class','vDateField');
    $('#id_milestone-9-from_date').attr('class','vDateField');
    $('#id_milestone-10-from_date').attr('class','vDateField');
    $('#id_milestone-11-from_date').attr('class','vDateField');
    $('#id_milestone-12-from_date').attr('class','vDateField');
    $('#id_milestone-13-from_date').attr('class','vDateField');
    $('#id_milestone-14-from_date').attr('class','vDateField');
    $('#id_milestone-15-from_date').attr('class','vDateField');

    $('#id_milestone-0-from_date').val(changeFormat($('#id_timebased-0-from_date').val()));
    


    $('#id_specificdates-0-from_date').attr('class','vDateField');
    $('#id_specificdates-0-to_date').attr('class','vDateField');
    $('#id_specificdates-1-from_date').attr('class','vDateField');
    $('#id_specificdates-1-to_date').attr('class','vDateField');
    $('#id_specificdates-2-from_date').attr('class','vDateField');
    $('#id_specificdates-2-to_date').attr('class','vDateField');
    $('#id_specificdates-3-from_date').attr('class','vDateField');
    $('#id_specificdates-3-to_date').attr('class','vDateField');
    $('#id_specificdates-4-from_date').attr('class','vDateField');
    $('#id_specificdates-4-to_date').attr('class','vDateField');
    $('#id_specificdates-5-from_date').attr('class','vDateField');
    $('#id_specificdates-5-to_date').attr('class','vDateField');
    $('#id_specificdates-6-from_date').attr('class','vDateField');
    $('#id_specificdates-6-to_date').attr('class','vDateField');
    $('#id_specificdates-7-from_date').attr('class','vDateField');
    $('#id_specificdates-7-to_date').attr('class','vDateField');
    $('#id_specificdates-8-from_date').attr('class','vDateField');
    $('#id_specificdates-8-to_date').attr('class','vDateField');
    $('#id_specificdates-9-from_date').attr('class','vDateField');
    $('#id_specificdates-9-to_date').attr('class','vDateField');
    $('#id_specificdates-10-from_date').attr('class','vDateField');
    $('#id_specificdates-10-to_date').attr('class','vDateField');
    $('#id_specificdates-11-from_date').attr('class','vDateField');
    $('#id_specificdates-11-to_date').attr('class','vDateField');
    $('#id_specificdates-12-from_date').attr('class','vDateField');
    $('#id_specificdates-12-to_date').attr('class','vDateField');





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
	   if(!isBetweenDate(document.getElementById("id_from_date").value, document.getElementById("id_to_date").value)) {
       	 	alert ('Planned end date occurs before the planned start date');
    		document.getElementById('id_to_date').focus();
    		return false;
     	}    
        else {
             document.program.action = '/project/initiation/';
             return true;
       	}
}
