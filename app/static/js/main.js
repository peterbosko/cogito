var responseOK=1;
var responseERROR=2;
var revalidacia_modal = false;

var AjaxMethods = {
    getDataFromGetRequest: function getDataFromGetRequest(dataFrom, params, data, callback) {
        var res=null;
        $.ajax({
            async: false,
            url: dataFrom+params+data,
            type: 'GET',
            success: function(result) {
                var res=JSON.parse(result);
                callback(res);
            },
            error: function(error) {
                console.log(error);
            }
        });
        return res;
    },
    getDataFromAsyncGetRequest: function getDataFromGetRequest(dataFrom, params, data, callback) {
        var res=null;
        $.ajax({
            async: true,
            url: dataFrom+params+data,
            type: 'GET',
            success: function(result) {
                var res=JSON.parse(result);
                callback(res);
            },
            error: function(error) {
                console.log(error);
            }
        });
        return res;
    },
    getDataFromPostRequest: function getDataFromPostRequest(dataFrom, params, data, callback) {
        var res=null;
        $.ajax({
            async: false,
            url: dataFrom+params,
            data : JSON.stringify(data),
            type: 'POST',
            contentType: 'application/json;charset=UTF-8',
            success: function(result) {
                var res=JSON.parse(result);
                callback(res);
            },
            error: function(error) {
                console.log(error);
            }
        });
        return res;
    },
    getDataFromAsyncPostRequest: function getDataFromAsyncPostRequest(dataFrom, params, data, callback) {
        var res=null;
        $.ajax({
            async: true,
            url: dataFrom+params,
            data : JSON.stringify(data),
            type: 'POST',
            contentType: 'application/json;charset=UTF-8',
            success: function(result) {
                var res=JSON.parse(result);
                callback(res);
            },
            error: function(error) {
                console.log(error);
            }
        });
        return res;
    }
};

function loadTemplateIntoModal(modalSelector, title, controlPath, fireMethod, methodParams) {

    var modalObj = $(modalSelector);
    modalObj.find('.modal-title').html(title);
    modalObj.find('.modal-body').html('<i class="fa fa-spinner fa-spin fa-lg"></i>');
    modalObj.removeClass('largescreen');
    modalObj.find('.modal-dialog').addClass('modal-lg');

    if ('#defaultModal' === modalSelector || '#defaultModal2' === modalSelector || '#defaultModal3' === modalSelector)
        modalObj.find('.modal-footer .btnSave').addClass('nodisplay').off('click');

    modalObj.find('.modal-body').load(controlPath, function () {

        if (fireMethod != "undefined" && fireMethod != null && fireMethod != '') {

            if (methodParams != "undefined") {
                window[fireMethod](methodParams);
            } else {
                window[fireMethod]();
            }
        }

    });

    modalObj.modal('show');
	
	if(revalidacia_modal == true && modalSelector === "#defaultModal2") {
		modalObj.on('hidden.bs.modal', function () {
			$('#setting-new-validation').click();
		})
	}
}

function loadTemplateIntoLargeScreenModal(modalSelector, cssClass, title, controlPath, fireMethod, methodParams) {
    loadTemplateIntoModal(modalSelector, title, controlPath, fireMethod, methodParams);
    var modalObj = $(modalSelector);
    modalObj.addClass(cssClass);
    modalObj.find('.modal-dialog').removeClass('modal-lg');
}

function getParameterFromUrl(p,u){
    if (!u){
        u = window.location;
    }
    var url = new URL(u);
    var r = url.searchParams.get(p);

    return r;
}

