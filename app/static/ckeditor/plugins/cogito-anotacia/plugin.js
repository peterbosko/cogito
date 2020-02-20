function copyToClipboard(text){
  const el = document.createElement('textarea');
  el.value = text;
  document.body.appendChild(el);
  el.select();
  document.execCommand('copy');
  document.body.removeChild(el)
}

( function() {
	var cogitoCmd = {
		readOnly: 1,
		modes: { wysiwyg: 1,source: 0 },

		exec: function( editor ) {
			if ( editor.fire( 'cogito-anotacia' ) ) {
                var data = {};
                data.data = editor.getData();
                AjaxMethods.getDataFromAsyncPostRequest('/dopln_anotaciu/', "", data, function(r){
                    copyToClipboard(r.data);
                    if (r.status==responseOK){//OK vetva
                        swal({ buttons: {},
                            title  :  "Úspech",
                            text   :  "Anotovaný text bol skopírovaný do klipboardu",
                            icon   :  "success"});
                    } else{
                        swal({ buttons: {},
                            title  :  "Chyba",
                            text   :  r.error_text,
                            icon   :  "error"});

                    }
                });

			}
		},
		startDisabled: false	
	};

	var pluginName = 'cogito-anotacia';

	CKEDITOR.plugins.add( pluginName, {
		// jscs:disable maximumLineLength
		lang: 'af,ar,az,bg,bn,bs,ca,cs,cy,da,de,de-ch,el,en,en-au,en-ca,en-gb,eo,es,es-mx,et,eu,fa,fi,fo,fr,fr-ca,gl,gu,he,hi,hr,hu,id,is,it,ja,ka,km,ko,ku,lt,lv,mk,mn,ms,nb,nl,no,oc,pl,pt,pt-br,ro,ru,si,sk,sl,sq,sr,sr-latn,sv,th,tr,tt,ug,uk,vi,zh,zh-cn', // %REMOVE_LINE_CORE%
		// jscs:enable maximumLineLength
		icons: 'cogito-anotacia', // %REMOVE_LINE_CORE%
		hidpi: true, // %REMOVE_LINE_CORE%
		init: function( editor ) {

			var command = editor.addCommand( pluginName, cogitoCmd );

			editor.ui.addButton && editor.ui.addButton( 'cogito-anotacia', {
				label: 'Skopírovať anotáciu do klipboardu',
				command: pluginName,
				toolbar: 'clipboard'
			} );
		}
	});
} )();
