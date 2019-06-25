

function ReqValidate(controls,fileds)
{

	controlname = controls.split(',');
	filedname  = fileds.split(',');
	len = controlname.length;
	for (var i=0;i<	len;i++)
	{
		value = document.getElementById(controlname[i]).value;
		if (value.indexOf(' ') == 0)
		{
			alert('Prefix space not allowed for '+filedname[i]);
			return false;
		}
		if(value == '')
		{
			alert(filedname[i] +' should not be empty.');
			document.getElementById(controlname[i]).focus();
			return false;
		}
		
	}
	
	return true;
}

function ComboValidate(controls,fields)
{
	controlname = controls.split(',');
	filedname  = fields.split(',');
	len = controlname.length;	

	for (var i=0;i<	len;i++)
	{
		if(document.getElementById(controlname[i]).value == '0')
		{
			alert('Select '+filedname[i]+' from the list.');
			return false;
		}
	}
	return true;	
}

function deleteconfirmation(chk)
{	
    if (chk == null)
	return false;
    if(chk.length !=null)
    {
		
        var checked= 0
        for (i = 0; i < chk.length; i++)
        {
       
	        if(chk[i].checked == true )
	        {
	          checked =1 ;
		      return confirm("Are you sure you want to delete?")
	        }
    	   
	     }	    
	 }
	 if(chk.checked == false || checked ==0)
	 {
	    alert("Select a Record to delete");
	        return false;
	 }
	 else
	    return confirm("Are you sure you want to delete?")
	 
}

function getComboValue(controls,fields)
{

    controlname = controls.split(',');
        filedname  = fields.split(',');
        len = controlname.length;
        for (var i=0;i< len;i++)
        {
                if(document.getElementById(controlname[i]).value != '')
                {
             //alert(document.getElementById(controlname[i]).value);
             document.getElementById(filedname[i]).value = document.getElementById(controlname[i]).value;
        }
    }
}


function doCheck(strForm)
{
  if(strForm)
	{
        objForm = document.getElementById(strForm);
	
        for(i=0; i < objForm.elements.length; i++)
		{
            if(objForm.elements[i].type == "checkbox")
			{
	            if(objForm.elements[i].checked == false)
				{
			
                	objForm.elements[i].checked = true;
				}
                	
			}
			   		
    	}
	}

}

function unCheck(strForm)
{
  if(strForm)
	{
        objForm = document.getElementById(strForm);
	
        for(i=0; i < objForm.elements.length; i++)
		{
            if(objForm.elements[i].type == "checkbox")
			{
	            if(objForm.elements[i].checked == true)
				{
			
                	objForm.elements[i].checked = false;
				}
                	
			}
			   		
    	}
	}

}

function FormCheck(strForm, obj)
{
	
	var checked = $(obj).attr('checked');
	
  if(strForm)
	{
        objForm = document.getElementById(strForm);
	
        for(i=0; i < objForm.elements.length; i++)
		{
            if(objForm.elements[i].type == "checkbox")
			{
				objForm.elements[i].checked = checked;	           
			}			   		
		}
		$(obj).attr('checked',checked);
	}
	
}

function emailValidation(controlname)
{

if(document.getElementById(controlname))
{
var email = document.getElementById(controlname).value;
	if(email != '')
	{

		var filter = /^[a-zA-Z][\w\.-]*[a-zA-Z0-9]@[a-zA-Z0-9][\w\.-]*[a-zA-Z0-9]\.[a-zA-Z][a-zA-Z\.]*[a-zA-Z]$/;
		if (!(filter.test(email))) 
		{ 
		   alert('Please enter a valid Email Id');
		   document.getElementById(controlname).focus();
		   return false;
		}
		else 
			return true;
	}
	else
		document.getElementById(controlname).focus();
		return false;
}
else
	document.getElementById(controlname).focus();
	return false;
}


function checkdate(objName) 
{
var datefield = objName;
/*if (chkdate(objName) == false)
{
datefield.select();
alert("That date is invalid.  Please try again.");
datefield.focus();
return false;
}
else {
return true;
   }*/
return true;
}



function fromToDateCheck(from,to){    
    var valid = false;
    if(document.getElementById(from)==null)
        return true;
        
    fromDate = getDate(from);
    toDate = getDate(to);
    if (Date.parse(fromDate) > Date.parse(toDate)) {
        valid = false;
        alert ("Start date should be greater than the end date.");
        }
    else {
        valid = true;
    }
     
   return valid;   
}

function plannedActualDateCheck(planned,actual){    
    var valid = false;
	if(document.getElementById(planned)==null)
        return true;
    var plannedDate = getDate(planned);
    var actualDate = getDate(actual);
    if (Date.parse(plannedDate) > Date.parse(actualDate)) {
        valid = false;
        alert ("Actual date should be within the planned date.");
        }
    else {
        valid = true;
    }
   return valid;   
}

