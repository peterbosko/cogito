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
/*
function vrat_tooltip(s, slovo){

    var thtml = "";

    AjaxMethods.getDataFromGetRequest('/vrat_slovo?sid=', s+'&slovo='+slovo, '', function(response){

        var obj = JSON.parse(response.data);

        if (obj){
            var pad = "";

            if (obj.pad){
                pad = "<tr><td>Pád:</td><td>"+ obj.pad +"</td></tr>";
            }

            var tvar = "";

            if (obj.tvar)
                tvar = obj.tvar;

            if (obj.zvratnost)
                tvar += " " + obj.zvratnost;

            var cas = "";

            if (obj.cas)
                cas = "<tr><td>Čas:</td><td>"+ obj.cas +"</td></tr>";

            var zak_tvar = "";

            if (obj.zak_tvar)
                zak_tvar = "<tr><td>Základný tvar:</td><td>"+ obj.zak_tvar +"</td></tr>";

            var id = "";

            if (obj.id)
                id = "<tr><td>Id slova:</td><td>"+ obj.id +"</td></tr>";

            var idsd = "";

            if (obj.sd_id)
                idsd = "<tr><td>Id slov. druhu:</td><td>"+ obj.sd_id +"</td></tr>";

            var rod = "";

            if (obj.rod)
                rod = obj.rod;

            if (obj.podrod)
                rod += " / "+obj.podrod;

            if (rod)
                rod = "<tr><td>Rod/Podrod:</td><td>"+ rod +"</td></tr>";

            var cislo = "";

            if (obj.cislo)
                cislo = "<tr><td>Číslo:</td><td>"+ obj.cislo +"</td></tr>";

            var osoba = "";

            if (obj.osoba)
                osoba = "<tr><td>Osoba:</td><td>"+ obj.osoba +"</td></tr>";

            var negneurprech = "";

            if (obj.je_negacia && obj.je_negacia=="A")
                negneurprech = "Neg"

            if (obj.je_neurcitok && obj.je_neurcitok=="A"){
                if (negneurprech)
                    negneurprech += "/";
                negneurprech += "Neur"
            }

            if (obj.je_prech  && obj.je_prech=="A"){
                if (negneurprech)
                    negneurprech+="/";
                negneurprech += "Prech"
            }

            if (negneurprech)
                negneurprech = "<tr><td>Neg/Neur/Prech:</td><td>"+ negneurprech +"</td></tr>";

            var pricastie = "";

            if (obj.pricastie)
                pricastie = "<tr><td>Príčastie:</td><td>"+ obj.pricastie +"</td></tr>";

            var popis = "";

            if (obj.popis)
                popis = "<tr><td>Popis:</td><td>"+ obj.popis +"</td></tr>";

            var sposob = "";

            if (obj.sposob)
                sposob = "<tr><td>Spôsob:</td><td>"+ obj.sposob +"</td></tr>";

            var anotacia = "";

            if (obj.anotacia)
                anotacia = "<tr><td>Anotácia:</td><td>"+ obj.anotacia +"</td></tr>";

            thtml = "<table>"+
                    "<tr><td style='text-align: center;' colspan='2'><b>"+ tvar +"</b></td></tr>"+
                    "<tr><td>Slovný druh:</td><td>"+ obj.slovny_druh +"</td></tr>"+
                    pad +
                    cas +
                    zak_tvar +
                    cislo +
                    rod +
                    osoba +
                    negneurprech +
                    pricastie +
                    sposob +
                    popis +
                    id +
                    idsd +
                    anotacia +
                    "</table>";
          }
    });
    return thtml;
}

function t(that){
  var sid = $(that).attr('sid');
  var slovo = $(that).text();

  if (sid && sid!="None")
      $(that).tooltip({
        placement: "right",
        title: vrat_tooltip(sid, slovo),
        selector: true,
        html : true,
    });
}
*/

