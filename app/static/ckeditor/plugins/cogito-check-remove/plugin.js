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
				wrapped.find('span').removeClass('active m n ns no-select').removeAttr('ondblclick onselectstart sdid sd');
				output = wrapped.html();
				
				editor.setData(output);
				
				$('body', parent.document).find('.cke_top.settings-enabled').addClass('settings-disabled').removeClass('settings-enabled');
				
				editor.on( 'selectionChange', function( evt ) {
					var source = this.getCommand( 'source' ),
						save = this.getCommand( 'save' );
						cogito_check = this.getCommand( 'cogito-word-check' );
						cogito_check_remove = this.getCommand( 'cogito-check-remove' );
						cogito_ut = this.getCommand( 'cogito-unit-test' );
						cogito_ut_list = this.getCommand( 'cogito-ut-list' );
						cogito_anotacia = this.getCommand( 'cogito-anotacia' );
						cogito_rozbor = this.getCommand( 'cogito-rozbor' );

					source.enable();
					//save.enable();
					cogito_check.enable();
					cogito_check_remove.disable();
					//cogito_ut.disable();
					//cogito_ut_list.disable();
					//cogito_anotacia.disable();
					//cogito_rozbor.disable();
					
				} );
				editor.on('key', function (e) { 
					e.removeListener();
					$('body', parent.document).find('#setting-new-validation').hide();
				});
				$('#save-context').prop('disabled', false);
			}	
			},
			startDisabled: true		
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