function TaskDateCheck(planned,actual){    
    var valid = false;
	if(document.getElementById(planned)==null)
        return true;
    var plannedDate = getDate(planned);
    var actualDate = getDate(actual);
    if (Date.parse(plannedDate) > Date.parse(actualDate)) {
        valid = false;
        alert ("Task date should be within the program date.");
        }
    else {
        valid = true;
    }
   return valid;   
}

function ProjectDateCheck(planned,actual){  

    var valid = false;
    var plannedDate = getProjDate(planned);
    var actualDate = getProjDate(actual);

if ((plannedDate) > (actualDate)) {
//  if (Date.parse(plannedDate) > Date.parse(actualDate)) {
        valid = false;
        alert ("Project planned date should be within the program planned date.");
        }
    else {
        valid = true;
    }
   return valid;   
}

function DateCheck(planned,actual,start,end,action){    
    var valid = false;
	if(document.getElementById(planned)==null)
        return true;
    var plannedDate = getDate(planned);
    var actualDate = getDate(actual);
    if (Date.parse(plannedDate) > Date.parse(actualDate)) {
        valid = false;
        alert (start +' should not be '+ action + ' than ' +end);
        }
    else {
        valid = true;
    }
   return valid;   
}

function getProjDate(obj){
    var strDate = obj;
	
    var dateObj;
    if(strDate.length >=10){
        dateObj = strDate.split('-');
     }
    var dateValue = new Date();
frmt = formatDate();
if (frmt == 'd-m-Y')
	dateValue = new Date(dateObj[2].toString(),dateObj[1].toString(),dateObj[0].toString());
else
	dateValue = new Date(dateObj[2].toString(),dateObj[0].toString(),dateObj[1].toString());
//dateValue.setFullYear(dateObj[2],dateObj[0],dateObj[1]); 
alert(dateValue);
    return dateValue;
}

function getDate(obj){
    //mm/dd/yyyy
    var strDate = document.getElementById(obj).value;
	
    var dateObj;
    if(strDate.length >=10){
        dateObj = strDate.split('-');
     }
    var dateValue = new Date();
    dateValue.setFullYear(dateObj[2],dateObj[1],dateObj[0]);  
    return dateValue;
}

function convertDate(obj)
{
  if (document.getElementById(obj) == null)
	return;  
   dateVal = document.getElementById(obj).value ;

   if( dateVal != '')
   {                      
        frmt = formatDate();
	frmtVal = frmt.split('-');
	var m =''; // to represent the month index
	var d = ''; // to represent the day index
	var y = ''; // to represent the year index			
	if ((dateVal.split("-")[0]).length > 2 )
	{
		y = 0;
		m = 1;
		d = 2;
	}		
	else if(frmtVal[0]=='m')
	{
		m=0;
		d=1;
		y=2;	
 	}
	else
	{
		d=0;
		m=1;
		y=2;			
	}
	var yearfield=dateVal.split("-")[y];
	var monthfield = dateVal.split("-")[m];
	var dayfield = dateVal.split("-")[d];

	daytimefield = dayfield.split(' ')
	if (daytimefield.length > 0)
		dayfield = daytimefield[0]
	var day = new Date(yearfield, monthfield-1, dayfield);	
        document.getElementById(obj).value = day.strfdate(frmt);
	
   }
}

function isDate(value){

if(value.length==0){
	return true; }
var returnval = false;
if(value.indexOf(' ') == 0)
	return false;	
		var monthfield = '';
		var dayfield = '';
		
		frmt = formatDate();
		frmtVal = frmt.split('-');		

		if(frmtVal[0]=='m'){	
			monthfield=value.split("-")[0];
		 	dayfield=value.split("-")[1]; }
		else{
				dayfield=value.split("-")[0];
				monthfield=value.split("-")[1]; }

		var yearfield=value.split("-")[2];
	
		var dayobj = ''
		try {	
			if (yearfield.length <= 3 || yearfield.length > 4)
			{
				returnval = false;
				return returnval;
			}
	
			dayobj = new Date(yearfield, monthfield-1, dayfield);			
			if ((dayobj.getMonth()+1!=monthfield)||(dayobj.getDate()!=dayfield)||(dayobj.getFullYear()!=yearfield))
				returnval = false;
		else
		returnval=true;
			 }
		catch(err){			
			returnval = false;
		}
	return returnval;
}

