/*
 The function below allows checking the browser's locale using the request's Accept-Language header.
 The value returned is used in order to set the CKAN's locale. Then the function performs a check about
 the cookies info message.
*/
$(document).ready(function(){

    function setSiteLanguage(data) {
      // ///////////////////////////////
      // Do language processing here.
      // ///////////////////////////////

      data = jQuery.parseJSON(data);

      if(data.availableLocales && data.locale){
        var pathArray = location.pathname.split( '/' );

        var localized = false;
        for(locale in data.availableLocales){
          for(path in pathArray){
            if(data.availableLocales[locale] == pathArray[path]){
              localized = true;
              break;
            }
          }
        }  

        if(!localized && !data.isDefaultLocale){
          location.href = location.origin + "/" + data.locale + location.pathname;
        }else{
          cookiesConsentShow();
        }
      }else{
        cookiesConsentShow();
      } 
    };

    function cookiesConsentShow(){
      // //////////////////////////////
      // Do cookies processing here.
      // //////////////////////////////

      var locales = {
        i18n: {
          it:{
            cookieMsg: "Questo sito web utilizza i cookies per erogare servizi di qualità, continuando la navigazione l'utente acconsente al loro utilizzo.",
            cookieAccept: "Accetto",
            cookieMoreInfo: "Ulteriori Informazioni",
            cookieInfoPage: "http://www.retecivica.bz.it/it/cookie.asp"
          },
          de:{
            cookieMsg: "Diese Website verwendet Cookies, um qualitativ hochwertige Dienstleistungen zu liefern, weiter Surfen Sie zu deren Verwendung.",
            cookieAccept: "Akzeptabel",
            cookieMoreInfo: "Weitere Informationen",
            cookieInfoPage: "http://www.buergernetz.bz.it/de/cookie.asp"
          }
        }
      };

      var locale = $('html').attr('lang');
      var messages = locales.i18n[locale];

      cookieChoices.showCookieConsentBar(
          messages.cookieMsg,
          messages.cookieAccept, 
          messages.cookieMoreInfo, 
          messages.cookieInfoPage
      );
    };

    $.ajax({ 
      url: "/loc_status",
      success: function(data, textStatus, jqXHR) {
        setSiteLanguage(data);
      },
      error: function(jqXHR, textStatus, errorThrown) {
      }
    });
    
});