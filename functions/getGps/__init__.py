import logging
from io import BytesIO
from PIL import Image
import azure.functions as func
import PIL.ExifTags as ExifTags


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('start.')

    if req.method == 'POST':
        logging.info(req.get_body())
        im = Image.open(BytesIO(req.get_body()))

        # exifからGPS情報を取得する
        exif = im._getexif()
        for k, v in exif.items():
            if k in ExifTags.TAGS:
                gps_tag = ExifTags.TAGS[k]

                if gps_tag == 'GPSInfo':
                    # 緯度経度の計算をする
                    lat_deg, lat_min, lat_sec = v[2][0], v[2][1], v[2][2]
                    latitude_n = lat_deg + (lat_min / 60.0) + (lat_sec / 3600.0)

                    lon_deg, lon_min, lon_sec = v[4][0], v[4][1], v[4][2]
                    longitude_e = lon_deg + (lon_min / 60.0) + (lon_sec / 3600.0)

                    # "緯度, 軽度" の形にデータ整形
                    logging.info(str(latitude_n) + ', ' + str(longitude_e))
                    return func.HttpResponse(str(latitude_n) + ', ' + str(longitude_e))

                else:
                    return func.HttpResponse('This image did not have GPS info in exif', status_code=500)

    else:
        logging.warning('not arrowed method. ' + req.method)
        return func.HttpResponse(
            'not arrowed method. ' + req.method,
            status_code=403
        )
