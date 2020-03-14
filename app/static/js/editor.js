/********************* Manage ck editor *****************************/
/********************* Manage ck editor *****************************/
/********************* Manage ck editor *****************************/
/********************* Manage ck editor *****************************/
function initCKEditorInstance(ckeditorName, h, type, settingsToolbar){
	
	CKEDITOR.timestamp = Math.random();
	
	CKEDITOR.addCss('.tooltip > .tooltip-inner { background-color: #000; color:#fff; }');
	
	CKEDITOR.addCss('span.no-select { -webkit-touch-callout: none; -webkit-user-select: none; -khtml-user-select: none; -moz-user-select: none; -ms-user-select: none; user-select: none; }');
	
	CKEDITOR.addCss('span.active { background-color: #afe5ff !important;  padding: 4px;}');
	
	CKEDITOR.addCss('span.no-select:hover { cursor: pointer; }');
	
	CKEDITOR.addCss('span.m { background-color: #ffeec2; }');

	CKEDITOR.addCss('span.n { background-color: #ffaab2; }');

	CKEDITOR.addCss('span.s { background-color: #ffffff; }');
	
	if(settingsToolbar.length > 0) {
		settingsToolbar = settingsToolbar;
	} else {	
		settingsToolbar = getToolbar(ckeditorName, type);
	}	
	
	var tbar = [];

	if (type==="kontext"){
		tbar = [
			{ name: 'document', items: [ 'Source' , '-' ,'Save'] },
			{ name: 'clipboard', items: [ 'Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'cogito-word-check', 'cogito-check-remove', '-' ,'cogito-unit-test' , 'cogito-ut-list' , '-' , 'cogito-anotacia', '-' , 'cogito-rozbor'] },
			'/',
			{ name: 'styles', items: [ 'Styles', 'Format', 'Font', 'FontSize' ] },
		]
	} else {
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
		},
		contentDom : function(event) {
			pripojJavascripty(ckeditorName);
			binduj_tooltip(ckeditorName);
		},
	  },
	  toolbar: tbar,
	  extraAllowedContent: '*[*]{*}(*)',
	});

	CKEDITOR.instances[ckeditorName].CogitoEditorType = type;
	
	CKEDITOR.on('instanceReady',function(){
		$('#cke_'+ckeditorName+' .cke_top').after(settingsToolbar);
	});
}

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

