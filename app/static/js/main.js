var responseOK=1;
var responseERROR=2;

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

function update_sid(that){
	var sid = $(that).data('id');
	var new_data = $(that).val();
	var main = $("iframe.cke_wysiwyg_frame").contents();
	
	
	if(new_data.indexOf(":") >= 0) {
		var data = new_data.split(':');
		main.find('span[sid="'+sid+'"].active').attr('sid',data[0]).text(data[1]).dblclick();
	} else {
		main.find('span[sid="'+sid+'"].active').attr('sid',new_data).dblclick();
	}
}

function acceptKontext(that){
	var data = $('#kontextBody');
	var editor = CKEDITOR.instances['txtContext'];
	data.find('span').removeClass('m n ns no-select active');
	
	editor.setData(data.html());
	$('#kontextModal').modal('toggle');
}

function prev_valid_word(that){
	var main = $("iframe.cke_wysiwyg_frame").contents();
	var prev = main.find('.active').prevAll('.ns').eq(0);
	var parent = main.find('.active').parent();
	if(prev.length) {
		prev.dblclick();
	} else {
		var prevp = parent.prevAll('p');
		for (i = 0; i < prevp.length; i++) {      
			 if (prevp.eq(i).find('span.ns').last().length) {
				  prevp.eq(i).find('span.ns').last().dblclick();
				  break;
			 }
		}
	}
	return false;
}

function next_valid_word(that){
	var main = $("iframe.cke_wysiwyg_frame").contents();
	var next = main.find('.active').nextAll('.ns').eq(0);
	var parent = main.find('.active').parent();
	if(next.length) {
		next.dblclick();
	} else {
		var nextp = parent.nextAll('p');
		for (i = 0; i < nextp.length; i++) {      
			 if (nextp.eq(i).find('span.ns').first().length) {
				  nextp.eq(i).find('span.ns').first().dblclick();
				  break;
			 }
		}
	}
	return false;
}

function prev_word(that){
	var main = $("iframe.cke_wysiwyg_frame").contents();
	var prev = main.find('.active').prevAll('span').eq(0);
	var parent = main.find('.active').parent();
	if(prev.length) {
		prev.dblclick();
	} else {
		var prevp = parent.prevAll('p');
		for (i = 0; i < prevp.length; i++) {      
			 if (prevp.eq(i).find('span').last().length) {
				  prevp.eq(i).find('span').last().dblclick();
				  break;
			 }
		}
	}
	return false;
}

function next_word(that){
	var main = $("iframe.cke_wysiwyg_frame").contents();
	var next = main.find('.active').nextAll('span').eq(0);
	var parent = main.find('.active').parent();
	if(next.length) {
		next.dblclick();
	} else {
		var nextp = parent.nextAll('p');
		for (i = 0; i < nextp.length; i++) {      
			 if (nextp.eq(i).find('span').first().length) {
				  nextp.eq(i).find('span').first().dblclick();
				  break;
			 }
		}
	}
	return false;
}

function accept_word(that){
	var main = $("iframe.cke_wysiwyg_frame").contents();
	var el = main.find('.active');
	
	if(el.hasClass('s')){
		el.removeClass('s').addClass('m').dblclick();
	} else {
		el.removeClass('m n ns').addClass('s');
		var next = main.find('.active').nextAll('.ns').eq(0);
		var parent = main.find('.active').parent();
		if(next.length) {
			next.dblclick();
		} else {
			parent.next().find('span.ns').first().dblclick();
		}
	}
	setProgressBar();
	return false;
}

