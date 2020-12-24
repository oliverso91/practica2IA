$(document).ready(function () {
cuerpo = []
});

$(document).on('ready', function() {
     $("#input-7").fileinput({
        uploadUrl: "Upload.php" // server upload action
        , autoReplace: true
        , showCaption: true
        , showUpload: true
        , showPreview: true
        , maxFileCount: 10
        , mainClass: "input-group-lg"
        , allowedPreviewTypes: ['text', 'image']
        , uploadExtraData: function () {  // callback example

            var documentos = [];

            $.each($(this)[0].filenames, function (i, v) {
                var nombre = v;
                //Busco la extension
                var lastPoint = nombre.lastIndexOf(".");
                var extension = nombre.substring(lastPoint + 1);

                var b;
                switch (extension.toUpperCase()) {
                    case "JPG":
                    case "PNG":
                    case "JPEG":
                        b = {
                            'id': i + 1,
                            'nombre': nombre,
                            'mensaje': '',
                            'tipo': extension.toUpperCase(),
                            'procesado': false
                        };
                        documentos.push(b);
                        break;
                    default:
                        b = {
                            'id': i + 1,
                            'nombre': nombre,
                            'mensaje': msgWrongFileType,
                            'tipo': extension.toUpperCase(),
                            'procesado': false
                        };
                        documentos.push(b);
                        break;
                }
            });

            //Recorro todos los xmls y pdfs, los que no tenga par se marcaran como bad
            $.each(xml, function (i, v) {
                if (v.tienePar == false) {
                    v.mensaje = msgNoPdf;
                    //bad.push(v);
                }
            });


            var data = {
                Documentos: documentos
                , DatoExtra: "Informacion EXTRA"
            }

            alert(JSON.stringify(data));
            return { datos: JSON.stringify(data) }; //Este objeto mandarias al SERVER al presionar upload
          }
        });


});

$('#input-7').on('filebatchpreupload', function (event, data) {
    //Si quieres que haga algo antes de enviar la informacion
    $("#divResult").text("Enviando...");
});

//Para procesar los archivos despues de haberlos subido
$('#input-7').on('filebatchuploadsuccess', function (event, data) {
    var response = data.response;
    $("#divResult").text("Procesados...");
    //Despues de procesare la informacion el server respondera con esto... puedes decidir que hacer.. ya se mostrar un mensaje al usuairo
});

$('#input-7').on('filecleared', function () {
    //Si queires que haga algo al limpiar los archivos
    alert('0 archivos');
});

$("#generar").on('click', function () {


  var images = document.getElementsByTagName('img');
  base = new Array();
  nombre  = new Array();
  var datos  = [];
  var objeto = {};
  for(var i = 0; i < images.length; i++) {
      if(i % 2 == 0){

            base[i]  = images[i].src
            nombre[i] = images[i].title
            //console.log(base[i]);
            //srcList.push('{"base": "p'+images[i].title + '", "nombre" : "' + images[i].title + '"}');
      }

   }
  // console.log(base);

   for(var i= 0; i < nombre.length; i++) {

       //var nombre = nombre[i];
       if (!(i in nombre)) {
           console.log("esta vacio");
       }
       else {

         datos.push({
              "nombre"    : nombre[i],
              "base"  : base[i]
          });

       }

   }


   objeto = datos;
   //console.log(JSON.stringify(objeto));
 enviardata(JSON.stringify(objeto));
});


/////////////////////enjvio de imagenes

function enviardata(datos) {

  data     = datos;

  $.ajax({
          type: 'POST',
          url:  "http://localhost:5000/cuerpo",
          contentType: "application/json",
          dataType: 'json',
          crossDomain: true,
          async: false,
          data: data,
          success: function (data) {

                //console.log(data);

          }
      });
}
