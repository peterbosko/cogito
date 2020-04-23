var supportsES6 = function() {
  try {
    new Function("(a = 0) => a");
    return true;
  }
  catch (err) {
    return false;
  }
}();

function ChybaAkNepodporovanyBrowser(){

	if (!supportsES6){
		  swal({ buttons: {},
				  title  :  "Chyba",
				  text   :  'Váš internetový prehliadač nepodporuje ES6 špecifikáciu javascriptu. Niektoré veci nemusia korektne fungovať !',
				  icon   :  "error"})
	}
	else{
	    //alert('podporovany browser');
	}

}