function add_word(that, is_new){
	var main = $("iframe.cke_wysiwyg_frame").contents();
	var slovo = '';
	var sdid = '';
	var sd = '';
	var param = '';
	var modal_title = '';
	
	if(is_new == true) {
		slovo = main.find('.active').html();
		param = '?slovo='+slovo;
		loadTemplateIntoModal('#defaultModal', 'Pridanie slova','/pridaj_slovo_vyber_sd/'+param);
	} else {
		sdid = main.find('.active').attr('sdid');
		sd = main.find('.active').attr('sd');
		param = '&sd_id='+sdid;
		if (sd=="OSTATNE"||
            sd=="CASTICA"||
            sd=="SPOJKA"||
            sd=="PRISLOVKA"||
            sd=="CITOSLOVCE"){
            modal_title = 'Pridať slovo iného druhu';
        }
        else if (sd=="POD_M"){
			modal_title = 'Pridať podstatné meno';
        }
        else if (sd=="SLOVESO"){
            modal_title = 'Pridať sloveso';
        }
        else if (sd=="ZAMENO"){
            modal_title = 'Pridať zámeno';
        }
        else if (sd=="CISLOVKA"){
            modal_title = 'Pridať číslovku';
        }
        else if (sd=="PRID_M"){
            modal_title = 'Pridať prídavné meno';
        }
        else if (sd=="PREDLOZKA"){
            modal_title = 'Pridať predložku';
        }
		loadTemplateIntoLargeScreenModal('#defaultModal2', 'largescreen', modal_title,'/zmenit_sd/?pridavanyDruh='+sd+param);
	}
	
}

function setProgressBar(){
	var main = $("iframe.cke_wysiwyg_frame").contents();
	var progressInfo = $('#kontextProgressText');
	var progressBar = $('#kontextProgress');
	var uspesnost = 0;
	
	var allWords = main.find('span');
	var allWordsAccepted = main.find('span.s');
	
	uspesnost = Math.round(((allWordsAccepted.length/allWords.length)*100) * 100) / 100;
	
	progressInfo.html(uspesnost+" %");
	progressBar.css("width", uspesnost+"%");
}