function isBetweenDate(fromDt,toDt){    
    var valid = false;
	if(fromDt == null)
        return true;
   if( toDt == null)
        return true;
   frmt = formatDate();
	frmtVal = frmt.split('-');
	var monthfield =''
	var dayfield = ''
	var tomonthfield =''
	var todayfield = ''
			
	if(frmtVal[0]=='m'){	
			monthfield = fromDt.split("-")[0];
		 	dayfield = fromDt.split("-")[1];
		 	tomonthfield = toDt.split("-")[0];
		 	todayfield = toDt.split("-")[1]; 
		 	}
	else{
			dayfield=fromDt.split("-")[0];
			monthfield=fromDt.split("-")[1];
			tomonthfield = toDt.split("-")[1];
		 	todayfield = toDt.split("-")[0];  
			}
	var yearfield=fromDt.split("-")[2];
	var toyearfield=toDt.split("-")[2];
				
	var fromDay = new Date(yearfield, monthfield-1, dayfield);	
	var toDay = new Date(toyearfield, tomonthfield-1, todayfield);

    if (fromDay > toDay) {
        valid = false;        
        }
    else {
        valid = true;
    }

   return valid;   
}

function isNumeric(value) {
  if (value == null || !value.toString().match(/^[-]?\d*\.?\d*$/)) return false;
  return true;
}

function isContactNum(value) {
  if (value == null || !value.toString().match(/^[+]?[0-9]*$/)) return false;
  return true;
}

function isOfficeNum(value) {
  if (value == null || !value.toString().match(/^(\(?\+?[0-9]*\)?)?[0-9\#\- \(\)\?]*$/)) return false;
  return true;
}


function isZipCode(value){
	if (value == null || !value.toString().match(/(^\d*$)|(^\d{5}(-\d{4})?$)|(^[ABCEGHJKLMNPRSTVXY]{1}\d{1}[A-Z]{1} *\d{1}[A-Z]{1}\d{1}$)/)) return false;
	return true;
}
var maxLength = 2000;
function doPaste(Object){

if (Object.value.length > maxLength)
{ 
           //Object.value = Object.value.substr(0,maxLength);   
	return false;
}

return true;
}


function imposeMaxLength(Object, event)
{

//8 or 0-Backspace
//9 or 46 Delete
var unicode=event.charCode? event.charCode : event.keyCode
	if ((unicode != null) &&  ( unicode == 13  || unicode == 8 || unicode == 0 || unicode == 9 || unicode == 46))
		return true;
  return (Object.value.length < maxLength);
}

function chkMaxlength(Object, text){

     if (Object.value.length > maxLength)
{ 
	alert(text +' should not exceed '+maxLength +' characters');
          return false;
}
return true;
}
function allTrim (wordString) {
    if ((wordString==null) || (wordString == '')) {
        return "";
    }
    while (wordString.substring(0,1) == ' ') {
        wordString = wordString.substring(1, wordString.length);
    }
    while (wordString.substring(wordString.length-1, wordString.length) == ' '){
        wordString = wordString.substring(0,wordString.length-1);
    }
    return wordString;
}

	
function dateMask(input)
{	
   format = formatDate();
	if (format == 'm-d-Y'){
		dateFormat = 'mm-dd-yyyy';
	}
	if (format == 'd-m-Y'){
		dateFormat = 'dd-mm-yyyy';
	}
	if (format == 'Y-m-d'){
		dateFormat = 'yyyy-mm-dd';
	}
   if (document.getElementById(input).value == null || document.getElementById(input).value == '' || document.getElementById(input).value == '2000-01-01')
   {
   	
   	document.getElementById(input).value = dateFormat;
   }
}

function dateClean(textin){
  if (document.getElementById(textin) == null)
	return;  
 if(document.getElementById(textin).value == "mm-dd-yyyy" || document.getElementById(textin).value == "dd-mm-yyyy" || document.getElementById(textin).value == "yyyy-mm-dd")
	{
		document.getElementById(textin).value = '';
	}
}

function CheckIsNumeric(event, obj) {
    var unicode = event.charCode ? event.charCode : event.keyCode;    
    //#,$,Space (unicode == 35) || (unicode == 36) || (unicode == 46)
    key = ((unicode == 189) || (unicode >= 48 && unicode <= 57) || (unicode == 27) || (unicode == 37) || (unicode == 39) || (unicode == 9) || (unicode == 46) || (unicode == 8));
    return key;
}

function CheckNumeric(obj) {
    var id = obj.id;
    var num = document.getElementById(id);
    var txtvalue = num.value;
    var result = parseFloat(txtvalue).toFixed(2);
    if (result.toString() === 'NaN') {
        $('#'+id).val('0.00');
        return false;
    }
    else {
        $('#'+id).val(result);
        return false;
    }
}
