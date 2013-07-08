    dojo.require("esri.widgets");
    dojo.require("esri.layout");
  dojo.require("esri.arcgis.utils");
    dojo.require('esri.map');
    dojo.require('dojo.fx');
    dojo.require('agsjs.dijit.TOC');
  var map, urlObject;
  var i18n;

  function initMap() {
    i18n = dojo.i18n.getLocalization("esriTemplate", "template");

    //Bi-directional language support added to support right-to-left languages like Arabic and Hebrew
    //Note: The map must stay ltr
    dojo.some(["ar","he"], function(l){
      if(dojo.locale.indexOf(l) !== -1){
          configOptions.isRightToLeft = true;
          return true;
      }
    });
    var dirNode = document.getElementsByTagName("html")[0];
    if(configOptions.isRightToLeft){
          dirNode.setAttribute("dir","rtl");
          dojo.addClass( dirNode,"esriRtl");
    }else{
      dirNode.setAttribute("dir","ltr");
      dojo.addClass(dirNode,"esriLtr");
    }


    dojo.byId('footerText').innerHTML = i18n.viewer.footer.label;
    dojo.byId('legendHeader').innerHTML = i18n.viewer.sidePanel.title;
    if (configOptions.geometryserviceurl && location.protocol === "https:") {
      configOptions.geometryserviceurl = configOptions.geometryserviceurl.replace('http:', 'https:');
    }
    esri.config.defaults.geometryService = new esri.tasks.GeometryService(configOptions.geometryserviceurl);
    if (!configOptions.sharingurl) {
      configOptions.sharingurl = location.protocol + '//' + location.host + "/sharing/content/items";
    }
    esri.arcgis.utils.arcgisUrl = configOptions.sharingurl;
    if (!configOptions.proxyurl) {
      configOptions.proxyurl = location.protocol + '//' + location.host + "/sharing/proxy";
    }
    esri.config.defaults.io.proxyUrl = configOptions.proxyurl;
    esri.config.defaults.io.alwaysUseProxy = false;
    urlObject = esri.urlToObject(document.location.href);
    urlObject.query = urlObject.query || {};
    if (configOptions.appid || (urlObject.query && urlObject.query.appid)) {
      var appid = configOptions.appid || urlObject.query.appid;
      var requestHandle = esri.request({
        url: configOptions.sharingurl + "/" + appid + "/data",
        content: {
          f: "json"
        },
        callbackParamName: "callback",
        load: function (response) {
          if (response.values.theme !== undefined) {
            configOptions.theme = response.values.theme;
          }
          if (response.values.webmap !== undefined) {
            configOptions.webmap = response.values.webmap;
          }
          if(response.values.owner !== undefined){
            configOptions.owner = response.values.owner;
          }
          createMap();
        },
        error: function (response) {
          var e = response.message;
          alert(i18n.viewer.errors.createMap + " : " + e);
        }
      });
    } else {
      //not a configured app 
      createMap();
    }
  }

  function createMap() {
    if (urlObject.query.title) {
      configOptions.title = urlObject.query.title;
    }
    if (urlObject.query.subtitle) {
      configOptions.title = urlObject.query.subtitle;
    }
    if (urlObject.query.webmap) {
      configOptions.webmap = urlObject.query.webmap;
    }
    if (urlObject.query.bingMapsKey) {
      configOptions.bingmapskey = urlObject.query.bingMapsKey;
    }
    if (urlObject.query.theme) {
      configOptions.theme = urlObject.query.theme;
    }
    if(urlObject.query.owner){
      configOptions.owner = urlObject.query.owner;
    }
    //add the custom theme
    //load the specified theme 
    var ss = document.createElement("link");
    ss.type = "text/css";
    ss.rel = "stylesheet";
    ss.href = "/static/agol_app/css/" + configOptions.theme + ".css";
    document.getElementsByTagName("head")[0].appendChild(ss);
    var mapDeferred = esri.arcgis.utils.createMap(configOptions.webmap, "map", {
      mapOptions: {
        slider: true,
        nav: false,
        wrapAround180: true
      },
      ignorePopups: false,
      bingMapsKey: configOptions.bingmapskey
    });
    mapDeferred.addCallback(function (response) {
      document.title = configOptions.title || response.itemInfo.item.title;
      dojo.byId("title").innerHTML = configOptions.title || response.itemInfo.item.title;
      dojo.byId("subtitle").innerHTML = configOptions.subtitle || response.itemInfo.item.snippet || "";
      dojo.byId("owner").innerHTML = configOptions.owner || response.itemInfo.item.owner;
      map = response.map;

      if (map.loaded) {
        initUI(response);
      } else {
        dojo.connect(map, "onLoad", function () {
          initUI(response);
        });
      }
      //resize the map when the browser resizes
      dojo.connect(dijit.byId('map'), 'resize', map, map.resize);
    });
    mapDeferred.addErrback(function (error) {
      alert(i18n.viewer.errors.createMap + " : " + error.message);
    });
  }

  function initUI(response) {
    //resize the layout and map to match the specified theme
    dijit.byId('mainWindow').resize();
    map.reposition();
    map.resize();
    //add theme for popup
    dojo.addClass(map.infoWindow.domNode, configOptions.theme);
    //add the scalebar 
    var scalebar = new esri.dijit.Scalebar({
      map: map,
      scalebarUnit: i18n.viewer.main.scaleBarUnits //metric or english
    });
    var layerInfo = esri.arcgis.utils.getLegendLayers(response);
      //legendDiv
    if (layerInfo.length > 0) {
        var legendDijit = new agsjs.dijit.TOC({
            map:map,
            layerInfos: layerInfo
        }, "legendDiv");
        legendDijit.startup();
    } else {
        dojo.byId('legendDiv').innerHTML = i18n.viewer.sidePanel.message;
    }
      /*
    if (layerInfo.length > 0) {
      var legendDijit = new esri.dijit.Legend({
        map: map,
        layerInfos: layerInfo
      }, "legendDiv");
      legendDijit.startup();
    } else {
      dojo.byId('legendDiv').innerHTML = i18n.viewer.sidePanel.message;
    }
    */
  }