function gridButtonFormater(data, title, dropright, w) {

    var dropdowntoggle = "";

    if (!dropright){
        dropright = "";
    }
    else{
        dropright="dropright";
        dropdowntoggle = "dropdown-toggle"
    }

    var formaterTitle = "";

    if (title != null && title != "undefined") {
        formaterTitle = "&nbsp;" + title;
    }

    var style="";

    if (w){
        style='style="width:'+w+'" ';
    }

    return "<div class=\"dropup\"><div class='btn-group "+dropright+"'><button type='button' data-boundary='viewport' class='btn btn-primary btn-xs "+dropdowntoggle+"' data-toggle='dropdown'><i class='fa fa-list lg'></i> </button><ul "+style+" class='dropdown-menu blue-menu' role='menu'>" + data + " </ul>" + formaterTitle + "</div></div>";
}

function SpustiUnitTestyKontextu(id, successCallback, failCallback){
        var result=AjaxMethods.getDataFromGetRequest('/spusti_unit_test_kontextu/', id, '',
            function (r){
                if (r.status==responseOK){//OK vetva
                    swal({ buttons: {},
                       title  :  "Úspech",
                       text   :  r.message_text,
                       icon   :  "success"}).then(function(result) {
                                                if (successCallback)
                                                    successCallback();
                                              });
                } else{
                   swal({ buttons: {},
                       title  :  "Chyba",
                       text   :  r.message_text,
                       icon   :  "error"}).then(function(result) {
                                                if (failCallback)
                                                    failCallback();
                                              });
            }
        });
}

function daj_ut_status_class(data){
        var s = "novy-zmeneny-UT";

        if( data ==  'M' || data ==  'N'){
           s='novy-zmeneny-UT';
        }
        else if (data ==  'U'){
           s='uspesny-UT';
        }
        else if (data ==  'X'){
           s='neuspesny-UT';
        }

        return s;
}


function daj_ut_status(data){
        var statusDesc = 'Nový';

        if (data=="M")
            statusDesc = "Zmenený";
        else if (data=="U")
            statusDesc="Úspešný"
        else if (data=="X")
            statusDesc="Neúspešný"

        return statusDesc;
}


function ZmazUnitTest(id, func){
	swal({
		title: "Potvrdenie",
		text: "Naozaj zmazať unit test?",
		icon: "warning",
		buttons: ["Zrušiť","Zmazať"],
		dangerMode: true,
		}).then((willDelete) => {
			if (willDelete) {
				ZmazUnitTestBezOtazky(id, func);
			}
		});
}

function ZmazUnitTestBezOtazky(id, func){
	var result=AjaxMethods.getDataFromGetRequest('/zmaz_unit_test/', id, '',
		function (r){
			if (r.status==responseOK){//OK vetva
				swal({ buttons: {},
				   title  :  "Úspech",
				   text   :  "Unit test bol vymazaný",
				   icon   :  "success"}).then(function(result) {
											if (func) func();
										  });
			} else{
			   swal({ buttons: {},
				   title  :  "Chyba",
				   text   :  r.error_text,
				   icon   :  "error"});
		}

	});
}

function SpustiUnitTest(id, func, nezobrazovat_swal){
        var vysledok = false;
        var result=AjaxMethods.getDataFromGetRequest('/spusti_konkretny_unit_test/', id, '',
            function (r){
                if (r.status==responseOK){//OK vetva
                    vysledok=true;
                    if (!nezobrazovat_swal) {
                       swal({ buttons: {},
                           title  :  "Úspech",
                           text   :  r.message_text,
                           icon   :  "success"}).then(function(result) {
                                                    if (func) {
                                                        func();
                                                    }
                                                  });
                    }
                } else{
                    vysledok=false;
                    if (!nezobrazovat_swal)
                       swal({ buttons: {},
                           title  :  "Chyba",
                           text   :  r.message_text,
                           icon   :  "error"}).then(function(result) {
                                                    if (func) func();
                                                  });
                }
            });
            return vysledok;
}

var LoadedScripts = {};
var LoadedStyles = {};

function loadScript(url, callback) {
    var head = document.getElementsByTagName('head')[0];
    var script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = url;

    script.onload = callback;

    head.appendChild(script);
}

function loadStyle(url) {
    var head = document.getElementsByTagName('head')[0];
    var script = document.createElement('link');
    script.rel = "stylesheet";
    script.href = url;

    head.appendChild(script);
}

