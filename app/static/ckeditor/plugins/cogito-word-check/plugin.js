( function() {
	var cogitoCmd = {
		readOnly: 1,
		modes: { wysiwyg: 1,source: 0 },

		exec: function( editor ) {
			if ( editor.fire( 'cogito-word-check' ) ) {
                var data = {};
                data.data = editor.getData();
				
                swal({ buttons: {},
                       title  :  "Kontrola",
                       text   :  'Prebieha kontrola textu...',
                       icon   :  "info",
                       closeOnClickOutside : false,
                       closeModal : false,
                       closeOnEsc : false,
                       // <div class="fa-3x"><i class="fas fa-spinner fa-spin"></i></div>
                       // not working now html : true
                       });

                AjaxMethods.getDataFromAsyncPostRequest('/kontrola_slov/', "", data, function(r){
                    if (r.status==responseOK){//OK vetva
                        swal.close();
                        swal({ buttons: {},
                            title  :  "Úspech",
                            text   :  "Kontext bol skontrolovaný. Miera zvalidovaných slov: " + r.data.uspesnost+" %",
                            icon   :  "success"});
                        editor.setData(r.data.data);
						
						setTimeout(function(){
							var all = editor.document.getElementsByTag( 'span' );

							for (var i = 0, max = all.count(); i < max; i++) {
								var el = all.$[i];
								
								el.setAttribute('ondblclick','load_slovo(this);');
								el.setAttribute('onselectstart','return false;');
							}	
						}, 200)	
                    } else{
                        swal({ buttons: {},
                            title  :  "Chyba",
                            text   :  r.error_text,
                            icon   :  "error"});

                    }
                });
			}
		}
	};

	var pluginName = 'cogito-word-check';

	CKEDITOR.plugins.add( pluginName, {
		// jscs:disable maximumLineLength
		lang: 'af,ar,az,bg,bn,bs,ca,cs,cy,da,de,de-ch,el,en,en-au,en-ca,en-gb,eo,es,es-mx,et,eu,fa,fi,fo,fr,fr-ca,gl,gu,he,hi,hr,hu,id,is,it,ja,ka,km,ko,ku,lt,lv,mk,mn,ms,nb,nl,no,oc,pl,pt,pt-br,ro,ru,si,sk,sl,sq,sr,sr-latn,sv,th,tr,tt,ug,uk,vi,zh,zh-cn', // %REMOVE_LINE_CORE%
		// jscs:enable maximumLineLength
		icons: 'cogito-word-check', // %REMOVE_LINE_CORE%
		hidpi: true, // %REMOVE_LINE_CORE%
		init: function( editor ) {

			var command = editor.addCommand( pluginName, cogitoCmd );

			editor.ui.addButton && editor.ui.addButton( 'cogito-word-check', {
				label: 'Kontrola slov',
				command: pluginName,
				toolbar: 'clipboard'
			} );
		}
	});
} )();
