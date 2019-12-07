﻿( function() {
	var cogitoCmd = {
		readOnly: 1,
		modes: { wysiwyg: 1,source: 0 },

		exec: function( editor ) {
			if ( editor.fire( 'cogito-ut-list' ) ) {
                var kt_id=$('#kt_id').val();
                if (!kt_id || kt_id == 0){
                    swal({ buttons: {},
                        title  :  "Chyba",
                        text   :  "Najskôr kontext uložte",
                        icon   :  "error"});
                }
                else{
                    loadTemplateIntoLargeScreenModal('#defaultModal','largefitheightscreen', 'Unit testy kontextu', '/zoznam_ut/?kontext_id='+kt_id);
			    }
			}
		},
		startDisabled: true	
	};

	var pluginName = 'cogito-ut-list';

	CKEDITOR.plugins.add( pluginName, {
		// jscs:disable maximumLineLength
		lang: 'af,ar,az,bg,bn,bs,ca,cs,cy,da,de,de-ch,el,en,en-au,en-ca,en-gb,eo,es,es-mx,et,eu,fa,fi,fo,fr,fr-ca,gl,gu,he,hi,hr,hu,id,is,it,ja,ka,km,ko,ku,lt,lv,mk,mn,ms,nb,nl,no,oc,pl,pt,pt-br,ro,ru,si,sk,sl,sq,sr,sr-latn,sv,th,tr,tt,ug,uk,vi,zh,zh-cn', // %REMOVE_LINE_CORE%
		// jscs:enable maximumLineLength
		icons: 'cogito-ut-list', // %REMOVE_LINE_CORE%
		hidpi: true, // %REMOVE_LINE_CORE%
		init: function( editor ) {

			var command = editor.addCommand( pluginName, cogitoCmd );

			editor.ui.addButton && editor.ui.addButton( 'cogito-ut-list', {
				label: 'Zobraziť unit testy',
				command: pluginName,
				toolbar: 'clipboard'
			} );
		}
	});
} )();