function binduj_tooltip(ckeditorName){
		var all = CKEDITOR.instances[ckeditorName].document.getElementsByTag( 'span' );
		for (var i = 0, max = all.count(); i < max; i++) {
			var el = all.$[i];
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
	var myscript6 = CKEDITOR.document.createElement( 'script', {
		attributes : {
			type : 'text/javascript',
			'src' : '/js/editor.js?='+Math.random()
			}
	});
	
	head.append( myscript1 );
	head.append( myscript5 );
	head.append( myscript6 );
}

function GetCKEditorHtml(ckeditorName){
	return CKEDITOR.instances[ckeditorName].getData();
}


function getToolbar(ckeditorName, type) {
	var settingsToolbar = '';
	
	if(type == 'kontext'){
		settingsToolbar = $('<span id="'+ckeditorName+'-settings-rows" class="cke_top settings-disabled" style="height: 80px; user-select: none;padding: 6px 8px 20px;">'+
							'<span class="cke_voice_label">Settings row</span>'+
							'<span class="cke_toolbox">'+
								'<span class="cke_toolbar cke_toolbar_last">'+
									'<span class="cke_voice_label"></span>'+
									'<span class="cke_toolbar_start"></span>'+
									'<span class="cke_toolgroup">'+
										'<a class="cke_button cke_button__source cke_button_disabled" href="#" title="">'+
											'<span class="cke_button_label cke_button__source_label" style="height: 24px;">'+
												'Gramatika pre tvar <i class="fa fa-long-arrow-alt-right"></i> <b><el class="setting-tvar"></el></b>'+
											'</span>'+
										'</a>'+
										'<a class="cke_button cke_button__source cke_button_disabled" id="'+ckeditorName+'-setting-new-validation" href="#" title="" onClick="return skontroluj_slova_znova(this, \''+ckeditorName+'\');" style="display: none;position: absolute; right: 200px;">'+
											'<span class="cke_button_label cke_button__source_label" style="color: red;font-weight: bold;cursor: pointer;">'+
												'Je potrebná nová validácia <i class="fa fa-redo-alt"></i>'+
											'</span>'+
										'</a>'+
										'<a class="cke_button cke_button__source cke_button_disabled" id="'+ckeditorName+'-setting-legend" href="#" title="" style="position: absolute; right: 30px;">'+
											'<span class="cke_button_label cke_button__source_label" >'+
												'Legenda <i class="fa fa-bars"></i>'+
												'<div class="legend">'+
													'<span style="background-color: #ffeec2;">slovo</span> - nepotvrdené slovo<br />'+
													'<span style="background-color: #ffaab2;">slovo</span> - slovo sa nenachádza v databáze<br />'+
													'<span style="background-color: #afe5ff;">slovo</span> - aktuálne vybraté slovo<br /><br />'+
													
													'<i class="fa fa-angle-left"></i><i class="fa fa-angle-right"></i> - Skok na nasledujúce / predchádzajúce slovo<br>'+
													'<i class="fa fa-angle-double-left"></i><i class="fa fa-angle-double-right"></i> - Skok na nasledujúce / predchádzajúce nepotvrdené slovo<br> '+
													'dvojklik v texte - Výber slova<br>'+
													'Prejdite všetky farebné slová a jednoznačne ich určite'+
												'</div>'+
											'</span>'+
										'</a><br />'+
										
										'<a class="cke_button cke_button__source cke_button_disabled" href="#" title="">'+
											'<span class="cke_button_label cke_button__source_label">'+
												'<el class="setting-slovny_druh"></el>'+
											'</span>'+
										'</a><br />'+
										'<a class="cke_button cke_button__source cke_button_disabled" href="#" title="">'+
											'<span class="cke_button_label cke_button__source_label">'+
												'<el class="setting-odvodene"></el>'+
											'</span>'+
										'</a>'+
									'</span>'+
									'<span class="cke_toolbar_end"></span>'+
								'</span>'+
								'<span class="cke_toolbar_break"></span>'+
							'</span>'+
						'</span>'+
						'<span  id="'+ckeditorName+'-settings-rows-buttons" class="cke_top settings-disabled" style="height: auto; user-select: none;">'+
							'<span class="cke_voice_label">Progress Bar</span>'+
							'<span class="cke_toolbox">'+
								'<div class="progress">'+
									'<div id="'+ckeditorName+'-kontextProgressText" class="progress-bar-text"></div> '+                      
									'<div id="'+ckeditorName+'-kontextProgress" class="progress-bar"></div> '+                      
								'</div>'+
								'<div style="text-align: center;">'+
									'<a href="#" class="btn" onclick="return prev_word(this, \''+ckeditorName+'\');" title="Predchádzajúce slovo"><i class="fa fa-angle-left"></i></a>'+
									'<a href="#" class="btn" onclick="return prev_valid_word(this, \''+ckeditorName+'\');" title="Predchádzajúce nezvalidované slovo"><i class="fa fa-angle-double-left"></i></a>'+
									'<a href="#" class="btn" onclick="return next_valid_word(this, \''+ckeditorName+'\');" title="Nasledujúce nezvalidované slovo"><i class="fa fa-angle-double-right"></i></a>'+
									'<a href="#" class="btn" onclick="return next_word(this, \''+ckeditorName+'\');" title="Nasledujúce slovo"><i class="fa fa-angle-right"></i></a>'+
									'<el class="setting-accept_word"></el>'+
								'</div>'+
								'<div>'+
									
								'</div>'+
							'</span>'+
						'</span>');
	} else {
		settingsToolbar = $('<span id="'+ckeditorName+'-settings-rows" class="cke_top settings-disabled" style="height: 80px; user-select: none;padding: 6px 8px 20px;">'+
								'<span class="cke_voice_label">Settings row</span>'+
								'<span class="cke_toolbox">'+
									'<span class="cke_toolbar cke_toolbar_last">'+
										'<span class="cke_voice_label"></span>'+
										'<span class="cke_toolbar_start"></span>'+
										'<span class="cke_toolgroup">'+
											'<a class="cke_button cke_button__source cke_button_disabled" href="#" title="">'+
												'<span class="cke_button_label cke_button__source_label" style="height: 24px;">'+
													'Popis slova <i class="fa fa-long-arrow-alt-right"></i> <b><el class="setting-popis_slova"></el></b>'+
												'</span>'+
											'</a>'+
										'</span>'+	
										'<span class="cke_toolbar_end"></span>'+
									'</span>'+
									'<span class="cke_toolbar_break"></span>'+
								'</span>'+
							'</span>'+
							'<span  id="'+ckeditorName+'-settings-rows-buttons" class="cke_top settings-disabled" style="height: auto; user-select: none;">'+
								'<span class="cke_toolbox">'+
									'<div style="text-align: center;">'+
										'<a href="#" class="btn" onclick="return prev_word(this, \''+ckeditorName+'\');" title="Predchádzajúce slovo"><i class="fa fa-angle-left"></i></a>'+
										'<a href="#" class="btn" onclick="return prev_valid_word(this, \''+ckeditorName+'\');" title="Predchádzajúce nezvalidované slovo"><i class="fa fa-angle-double-left"></i></a>'+
										'<a href="#" class="btn" onclick="return next_valid_word(this, \''+ckeditorName+'\');" title="Nasledujúce nezvalidované slovo"><i class="fa fa-angle-double-right"></i></a>'+
										'<a href="#" class="btn" onclick="return next_word(this, \''+ckeditorName+'\');" title="Nasledujúce slovo"><i class="fa fa-angle-right"></i></a>'+
										'<a href="#" onclick="return edit_meaning(this, \''+ckeditorName+'\');" class="btn" style="position: absolute; right: 20px;">Upraviť popis slova <i class="fa fa-edit"></i></a>'+
									'</div>'+
									'<div>'+
										
									'</div>'+
								'</span>'+
							'</span>');
	}
	return settingsToolbar;
}
    

/********************* Manage ck editor *****************************/
/********************* Manage ck editor *****************************/
/********************* Manage ck editor *****************************/
/********************* Manage ck editor *****************************/

function update_sid(that, ckeditorName){
	var sid = $(that).data('id');
	var new_data = $(that).val();
	var main = $("#cke_"+ckeditorName+" iframe.cke_wysiwyg_frame").contents();
	
	
	if(new_data.indexOf(":") >= 0) {
		var data = new_data.split(':');
		main.find('span[sid="'+sid+'"].active').attr('sid',data[0]).text(data[1]).dblclick();
	} else {
		main.find('span[sid="'+sid+'"].active').attr('sid',new_data).dblclick();
	}
}

function acceptKontext(that, ckeditorName){
	var data = $('#kontextBody');
	var editor = CKEDITOR.instances[ckeditorName];
	data.find('span').removeClass('m n ns no-select active');
	
	editor.setData(data.html());
	$('#kontextModal').modal('toggle');
}

///////////// WORD NAVIGATION /////////////

function prev_valid_word(that, ckeditorName){
	var main = $("#cke_"+ckeditorName+" iframe.cke_wysiwyg_frame").contents();
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

function next_valid_word(that, ckeditorName){
	var main = $("#cke_"+ckeditorName+" iframe.cke_wysiwyg_frame").contents();
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

function prev_word(that, ckeditorName){
	var main = $("#cke_"+ckeditorName+" iframe.cke_wysiwyg_frame").contents();
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

function next_word(that, ckeditorName){
	var main = $("#cke_"+ckeditorName+" iframe.cke_wysiwyg_frame").contents();
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

///////////// END WORD NAVIGATION /////////////

///////////// WORD FUNCTIONS /////////////

function accept_word(that, ckeditorName){
	var main = $("#cke_"+ckeditorName+" iframe.cke_wysiwyg_frame").contents();
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
			//parent.next().find('span.ns').first().dblclick();
			next_word(that);
		}
	}
	setProgressBar(ckeditorName);
	return false;
}

function add_word(that, is_new, add_new_meaning, ckeditorName){

    add_new_meaning = add_new_meaning || false;

	var main = $("#cke_"+ckeditorName+" iframe.cke_wysiwyg_frame").contents();
	var slovo = '';
	var sdid = '';
	var sd = '';
	var param = '';
	var modal_title = '';

    sd = main.find('.active').attr('sd');


	if(is_new == true && !add_new_meaning) {
		slovo = main.find('.active').html();
		param = '?slovo='+slovo+'&slovnyDruh='+sd;

		loadTemplateIntoModal('#defaultModal', 'Pridanie slova','/pridaj_slovo_vyber_sd/'+param);
	} else {
		sdid = main.find('.active').attr('sdid');
		param = '?sd_id='+sdid+'&slovnyDruh='+sd;

		if (add_new_meaning)
		    param = param+'&ulozAkoNoveSlovo=true';

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
		loadTemplateIntoLargeScreenModal('#defaultModal2', 'largescreen', modal_title,'/zmenit_sd/'+param);
	}
	return false;
}

function edit_sd(that, ckeditorName){
	var main = $("#cke_"+ckeditorName+" iframe.cke_wysiwyg_frame").contents();
	var slovo = '';
	var sdid = '';
	var sd = '';
	var param = '';
	var modal_title = '';

    sd = main.find('.active').attr('sd');

	sdid = main.find('.active').attr('sdid');
	param = '?sd_id='+sdid+'&slovnyDruh='+sd;

    if (sd=="OSTATNE"||
            sd=="CASTICA"||
            sd=="SPOJKA"||
            sd=="PRISLOVKA"||
            sd=="CITOSLOVCE"){
            modal_title = 'Zmeniť slovo iného druhu';
    }
    else if (sd=="POD_M"){
			modal_title = 'Zmeniť podstatné meno';
    }
    else if (sd=="SLOVESO"){
            modal_title = 'Zmeniť sloveso';
    }
    else if (sd=="ZAMENO"){
            modal_title = 'Zmeniť zámeno';
    }
    else if (sd=="CISLOVKA"){
            modal_title = 'Zmeniť číslovku';
    }
    else if (sd=="PRID_M"){
            modal_title = 'Zmeniť prídavné meno';
    }
    else if (sd=="PREDLOZKA"){
            modal_title = 'Zmeniť predložku';
    }
	loadTemplateIntoLargeScreenModal('#defaultModal2', 'largescreen', modal_title,'/zmenit_sd/'+param);
	return false;
}

function edit_meaning(that, ckeditorName){
	var main = $("#cke_"+ckeditorName+" iframe.cke_wysiwyg_frame").contents();
	var slovo = '';
	var sdid = '';
	var sd = '';
	var param = '';
	var modal_title = '';

    sd = main.find('.active').attr('sd');

	sdid = main.find('.active').attr('sdid');
	param = '?sd_id='+sdid+'&slovnyDruh='+sd;
	
	modal_title = 'Upraviť popis slova';
	
	loadTemplateIntoLargeScreenModal('#defaultModal2', 'largescreen', modal_title,'/zmenit_popis/'+param);
	return false;
}

///////////// END WORD FUNCTIONS /////////////

function setProgressBar(ckeditorName){
	var main = $("#cke_"+ckeditorName+" iframe.cke_wysiwyg_frame").contents();
	var progressInfo = $('#'+ckeditorName+'-kontextProgressText');
	var progressBar = $('#'+ckeditorName+'-kontextProgress');
	var uspesnost = 0;
	
	var allWords = main.find('span');
	var allWordsAccepted = main.find('span.s');
	
	uspesnost = Math.round(((allWordsAccepted.length/allWords.length)*100) * 100) / 100;
	
	progressInfo.html(uspesnost+" %");
	progressBar.css("width", uspesnost+"%");
	
	if(uspesnost == 100) {
		var data = {};
		
		$('#'+ckeditorName+'Status').val('V');
		
		data.id=$("#"+ckeditorName+"_kt_id").val();
		data.status = 'V';
		data.nazov = $("#"+ckeditorName+"Name").val();
		data.obsah = CKEDITOR.instances[ckeditorName].getData();
		data.text= CKEDITOR.instances[ckeditorName].document.getBody().getText();
		
		var wrapped = $("<div>" + data.obsah + "</div>");
		wrapped.find('span').removeClass('active m n ns no-select').removeAttr('ondblclick onselectstart sdid sd');
		data.obsah = wrapped.html();
		
		var result=AjaxMethods.getDataFromPostRequest('/pridat_kontext/', '', data,
            function (r){
                if (r.status==responseOK){//OK vetva
                    swal({ buttons: {},
                       title  :  "Úspech",
                       text   :  'Text je na 100% zvalidovaný.',
                       icon   :  "success"}).then(function(result) {
                                                window.location.replace("/moje_kontexty/");

                                              });
                } else {
                   swal({ buttons: {},
                       title  :  "Chyba",
                       text   :  r.error_text,
                       icon   :  "error"});
				}
			}
		);
	} else {
		$('#'+ckeditorName+'Status').val('N');
	}
	return false;
}

function skontroluj_slova_znova(that, ckeditorName) {
	var data = {};
	data.data = CKEDITOR.instances[ckeditorName].getData();
	
	swal({ buttons: {},
		   title  :  "Kontrola",
		   text   :  'Prebieha kontrola textu...',
		   icon   :  "info",
		   closeOnClickOutside : false,
		   closeModal : false,
		   closeOnEsc : false,
		   });
	AjaxMethods.getDataFromAsyncPostRequest('/kontrola_slov/', "", data, function(r){
		if (r.status==responseOK){//OK vetva
			
			CKEDITOR.instances[ckeditorName].setData(r.data.data + '&nbsp;');
			
			$('body', parent.document).find('#'+ckeditorName+'-kontextProgress').css("width", r.data.uspesnost+"%");
			$('body', parent.document).find('#'+ckeditorName+'-kontextProgressText').html(r.data.uspesnost+" %");
			$('body', parent.document).find('#cke_'+ckeditorName+' .cke_top.settings-disabled').addClass('settings-enabled').removeClass('settings-disabled');
			
			setTimeout(function(){
				var all = CKEDITOR.instances[ckeditorName].document.getElementsByTag( 'span' );

				for (var i = 0, max = all.count(); i < max; i++) {
					var el = all.$[i];
					
					el.setAttribute('ondblclick','load_slovo(this, \''+ckeditorName+'\');');
				}
				
				
				
				CKEDITOR.instances[ckeditorName].focus();
				var range = CKEDITOR.instances[ckeditorName].createRange();
				range.moveToElementEditEnd( range.root );
				CKEDITOR.instances[ckeditorName].getSelection().selectRanges( [ range ] );
				
				$('body', parent.document).find('#'+ckeditorName+'-setting-new-validation').hide();
				$('#cke_'+ckeditorName).find('span.m, span.n').first().dblclick();
				swal.close();
			}, 200)	
		} else {
			swal({ buttons: {},
				title  :  "Chyba",
				text   :  r.error_text,
				icon   :  "error"});

		}
	})
	
	return false;
}

function load_slovo(that, active = false, ckeditorName){
	
	if(active == true) {
		var main = $("#cke_"+ckeditorName+" iframe.cke_wysiwyg_frame").contents();
		that = main.find('.active');
	}
	var sid = $(that).attr('sid');
	var slovo = $(that).text();
	var data = {};
	
	var settings_row = $('body', parent.document).find('#'+ckeditorName+'-settings-rows');
	var settings_row_buttons = $('body', parent.document).find('#'+ckeditorName+'-settings-rows-buttons');
	
	settings_row.find('el').html('');
	var cislo = {'J': 'Jednotné', 'M': 'Množné', 'P': 'Pomnožné'};
	var class_type = 's';
	var slovo_sa_v_db_nenachadza = 0;
	
	
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
		var obj = response;
		if (obj.data){
			settings_row.find('.setting-popis_slova').html(obj.data.popis);
			
			/*** AKTUALIZUJ PRIDANE SLOVO ***/
			if(obj.vsetky_slova.length > 0 && class_type == 'n') {
				if(obj.vsetky_slova.length > 1) {
					$(that).removeClass('n').addClass('m');
					class_type = 'm';
				} else {
					$(that).removeClass('n').addClass('s');
					class_type = 's';
					$(that).attr('sid', obj.data.id);
				}
			}
			
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
					options = '<select data-id="'+obj.data.id+'" onchange="update_sid(this, \''+ckeditorName+'\');">';
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
		} else {
			slovo_sa_v_db_nenachadza = 1;
		}
	});
	
	if(slovo_sa_v_db_nenachadza == 1 && active == true) {
		swal({ buttons: {},
				title  :  "Chyba",
				text   :  "Slovo sa v databáze nenachádza.",
				icon   :  "error"});
	}

	var editovat_sd = '<a href="#" onclick="return edit_sd(this, \''+ckeditorName+'\');" class="btn" style="position: absolute; right: 240px;">Editovať v slovníku <i class="fa fa-edit"></i></a>';
	var save_name = '';
	var func = 'accept_word(this, \''+ckeditorName+'\');';

	if(class_type == 's') {
		save_name = 'Upraviť slovo v kontexte <i class="fa fa-edit"></i>';
	} else if(class_type == 'm') {
		save_name = 'Potvrdiť slovo v kontexte <i class="fa fa-check-double"></i>';
	} else {
		save_name = 'Znovu načítaj slovo v kontexte <i class="fa fa-edit"></i>';
		func = 'load_slovo(null, true, \''+ckeditorName+'\');';
	}
	
	settings_row_buttons.find('.setting-accept_word').html('<a href="#" onclick="return '+func+'" class="btn" style="position: absolute; right: 20px;">'+save_name+'</a>');
	
	if(class_type != 'n') {
		settings_row_buttons.find('.setting-accept_word').append(editovat_sd);
		settings_row_buttons.find('.setting-accept_word').append('<a href="#" onclick="return add_word(this, false, true, \''+ckeditorName+'\');" class="btn" style="position: absolute; left: 20px;"><i class="fa fa-plus"></i> Pridať nový význam slova <i class="fa fa-info-circle"></i></a>');
	} else {
		settings_row_buttons.find('.setting-accept_word').append('<a href="#" onclick="return add_word(this, true, false, \''+ckeditorName+'\');" class="btn" style="position: absolute; left: 20px;"><i class="fa fa-plus"></i> Pridať nové slovo</a>');
	}
	
	return false;
}

function ZmenKontext(redirect, ckeditorName){
        var formSelector="#"+ckeditorName+"Form";

        $(formSelector).data('formValidation').validate();
        var formIsVald = $(formSelector).data('formValidation').isValid();

        if (formIsVald) {
            data = {};

            data.id=$("#"+ckeditorName+"_kt_id").val();
            data.nazov=$("#"+ckeditorName+"Name").val();
            data.status=$("#"+ckeditorName+"Status").val();
            data.obsah = CKEDITOR.instances[ckeditorName].getData();
            
			var wrapped = $("<div>" + data.obsah + "</div>");
			wrapped.find('span').removeClass('active m n ns no-select').removeAttr('ondblclick onselectstart sdid sd');
			data.obsah = wrapped.html();
			
			data.text= CKEDITOR.instances[ckeditorName].document.getBody().getText();

            AjaxMethods.getDataFromPostRequest('/pridat_kontext/', "", data, function(r){
                if (r.status==responseOK){//OK vetva
                    swal({ buttons: {},
                       title  :  "Úspech",
                       text   :  "Kontext bol úspešne pridaný/zmenený",
                       icon   :  "success"}).then(function(result) {
                                                    $("#"+ckeditorName+"_kt_id").val(r.data);
                                                    if (redirect)
                                                        window.location.replace("/moje_kontexty/");
                                                  });
                } else{
                    swal({ buttons: {},
                       title  :  "Chyba",
                       text   :  r.error_text,
                       icon   :  "error"});

                }
            });
        }
        else{
            swal({ buttons: {},
                       title  :  "Chyba",
                       text   :  "Chyba validácie. Skontrolujte červené položky",
                       icon   :  "error"});
        }
}