function update_sid(that, row_id){
	var sid = $(that).data('id');
	var new_data = $(that).val();
	
	if(new_data.indexOf(":") >= 0) {
		var data = new_data.split(':');
		console.log(data);
		$('p[data-row-id="'+row_id+'"] span[sid="'+sid+'"]').attr('sid',data[0]);
		$('p[data-row-id="'+row_id+'"] span[sid="'+data[0]+'"]').text(data[1]);
		$('p[data-row-id="'+row_id+'"] span[sid="'+data[0]+'"]').dblclick();
	} else {
		$('p[data-row-id="'+row_id+'"] span[sid="'+sid+'"]').attr('sid',new_data);
		$('p[data-row-id="'+row_id+'"] span[sid="'+new_data+'"]').dblclick();
	}
}

function prev_word(that){
	var row_id = $(that).data('row-id');

	$('#data-row-'+row_id).find('.active').prev().dblclick();
}

function next_word(that){
	var row_id = $(that).data('row-id');
	
	$('#data-row-'+row_id).find('.active').next().dblclick();
}

function accept_word(row_id, sid){
	var el = $('#data-row-'+row_id).find('.active');
	
	if(el.hasClass('s')){
		el.removeClass('s').addClass('m').dblclick();
	} else {
		el.removeClass('m').removeClass('n').addClass('s').next().dblclick();
	}	
}