function load_slovo(that){
	var sid = $(that).attr('sid');
	var slovo = $(that).text();
	var data = {};
	
	var settings_row = $('body', parent.document).find('#settings-rows');
	var settings_row_buttons = $('body', parent.document).find('#settings-rows-buttons');
	
	settings_row.find('el').html('');
	var cislo = {'J': 'Jednotné', 'M': 'Množné', 'P': 'Podmnožné'};
	var class_type = 's';
	
	
	
	if($(that).hasClass('m')) {
		class_type = 'm';
	} else if($(that).hasClass('n')) {
		class_type = 'n';
	}
	
	$('span').removeClass('active');
	$(that).addClass('active');
	
	var options;
	settings_row.find('.setting-tvar').html(slovo);
	
	/*** NACITAJ SLOVO DO OBJEKTU ***/
	
	AjaxMethods.getDataFromGetRequest('/daj_komplet?sid=', sid+'&vyraz='+slovo, '', function(response){
		//console.log(response);
		var obj = response;
		if (obj.data){
			/*** NACITAJ VSETKY SLOVA PRE DANE SLOVO ***/
			if(class_type == 's') {
				var slovo_data = '';
				if(obj.data.pad) {
					slovo_data += ", PÁD: "+obj.data.pad;
				}
				if(obj.data.cislo) {
					slovo_data += ", ČÍSLO: "+cislo[obj.data.cislo];
				}
				if(obj.data.osoba) {
					slovo_data += ", OSOBA: "+obj.data.osoba;
				}
				if(obj.data.stupen) {
					slovo_data += ", STUPEŇ: "+obj.data.stupen;
				}
				if(obj.data.cas) {
					slovo_data += ", ČAS: "+obj.data.cas;
				}
				if(obj.data.rod) {
					slovo_data += ", ROD: "+obj.data.rod;
				}
				if(obj.data.podrod) {
					slovo_data += ", PODROD: "+obj.data.podrod;
				}
				if(obj.data.sposob) {
					slovo_data += ", SPÔSOB: "+obj.data.sposob;
				}
				if(obj.data.zvratnost) {
					slovo_data += ", ZVRATNOSŤ: "+obj.data.zvratnost;
				}
				if(obj.data.anotacia) {
					slovo_data += ", ANOTÁCIA: "+obj.data.anotacia;
				}
				if(obj.data.popis) {
					slovo_data += ", POPIS: "+obj.data.popis;
				}
				
				settings_row.find('.setting-slovny_druh').html("Slovný druh: "+obj.data.slovny_druh+", "+obj.data.tvar+" ("+obj.data.zak_tvar+")"+ slovo_data + "");
			} else {
				
				if(obj.vsetky_slova.length > 0) {
					var i;
					options = '<select data-id="'+obj.data.id+'" onchange="update_sid(this);">';
					for (i = 0; i < obj.vsetky_slova.length; i++) { 
						var selected = '';
						var slovo_data = '';
						
						if (obj.data.id && obj.data.id == obj.vsetky_slova[i].id) {
							selected = 'selected=selected';
						}
						
						if(obj.vsetky_slova[i].pad) {
							slovo_data += ", PÁD: "+obj.vsetky_slova[i].pad;
						}
						if(obj.vsetky_slova[i].cislo) {
							slovo_data += ", ČÍSLO: "+cislo[obj.vsetky_slova[i].cislo];
						}
						if(obj.vsetky_slova[i].osoba) {
							slovo_data += ", OSOBA: "+obj.vsetky_slova[i].osoba;
						}
						if(obj.vsetky_slova[i].stupen) {
							slovo_data += ", STUPEŇ: "+obj.vsetky_slova[i].stupen;
						}
						if(obj.vsetky_slova[i].cas) {
							slovo_data += ", ČAS: "+obj.vsetky_slova[i].cas;
						}
						if(obj.vsetky_slova[i].rod) {
							slovo_data += ", ROD: "+obj.vsetky_slova[i].rod;
						}
						if(obj.vsetky_slova[i].podrod) {
							slovo_data += ", PODROD: "+obj.vsetky_slova[i].podrod;
						}
						if(obj.vsetky_slova[i].sposob) {
							slovo_data += ", SPÔSOB: "+obj.vsetky_slova[i].sposob;
						}
						if(obj.vsetky_slova[i].zvratnost) {
							slovo_data += ", ZVRATNOSŤ: "+obj.vsetky_slova[i].zvratnost;
						}
						if(obj.vsetky_slova[i].anotacia) {
							slovo_data += ", ANOTÁCIA: "+obj.vsetky_slova[i].anotacia;
						}
						if(obj.vsetky_slova[i].popis) {
							slovo_data += ", POPIS: "+obj.vsetky_slova[i].popis;
						}
						
						options = options + "<option value="+obj.vsetky_slova[i].id+" "+selected+">"+obj.vsetky_slova[i].slovny_druh+", "+obj.vsetky_slova[i].tvar+" ("+obj.vsetky_slova[i].zak_tvar+")"+slovo_data+"</option>";
					}
					options = options + '</select>';
					settings_row.find('.setting-slovny_druh').html('Slovný druh: ' + options);
				}
			}
			
			if(obj.odvodene.length > 0) {
				var i;
				var from_words = '';
				for (i = 0; i < obj.odvodene.length; i++) { 
					from_words = from_words + obj.odvodene[i].parent_sd.zak_tvar+" ("+obj.odvodene[i].parent_sd.popis+")";
					if((i+1) < obj.odvodene.length) {
						from_words += ", ";
					}
				}
				settings_row.find('.setting-odvodene').html('Odvodené od slov: <b>' + from_words + '</b>');
			}
			$(that).attr('sdid', obj.data.sd_id);
			$(that).attr('sd', obj.data.slovny_druh);
		}
	});
	
	var save_name = 'Potvrdiť slovo <i class="fa fa-check-double"></i>';
	if(class_type == 's') {
		save_name = 'Upraviť slovo <i class="fa fa-edit"></i>';
	}
	if(class_type != 'n') {
		settings_row_buttons.find('.setting-accept_word').html('<a href="#" onclick="accept_word(this);" class="btn" style="position: absolute; right: 20px;">'+save_name+'</a>');
		settings_row_buttons.find('.setting-accept_word').append('<a href="#" onclick="add_word(this, false);" class="btn" style="position: absolute; left: 200px;"><i class="fa fa-plus"></i> Pridať nový význam slova <i class="fa fa-info-circle"></i></a>');
	} else {
		settings_row_buttons.find('.setting-accept_word').html('');
	}
	//$('select').niceSelect();

}

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


