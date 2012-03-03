
var IsiPhone = navigator.userAgent.indexOf("iPhone") != -1 ;
var IsiPod = navigator.userAgent.indexOf("iPod") != -1 ;
var IsiPad = navigator.userAgent.indexOf("iPad") != -1 ;
var IsiPhoneOS = IsiPhone || IsiPad || IsiPod ; 




function isBlank(A){return A.replace(/\s+/g,"").length==0}

function isValidEmailAddress(emailAddress) {
    var pattern = new RegExp(/^(("[\w-\s]+")|([\w-]+(?:\.[\w-]+)*)|("[\w-\s]+")([\w-]+(?:\.[\w-]+)*))(@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$)|(@\[?((25[0-5]\.|2[0-4][0-9]\.|1[0-9]{2}\.|[0-9]{1,2}\.))((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[0-9]{1,2})\.){2}(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[0-9]{1,2})\]?$)/i);
    return pattern.test(emailAddress);
}

function isValidLogin(login) {
    //^([^.])([\w_.]+)([^.])$
    //var pattern = new RegExp(/^([\w_]+[\w])(?!.)$/);
    //var pattern = new RegExp(/^([^.])([\w_.]+)([^.])$/);
    var pattern = new RegExp(/^([a-zA-Z0-9]{1,2})$|^([a-z0-9]([^\-_.]??)[a-z0-9_\.-]+[a-z0-9])$/);
    //

    return pattern.test(login);
}

function isValidDate(data) {
    //(0[1-9]|[12][0-9]|3[01])\/(0[1-9]|1[012])\/(19|20)\d\d
    //var pattern = new RegExp(/^(0[1-9]|[12][0-9]|3[01])[/](0[1-9]|1[012])[/](19|20)\d\d$/);
    var pattern = new RegExp(/^(0[1-9]|[12][0-9]|3[01])\/(0[1-9]|1[012])\/(19|20)\d\d$/);
    return pattern.test(data);
}

function isValidNumber(number) {
    var pattern = new RegExp(/^([\d]+)$/);
    return pattern.test(number);
}

function isValidHexNumber(number) {
    var pattern = new RegExp(/^([A-Fa-f0-9]+)$/);
    return pattern.test(number);
}


function isValidUrl(url) {
    if (isBlank(url))
        return false;
    return true;
}

function isValidOrkutUrl(url) {
    if(isValidUrl(url)) {
        return true;
    }
    return false;
}

function isValidFacebookUrl(url) {
    if(isValidUrl(url)) {
        return true;
    }
    return false;
}





function PermiteApenasNumeros(e) {
    var key = window.event ? e.keyCode : e.which;
    var keychar = String.fromCharCode(key);
    
    switch(key) {
        case 8:
        case 13:
        case 0:
            return true; break;
        default: return /[0-9]/.test(keychar); break;
    }
}


function PermiteApenasHex(e) {
    var key = window.event ? e.keyCode : e.which;
    var keychar = String.fromCharCode(key);
    
    switch(key) {
        case 8:
        case 13:
        case 0:
            return true; break;
        default: return /[a-fA-F0-9]/.test(keychar); break;
    }
}


function PermiteApenasLoginPonto(e) {
    var key = window.event ? e.keyCode : e.which;
    var keychar = String.fromCharCode(key);
    
    switch(key) {
        case 8:
        case 13:
        case 0:
            return true; break;
        default: return /[a-zA-Z0-9_.]/.test(keychar); break;
    }
}

function PermiteApenasLogin(e) {
    var key = window.event ? e.keyCode : e.which;
    var keychar = String.fromCharCode(key);
    
    switch(key) {
        case 8:
        case 13:
        case 0:
            return true; break;
        default: return /[a-zA-Z0-9_]/.test(keychar); break;
    }
}






function BlockMove(event) {
	event.preventDefault();
}







function get_locale_date(data_utc) {
	//alert(data.replace(/-/g, "/"));
	//utc_date = new Date(data.replace(/-/g, "/"));
	
	var data_hora = data_utc.split("T");
	var data = data_hora[0].split("-");
	var hora = data_hora[1].split(":");

	var d = new Date();
	d.setUTCFullYear(data[0]);
	d.setUTCMonth(data[1]);
	d.setUTCDate(data[2]);
	d.setUTCHours(hora[0]);
	d.setUTCMinutes(hora[1]);
	d.setUTCSeconds(hora[2]);
	return d;
	//var utc_date = new Date(data);
	//d.setUTCFullYear(utc_date.getFullYear());
	//d.setUTCMonth(utc_date.getMonth());
	//d.setUTCDate(utc_date.getDate());
	//d.setUTCHours(utc_date.getHours());
	//d.setUTCMinutes(utc_date.getMinutes());
	//d.setUTCSeconds(utc_date.getSeconds());

}
function format_date(data) {
	var dt = get_locale_date(data);
	return check_number(dt.getDate()) + "/" + 
		check_number(dt.getMonth()+1) + " " + 
		check_number(dt.getHours()) + "h" + 
		check_number(dt.getMinutes());
}
function format_date_timestamp(data) {
	var dt = new Date(data*1000);
	return check_number(dt.getDate()) + "/" + 
		check_number(dt.getMonth()+1) + " " + 
		check_number(dt.getHours()) + "h" + 
		check_number(dt.getMinutes());
}

function format_date_simple(data) {
	var dt = get_locale_date(data);
	return check_number(dt.getDate()) + "/" + 
		check_number(dt.getMonth());
}
function check_number(i) {
	if (i<10) return "0" + i.toString();
	return i.toString();
}
function format_phone_number(phone) {
	switch(phone.length) {
		case 10:
			return "(" + phone.substr(0, 2) + ") " + phone.substr(2, 4)+ "-" + phone.substr(6);
			break;
		case 8:
			return phone.substr(0, 4) + "-" + phone.substr(4);
			break;
		default:
			return phone;
	}
}



function zeroPad(num, places) {
  var zero = places - num.toString().length + 1;
  return Array(+(zero > 0 && zero)).join("0") + num;
}


function mod10CheckDigit(barcode) {
	// Luhn algorithm producer, by Avraham Plotnitzky. (aviplot at gmail)
    var luhnArr = [[0,1,2,3,4,5,6,7,8,9],[0,2,4,6,8,1,3,5,7,9]], sum = 0;
    barcode.replace(/\D+/g,"").replace(/[\d]/g, function(c, p, o){
        sum += luhnArr[ (o.length-p)&1 ][ parseInt(c,10) ]
    });
    return ((10 - sum%10)%10);
}
/*
function mod10CheckDigit_old(barCode) {
	//Strip all characters except numbers
	bc = barCode.replace(/[^0-9]+/g,'');
	total = 0;

	//Get Odd Numbers
	for (i=0; i<bc.length; i=i+2) {
		if ((parseInt(bc.substr(i,1)) * 2) > 9) {
			total = total + (parseInt(bc.substr(i,1)) * 2) - 9;
		} else {
			total = total + (parseInt(bc.substr(i,1)) * 2);
		}
	}
	//0, 2, 4, 6, 8, ..

	//Get Even Numbers
	for (i=1; i<bc.length; i=i+2) {
		total = total + (parseInt(bc.substr(i,1)));
	}
	//1, 3, 5, 7, 9, ..

	//Determine the checksum
	modDigit = (10 - total % 10) % 10;

	alert ("TOTAL " + total);
	alert ("DIGITO " + modDigit);
	return modDigit;
}
*/