function load_slovo(that){
	var sid = $(that).attr('sid');
	var slovo = $(that).text();
	var row_id = $(that).parent().data('row-id');
	var data = {};
	var settings_row = $('#row-id-'+row_id);
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
	settings_row.find('.setting-tvar').html('Tvar: ' + slovo + ' | ');
	
	/*** NACITAJ SLOVO DO OBJEKTU ***/
	
	AjaxMethods.getDataFromGetRequest('/vrat_slovo?sid=', sid+'&slovo='+slovo, '', function(response){
		var obj = JSON.parse(response.data);
		console.log('OBJ:');
		console.log(obj);
		if (obj){
			
			/*** NACITAJ VSETKY SLOVNE DRUHY PRE DANE SLOVO ***/
			if(class_type == 's') {
				settings_row.find('.setting-slovny_druh').html('Slovný druh: ' + obj.slovny_druh);
			} else {
				AjaxMethods.getDataFromAsyncGetRequest('/daj_tvary_slova?vyraz='+slovo, "", "", function(r){
					if (r.status==responseOK){
						data = r.data;
						if(data.length > 0) {
							var i;
							options = '<select data-id="'+obj.id+'" onchange="update_sid(this, '+row_id+');">';
							for (i = 0; i < data.length; i++) { 
								var selected = '';
								if (obj.id && obj.id == data[i].id) {
									selected = 'selected=selected';
								}
								options = options + "<option value="+data[i].id+" "+selected+">"+data[i].slovny_druh+" - "+data[i].zak_tvar+"</option>";
							}
							var options = options + '</select> | ';
						}
					}
					settings_row.find('.setting-slovny_druh').html('Slovný druh: ' + options);
				});
			}
			if(obj.slovny_druh == "POD_M") {
				if(obj.rod) {
					settings_row.find('.setting-rod').html('Rod: ' + obj.rod + ' | ');
					if(obj.rod == "M") {
						if(obj.podrod) {
							settings_row.find('.setting-podrod').html('Podrod: ' + obj.podrod + ' | ');
						}	
					}	
				}
				if(obj.vzor) {
					settings_row.find('.setting-vzor').html('Vzor: ' + obj.vzor + ' | ');
				}
				if(obj.prefix) {
					settings_row.find('.setting-prefix').html('Prefix: ' + obj.prefix + ' | ');
				}
				if(obj.sufix) {
					settings_row.find('.setting-sufix').html('Sufix: ' + obj.sufix + ' | ');
				}
				if(obj.pocitatelnost) {
					settings_row.find('.setting-pocitatelnost').html('Pocitatelnost: ' + obj.pocitatelnost + ' | ');
				}
				if(obj.anotacia) {
					settings_row.find('.setting-anotacia').html('Anotácia: ' + obj.anotacia + ' | ');
				}
				if(obj.sem_id) {				

					/*** NACITAJ SEMANTICKY PRIZNAK PRE DANE SLOVO SO SLOVNYM DRUHOM ***/
					
					AjaxMethods.getDataFromAsyncGetRequest('/daj_sem_priznak?sem_id='+obj.sem_id, '', "", function(r){
						if (r.status==responseOK){
							data = r.data;
							console.log('Všetky semanticke priznaky:');
							console.log(data);
							settings_row.find('.setting-priznak_slova').html('Sémantický príznak: ' + data.kod + ' - ' + data.nazov + ' | ');
						}
					});
				}
				
				if(class_type == 's') {
					settings_row.find('.setting-slovny_druh').html('Slovný druh: ' + obj.slovny_druh);
					settings_row.find('.setting-pad').html('Pád: ' + obj.pad);
					settings_row.find('.setting-cislo').html('Číslo: ' + obj.cislo);
					settings_row.find('.setting-odvodene').html('Odvodené od slov: ');
				} else {
					/*** NACITAJ VSETKY PADY PRE DANE SLOVO SO SLOVNYM DRUHOM ***/
					
					AjaxMethods.getDataFromAsyncGetRequest('/daj_vsetky_pady_slova?cislo='+obj.cislo, '&sd_id='+obj.sd_id, "", function(r){
						if (r.status==responseOK){
							data = r.data;
					
							if(data.length > 0) {
								var i;
								options = '<select data-id="'+obj.id+'" onchange="update_sid(this, '+row_id+');">';
								for (i = 0; i < data.length; i++) { 
									var selected = '';
									if (obj.id && obj.pad == data[i].pad) {
										selected = 'selected=selected';
									}
									options = options + "<option value="+data[i].id+":"+data[i].tvar+" "+selected+">"+data[i].pad+" - "+data[i].tvar+"</option>";
								}
								var options = options + '</select> | ';
							}
						}
						settings_row.find('.setting-pad').html('Pád: ' + options);
					});
					
					/*** NACITAJ VSETKY CISLA PRE DANY SLOVNY DRUH ***/
					
					AjaxMethods.getDataFromAsyncGetRequest('/daj_vsetky_cisla_slova?pad='+obj.pad, '&sd_id='+obj.sd_id, "", function(r){
						if (r.status==responseOK){
							data = r.data;
							if(data.length > 0) {
								var i;
								options = '<select data-id="'+obj.id+'" onchange="update_sid(this, '+row_id+');">';
								for (i = 0; i < data.length; i++) { 
									var selected = '';
									if (obj.id && obj.cislo == data[i].cislo) {
										selected = 'selected=selected';
									}
									options = options + "<option value="+data[i].id+":"+data[i].tvar+" "+selected+">"+cislo[data[i].cislo]+"</option>";
								}
								var options = options + '</select> | ';
							}
						}
						settings_row.find('.setting-cislo').html('Číslo: ' + options);
					});
					
					/* CHYBAJU DATA V DB - dorobit prepojenie semantika - slovny druh
					
					AjaxMethods.getDataFromAsyncGetRequest('/daj_odvodene_od_slova?pad='+obj.pad, '&sd_id='+obj.sd_id, "", function(r){
						if (r.status==responseOK){
							data = r.data;
							console.log(data);
							if(data.length > 0) {
								var i;
								options = '<select data-id="'+obj.id+'" onchange="update_sid(this, '+row_id+');">';
								for (i = 0; i < data.length; i++) { 
									var selected = '';
									if (obj.id && obj.cislo == data[i].cislo) {
										selected = 'selected=selected';
									}
									options = options + "<option value="+data[i].id+":"+data[i].tvar+" "+selected+">"+cislo[data[i].cislo]+"</option>";
								}
								var options = options + '</select>';
							}
						}
						settings_row.find('.setting-odvodene').html('Odvodené od slov: ' + from_words);
					});
					*/
				}	
			}
			
			if(class_type == 's') {
				if(obj.popis) {
					settings_row.find('.setting-popis').html('Popis: ' + obj.popis);
				}	
			} else {	
				/*** NACITAJ VSETKY POPISY PRE DANE SLOVO ***/
				
				AjaxMethods.getDataFromAsyncGetRequest('/daj_vsetky_slova?vyraz='+obj.tvar, '', "", function(r){
					if (r.status==responseOK){
						data = r.data;
						console.log('Všetky popisy slova:');
						console.log(data);
						if(data.length > 0) {
							var i;
							var counter = 0;
							options = '<select data-id="'+obj.id+'" onchange="update_sid(this, '+row_id+');">';
							for (i = 0; i < data.length; i++) { 
								var selected = '';
								if (obj.id && obj.id == data[i].id) {
									selected = 'selected=selected';
								}
								//if(data[i].popis) {
									options = options + "<option value="+data[i].id+":"+data[i].tvar+" "+selected+">"+data[i].popis+" - ID: "+data[i].id+"</option>";
									++counter;
								//}
							}
							var options = options + '</select> | ';
						}
						if(counter > 0) {
							settings_row.find('.setting-popis').html('Popis: ' + options);
						}
					}
				});
			}
		}
	});
	settings_row.find('.prev-word').html('<a href="#" onclick="prev_word(this);" data-row-id="'+row_id+'">Predchádzajúce slovo</a>');
	settings_row.find('.next-word').html('<a href="#" onclick="next_word(this);" data-row-id="'+row_id+'">Nasledujúce slovo</a>');
	
	var save_name = 'Potvrdiť slovo';
	if(class_type == 's') {
		save_name = 'Upraviť slovo';
	}
	if(class_type != 'n') {
		settings_row.find('.setting-accept_word').html('<a href="#" onclick="accept_word('+row_id+', '+sid+');" data-row-id="'+row_id+'" style="float: right;">'+save_name+'</a>');
	}
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
                'src' : '/static/js/allJS.min.js'
                }
        });
        var myscript5 = CKEDITOR.document.createElement( 'script', {
            attributes : {
                type : 'text/javascript',
                'src' : '/static/js/main.js?='+Math.random()
                }
        });
		
		var myscript6 = CKEDITOR.document.createElement( 'script', {
            attributes : {
                type : 'text/javascript',
                'src' : '/static/js/jquery.nice-select.min.js'
                }
        });
		
        head.append( myscript1 );
        head.append( myscript5 );
        head.append( myscript6 );
    }

    function GetCKEditorHtml(ckeditorName){
        return CKEDITOR.instances[ckeditorName].getData();
    }

    function initCKEditorInstance(ckeditorName, h, toolbar){

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
		        { name: 'clipboard', items: [ 'Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo', '-', 'cogito-word-check', 'cogito-check-remove', '-' ,'cogito-unit-test' , 'cogito-ut-list' , '-' , 'cogito-anotacia', '-' , 'cogito-rozbor'] },
	        ]
        }
        else {
            tbar = [
        		{ name: 'document', items: [ 'Source' , '-' ,'Save'] },
		        { name: 'clipboard', items: [ 'Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo', '-', 'cogito-word-check', 'cogito-check-remove', '-' ] },
	        ]
        }

        CKEDITOR.replace(ckeditorName, {
          height: h,
          on: {
            instanceReady: function(evt) {
              var itemTemplate = '<li data-id="{id}">' +
                '<div><strong class="item-title">{tvar} - {slovny_druh} ({zak_tvar})</strong></div>' +
                '<div><i>Pád: {pad} Číslo: {cislo} Osoba:{osoba}</i></div>' +
                '<div><i>Stupeň: {stupen} Čas: {cas} Rod:{rod} Podrod:{podrod}</i></div>' +
                '<div><i>Spôsob: {sposob} Zvratnosť: {zvratnost}</i></div>' +
                '<div><i>Anotácia: {anotacia}</i></div>' +
                '<div><i>Popis: {popis}</i></div>' +
                '</li>',
                outputTemplate = '<span class="s" sid="{id}">{tvar}</span>';

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
		  //contentsCss : '/static/css/nice-select.css',
          toolbar: tbar,
		  extraAllowedContent: '*[*]{*}(*)',
		  allowedContent: {
				div: {
					classes: { 'settings-rows': true, 'settings-row': true }
				},
				el: {},
				span: {},
				b: {},
				a: {},
				select: {}
		  },
        });

        CKEDITOR.instances[ckeditorName].CogitoEditorType = toolbar;
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