/********************* Manage ck editor *****************************/
/********************* Manage ck editor *****************************/
/********************* Manage ck editor *****************************/
/********************* Manage ck editor *****************************/
    function textTestCallback(range) {
      if (!range.collapsed) {
        return null;
      }
		return CKEDITOR.plugins.textMatch.match(range, matchCallback);
    }

    function matchCallback(text, offset) {
      var pattern = /([a-zA-Z\u00C0-\u024F\u1E00-\u1EFF])*$/,
        match = text.slice(0, offset)
        .match(pattern);

      if (!match) {
        return null;
      }

      return {
        start: match.index,
        end: offset
      };
    }

    function dataCallback(matchInfo, callback) {
      var data = {};

      var vyraz=matchInfo.query;

      var presna_zhoda="N";

      if (vyraz.endsWith("#")){
          //presna_zhoda = "A";
          vyraz = vyraz.substr(0,vyraz.length-1);
      }

      AjaxMethods.getDataFromAsyncGetRequest('/daj_tvary_slova?', "vyraz="+vyraz+"&presna_zhoda="+presna_zhoda, "", function(r){
            if (r.status==responseOK){//OK vetva
                data = r.data;
                callback(data);
            }
      });
    }

    function binduj_tooltip(ckeditorName){
            var all = CKEDITOR.instances[ckeditorName].document.getElementsByTag( 'span' );
            for (var i = 0, max = all.count(); i < max; i++) {
                var el = all.$[i];
				//el.setAttribute('onmouseover','t(this);');
				//el.classList.remove("m");
				//el.classList.remove("n");
				//el.classList.remove("active");
            }
	}
	
	function load_sematicke_pady(ckeditorName) {
		/*** NACITAJ SEMANTICKY PAD PRE DANE SLOVO ***/
		var all = CKEDITOR.instances[ckeditorName].document.getElementsByTag( 'span' );
		for (var i = 0, max = all.count(); i < max; i++) {
			var el = all.$[i];
			var sid = el.getAttribute('sid');
			if(sid) {
				AjaxMethods.getDataFromAsyncGetRequest('/daj_sem_pad?sid='+sid, '', "", function(r){
					if (r.status==responseOK){
						var data = r.data;
						console.log(sid);
						console.log(data);
						/*if(data.kod) {
							$(el).tooltip({
								placement: "top",
								title: data.kod,
								selector: true,
								html : true,
							});
						}*/
					}
				});
			}		
		}		
	}

    function pripojJavascripty(ckeditorName){
        var head = CKEDITOR.instances[ckeditorName].document.getHead();
        var myscript1 = CKEDITOR.document.createElement( 'script', {
            attributes : {
                type : 'text/javascript',
                'src' : '/js/allJS.min.js'
                }
        });
        var myscript5 = CKEDITOR.document.createElement( 'script', {
            attributes : {
                type : 'text/javascript',
                'src' : '/js/main.js?='+Math.random()
                }
        });
		
        head.append( myscript1 );
        head.append( myscript5 );
    }

    function GetCKEditorHtml(ckeditorName){
        return CKEDITOR.instances[ckeditorName].getData();
    }

    function initCKEditorInstance(ckeditorName, h, toolbar, settingsToolbar){

		CKEDITOR.timestamp=Math.random();
        
		CKEDITOR.addCss('.tooltip > .tooltip-inner { background-color: #000; color:#fff; }');
		
		CKEDITOR.addCss('span.no-select { -webkit-touch-callout: none; -webkit-user-select: none; -khtml-user-select: none; -moz-user-select: none; -ms-user-select: none; user-select: none; }');
        
		CKEDITOR.addCss('span.active { background-color: #afe5ff !important;  padding: 4px;}');
        
		CKEDITOR.addCss('span.no-select:hover { cursor: pointer; }');
		
		CKEDITOR.addCss('span.m { background-color: #ffeec2; }');

        CKEDITOR.addCss('span.n { background-color: #ffaab2; }');

        CKEDITOR.addCss('span.s { background-color: #ffffff; }');
		
        var tbar = [];

        if (!toolbar){
            toolbar = "kontext";
        }

        if (toolbar==="kontext"){
            tbar = [
        		{ name: 'document', items: [ 'Source' , '-' ,'Save'] },
		        { name: 'clipboard', items: [ 'Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'cogito-word-check', 'cogito-check-remove', '-' ,'cogito-unit-test' , 'cogito-ut-list' , '-' , 'cogito-anotacia', '-' , 'cogito-rozbor'] },
				'/',
				{ name: 'styles', items: [ 'Styles', 'Format', 'Font', 'FontSize' ] },
			]
        }
        else {
            tbar = [
        		{ name: 'document', items: [ 'Source' , '-' ,'Save'] },
		        { name: 'clipboard', items: [ 'Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'cogito-word-check', 'cogito-check-remove', '-' ] },
	        ]
        }
		var info = '<p style="color:red">Pre určenie slova kliknite na jeden zaznam zo zoznamu:</p>';
        CKEDITOR.replace(ckeditorName, {
          height: h,
          on: {
            instanceReady: function(evt) {
              var itemTemplate = '<li data-id="{id}"><span>Pre určenie slova kliknite na jeden zaznam zo zoznamu:</span>' +
                '<div><strong class="item-title">{tvar} - {slovny_druh} ({zak_tvar})</strong></div>' +
                '<div><i>Pád: {pad} Číslo: {cislo} Osoba:{osoba}</i></div>' +
                '<div><i>Stupeň: {stupen} Čas: {cas} Rod:{rod} Podrod:{podrod}</i></div>' +
                '<div><i>Spôsob: {sposob} Zvratnosť: {zvratnost}</i></div>' +
                '<div><i>Anotácia: {anotacia}</i></div>' +
                '<div><i>Popis: {popis}</i></div>' +
                '</li>',
                outputTemplate = '<span class="s" sid="{id}">{tvar}</span>&nbsp;';

              var autocomplete = new CKEDITOR.plugins.autocomplete(evt.editor, {
                textTestCallback: textTestCallback,
                dataCallback: dataCallback,
                itemTemplate: itemTemplate,
                outputTemplate: outputTemplate
              });

              // Override default getHtmlToInsert to enable rich content output.
              autocomplete.getHtmlToInsert = function(item) {
				  
                return this.outputTemplate.output(item);
              }
            },
            contentDom : function(event) {
                pripojJavascripty(ckeditorName);
                binduj_tooltip(ckeditorName);
                //load_sematicke_pady(ckeditorName);
            },
          },
          toolbar: tbar,
		  extraAllowedContent: '*[*]{*}(*)',
        });

        CKEDITOR.instances[ckeditorName].CogitoEditorType = toolbar;
		
		CKEDITOR.on('instanceReady',function(){
			$('#cke_1_top').after(settingsToolbar);
		});
		
		
    }

/********************* Manage ck editor *****************************/
/********************* Manage ck editor *****************************/
/********************* Manage ck editor *****************************/
/********************* Manage ck editor *****************************/

function nahrad_zobaky(str){
    return str.replace(/</g,"&lt;").replace(/>/g,"&gt;");
}
/*
function bindSlovesoAutocomplete(selector) {
    $(selector).select2({
        minimumInputLength: 1,
        allowClear: true,
        initSelection: function (element, callback) {
            var data = { id: element.val(), text: 'aaa' };
            callback(data);
        },
        ajax: {
            url: "/daj_autocomplete_slovies",
            dataType: 'json',
            quietMillis: 100,
            data: function (params) {
                var page = params.page;
                if (page == null) page = 1;
                return {
                    term: params.term,
                    onPage: 10,
                    page: page
                };
            },
            processResults: function (data, params) {
                var more = false;
                var x = {
                    "data": []
                };
                var i = 0;

                $.each(data.data, function (index, obj) {
                    x.data[i] = { id: obj.Id, text: obj.Name };
                    i++;
                    more = (params.page * 10) < obj.TotalResults;
                });

                return { results: x.data, more: more };
            }
        },
        escapeMarkup: function (m) { return m; } // we do not want to escape markup since we are displaying html in results
    });
}
*/

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
