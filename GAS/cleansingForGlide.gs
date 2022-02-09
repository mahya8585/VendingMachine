function onRecordRow(e){
  const [timeStamp, imgUrl, description] = e.values;
  const getGpsUrl = "GPSを取得するAzure logic appのAPI URL";

  //GPS情報のクレンジング
  var data = {"url": imgUrl};
  var payload = JSON.stringify(data);
  var options = {
    "method" : "POST",
    "contentType" : "application/json",
    "payload" : payload
  };

  var place = UrlFetchApp.fetch(getGpsUrl, options);
  Logger.log(place);

  //Glideデータシートの最終行を取得
  var sheet = SpreadsheetApp.getActiveSpreadsheet();
  var target = sheet.getSheetByName("glide-data");
  var columnVals = target.getRange("A:A").getValues(); 
  const lastRow = String((columnVals.filter(String).length + 1).toFixed(0));

  if(place.getResponseCode() == 200){
    //Glideデータの書き込み(GPS取得できた時)
    var range = target.getRange("A"+lastRow +":D"+lastRow);
    range.setValues([[timeStamp,imgUrl,description,String(place)]]);

  } else {
    //Glideデータの書き込み(GPS取得できなかった時)
    var range = target.getRange("A"+lastRow +":E"+lastRow);
    range.setValues([[timeStamp,imgUrl,description,"35, 139",String(place) + String(place.getResponseCode())]]);
  }
}