function loadNeededScriptsAndStyles(script, style, callback) {
    if (style){
        if (LoadedStyles[style] == null) {
            LoadedStyles[style] = 1;

            loadStyle(style);
        }
    }

    if (script) {
        if (LoadedScripts[script] == null) {
            LoadedScripts[script] = 1;

            loadScript(script, callback);

            return true;
        }
    }

    return false;
}




function nahrad_zobaky(str){
    return str.replace(/</g,"&lt;").replace(/>/g,"&gt;");
}

function bindSlovesoAutocomplete(selector){
	$(selector).select2({
		language: {
				errorLoading: function () {
					return "Výsledky sa nepodarilo načítať.";
				},
				inputTooLong: function (args) {
					var overChars = args.input.length - args.maximum;
					return "Prosím, zadajte o"+ ' ' + overChars + ' ' + 'znak/znaky/znakov menej';
				},
				inputTooShort: function (args) {
					var remainingChars = args.minimum - args.input.length;
					return "Prosím zadajte ďalšie" + ' ' + remainingChars + ' ' + 'znaky';
				},
				loadingMore: function () {
					return 'Načítavam viac výsledkov...';
				},
				maximumSelected: function (args) {
					return 'Môžete vybrať maximálne' + ' ' + args.maximum + ' ' + 'položiek';
				},
				noResults: function () {
					return 'Nenašli sa žiadne záznamy';
				},
				searching: function () {
					return 'Vyhľadávamie';
				}
			},
	  allowClear: true,
	  ajax: {
		url: "/daj_autocomplete_slovies",
		dataType: 'json',
		delay: 250,
		data: function (params) {
		  return {
			term: params.term, // search term
			page: params.page
		  };
		},
		processResults: function (data, params) {
		  // parse the results into the format expected by Select2
		  // since we are using custom formatting functions we do not need to
		  // alter the remote JSON data, except to indicate that infinite
		  // scrolling can be used
		  params.page = params.page || 1;

		  return {
			results: data.data,
			pagination: {
			  more: (params.page * 30) < data.total_count
			}
		  };
		},
		cache: true
	  },
	  placeholder: 'Hľadaj sloveso',
	  minimumInputLength: 3,
	  templateResult: function formatSloveso (sloveso) {
		  if (sloveso.loading) {
			return sloveso.text;
		  }

		  var $container = $(
			"<div class='select2-result-sloveso clearfix'>" +
				"<div class='select2-result-sloveso-text'></div>"+
			"</div>");

		  $container.find(".select2-result-sloveso-text").html(sloveso.text);

		  return $container;
		},
	  templateSelection: function formatSlovesoSelection (s) {
		  return s.text;
		}
	});
}

function bindUserAutocomplete(selector, placeholderText){
	placeholderText = placeholderText || "Hľadaj používateľa";
	$(selector).select2({
		language: {
				errorLoading: function () {
					return "Výsledky sa nepodarilo načítať.";
				},
				inputTooLong: function (args) {
					var overChars = args.input.length - args.maximum;
					return "Prosím, zadajte o"+ ' ' + overChars + ' ' + 'znak/znaky/znakov menej';
				},
				inputTooShort: function (args) {
					var remainingChars = args.minimum - args.input.length;
					return "Prosím zadajte ďalšie" + ' ' + remainingChars + ' ' + 'znaky';
				},
				loadingMore: function () {
					return 'Načítavam viac výsledkov...';
				},
				maximumSelected: function (args) {
					return 'Môžete vybrať maximálne' + ' ' + args.maximum + ' ' + 'položiek';
				},
				noResults: function () {
					return 'Nenašli sa žiadne záznamy';
				},
				searching: function () {
					return 'Vyhľadávamie';
				}
			},
	  allowClear: true,
	  ajax: {
		url: "/daj_autocomplete_user",
		dataType: 'json',
		delay: 250,
		data: function (params) {
		  return {
			term: params.term, // search term
			page: params.page
		  };
		},
		processResults: function (data, params) {
		  // parse the results into the format expected by Select2
		  // since we are using custom formatting functions we do not need to
		  // alter the remote JSON data, except to indicate that infinite
		  // scrolling can be used
		  params.page = params.page || 1;

		  return {
			results: data.data,
			pagination: {
			  more: (params.page * 30) < data.total_count
			}
		  };
		},
		cache: true
	  },
	  placeholder: placeholderText,
	  minimumInputLength: 3,
	  templateResult: function formatSloveso (sloveso) {
		  if (sloveso.loading) {
			return sloveso.text;
		  }

		  var $container = $(
			"<div class='select2-result-user clearfix'>" +
				"<div class='select2-result-user-text'></div>"+
			"</div>");

		  $container.find(".select2-result-user-text").html(sloveso.text);

		  return $container;
		},
	  templateSelection: function formatSlovesoSelection (s) {
		  return s.text;
		}
	});
}

