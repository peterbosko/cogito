( function() {
	var cogitoCmd = {
		readOnly: 1,
		modes: { wysiwyg: 1,source: 0 },

		exec: function( editor ) {
			var ckeditorName = editor.name;
			if ( editor.fire( 'cogito-rozbor' ) ) {
                loadTemplateIntoModal('#defaultModal','Rozbor viet kontextu', '/rozbor_viet_kontextu/');
				$('#strukturaVety').data('editor-id', ckeditorName);
				
				var data = {};
				
				data.kontext = CKEDITOR.instances[ckeditorName].getData();

				AjaxMethods.getDataFromPostRequest('/vyrob_stromy_viet/', "", data, function(r){
					if (r.status==responseOK){//OK vetva
						$('#jsTree').jstree({ 'core' : {
							'data' : r.data
							}
						});
						$('#jsTree').on("dblclick.jstree", function (e) {
							var instance = $.jstree.reference(this),
							node = instance.get_node(e.target);
							var poradieVety = node.id.replace('veta_','');
							if (!poradieVety.includes('_')){
									d = {};
									d.kontext = CKEDITOR.instances[ckeditorName].getData();
									d.veta = poradieVety;
									AjaxMethods.getDataFromPostRequest('/vyrob_popis_struktury_vety/', "", d, function(r){
										if (r.status==responseOK){//OK vetva
											$('#strukturaVety').removeClass('nodisplay');
											$('#taStrukturaVety').val(r.data);
										} else{
											swal({ buttons: {},
											   title  :  "Chyba",
											   text   :  r.error_text,
											   icon   :  "error"});
										}
									});
							}
						});
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

	var pluginName = 'cogito-rozbor';

	CKEDITOR.plugins.add( pluginName, {
		// jscs:disable maximumLineLength
		lang: 'af,ar,az,bg,bn,bs,ca,cs,cy,da,de,de-ch,el,en,en-au,en-ca,en-gb,eo,es,es-mx,et,eu,fa,fi,fo,fr,fr-ca,gl,gu,he,hi,hr,hu,id,is,it,ja,ka,km,ko,ku,lt,lv,mk,mn,ms,nb,nl,no,oc,pl,pt,pt-br,ro,ru,si,sk,sl,sq,sr,sr-latn,sv,th,tr,tt,ug,uk,vi,zh,zh-cn', // %REMOVE_LINE_CORE%
		// jscs:enable maximumLineLength
		icons: 'cogito-rozbor', // %REMOVE_LINE_CORE%
		hidpi: true, // %REMOVE_LINE_CORE%
		init: function( editor ) {

			var command = editor.addCommand( pluginName, cogitoCmd );

			editor.ui.addButton && editor.ui.addButton( 'cogito-rozbor', {
				label: 'Rozbor viet',
				command: pluginName,
				toolbar: 'clipboard'
			} );
		}
	});
} )();
