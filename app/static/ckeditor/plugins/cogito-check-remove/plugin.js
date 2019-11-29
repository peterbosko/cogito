( function() {
	var cogitoCmd = {
		readOnly: 1,
		modes: { wysiwyg: 1,source: 0 },

		exec: function( editor ) {
			if ( editor.fire( 'cogito-check-remove' ) ) {
                var data = {};
				var output = '';
				data.data = editor.getData();
				
				var wrapped = $("<div>" + data.data + "</div>");
				wrapped.find('.settings-rows').remove();
				wrapped.find('span').removeClass('active m n no-select').removeAttr('ondblclick onselectstart');
				output = wrapped.html();
				
				editor.setData(output);
			}	
		}	
	};

	var pluginName = 'cogito-check-remove';

	CKEDITOR.plugins.add( pluginName, {
		// jscs:disable maximumLineLength
		lang: 'af,ar,az,bg,bn,bs,ca,cs,cy,da,de,de-ch,el,en,en-au,en-ca,en-gb,eo,es,es-mx,et,eu,fa,fi,fo,fr,fr-ca,gl,gu,he,hi,hr,hu,id,is,it,ja,ka,km,ko,ku,lt,lv,mk,mn,ms,nb,nl,no,oc,pl,pt,pt-br,ro,ru,si,sk,sl,sq,sr,sr-latn,sv,th,tr,tt,ug,uk,vi,zh,zh-cn', // %REMOVE_LINE_CORE%
		// jscs:enable maximumLineLength
		icons: 'cogito-check-remove', // %REMOVE_LINE_CORE%
		hidpi: true, // %REMOVE_LINE_CORE%
		init: function( editor ) {

			var command = editor.addCommand( pluginName, cogitoCmd );

			editor.ui.addButton && editor.ui.addButton( 'cogito-check-remove', {
				label: 'Zrušiť kontrolu slov',
				command: pluginName,
				toolbar: 'clipboard'
			} );
		}
	});
} )();
