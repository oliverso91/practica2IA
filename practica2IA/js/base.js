var dominio = 'http://localhost:3000/';
//var baseUrl    = Dominio+ ':4000/';
var nombre    = getCookie('api-nombre');
var rol    = getCookie('api-rol');


function get(url, param) {
    var url_string = url;
    var url = new URL(url_string);
    var param = url.searchParams.get(param);
    return param;

}
