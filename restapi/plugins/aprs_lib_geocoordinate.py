import decimal

class GeoCoordinateTools:

    @classmethod
    def decimal_to_aprs(cls, lat_dec, lon_dec):
        lat=cls._format_aprs(lat_dec, 'lat')
        lon=cls._format_aprs(lon_dec, 'lon')

        return (lat, lon)

    @classmethod
    def _format_aprs(cls, value_dec, type='lat'):
        coordinate_dec=decimal.Decimal(value_dec)
        coordinate_deg=int(coordinate_dec)
        coordinate_dec_places=(coordinate_dec-coordinate_deg)*60
        if type=='lat':
            orientation='N'
        elif type=='lon':
            orientation='E'

        result=format(f"{coordinate_dec_places:0.2f}")
        if len(result)==4:
            result=f"0{result}"

        result=f"{coordinate_deg}{result}{orientation}"
        if coordinate_deg < 100 and type=='lon':
            result=f"0{result}"

        return result