function ZmazSlovnyDruh(id, func){
	swal({
		title: "Potvrdenie",
		text: "Naozaj zmazať celý slovný druh?",
		icon: "warning",
		buttons: ["Zrušiť","Zmazať"],
		dangerMode: true,
		}).then((willDelete) => {
			if (willDelete) {
				ZmazSlovnyDruhBezOtazky(id, func);
			}
		});
}

function ZmazSlovnyDruhBezOtazky(id, func){
	var result=AjaxMethods.getDataFromGetRequest('/zmaz_cely_slovny_druh/', '?sd_id='+id, '',
		function (r){
			if (r.status==responseOK){//OK vetva
				swal({ buttons: {},
				   title  :  "Úspech",
				   text   :  "Slovný druh bol vymazaný",
				   icon   :  "success"}).then(function(result) {
											if (func) func();
										  });
			} else{
			   swal({ buttons: {},
				   title  :  "Chyba",
				   text   :  r.error_text,
				   icon   :  "error"});
		}

	});
}

function ChybaAkNepodporovanyBrowser(){

	var isOpera=false;
	var isChrome=false;
	var isSafari=false;
	var isFirefox=false;
	var isEdge=false;
	var isIE=false;
	var isUnknown=false;

	if((navigator.userAgent.indexOf("Opera") || navigator.userAgent.indexOf('OPR')) != -1 )
	{
		isOpera = true;
	}
	else if(navigator.userAgent.indexOf("Edge") != -1 )
	{
		isEdge = true;
	}
	else if(navigator.userAgent.indexOf("Chrome") != -1 )
	{
		isChrome = true;
	}
	else if(navigator.userAgent.indexOf("Safari") != -1)
	{
		isSafari = true;
	}
	else if(navigator.userAgent.indexOf("Firefox") != -1 )
	{
		isFirefox = true;
	}
	else if((navigator.userAgent.indexOf("MSIE") != -1 ) || (!!document.documentMode == true )) //IF IE > 10
	{
		isIE = true;
	}
	else
	{
		isUnknown = true;
	}

	if (!isFirefox&&!isEdge&&!isChrome){
		  swal({ buttons: {},
				  title  :  "Chyba",
				  text   :  'Používate nepodporovaný prehliadač. Niektoré časti stránky nemusia korektne fungovať. Podporované sú Google Chrome, Mozilla Firefox a Microsoft Edge',
				  icon   :  "error"})
	}

}

function getCKeditorInstance() {
	var docTitle = document.title;
	var editorInstance = docTitle.split(" ,")[1];
	
	return editorInstance;
}
	
$(document).ready(function(){
	$('ul.dropdown-menu [data-toggle=dropdown]').on('click', function(event) {
		event.preventDefault(); 
		event.stopPropagation(); 
		$(this).parent().parent().find('.dropdown-menu').removeClass('show');
		$(this).parent().find('.dropdown-menu').toggleClass('show');
	});
	
	ChybaAkNepodporovanyBrowser();
});

