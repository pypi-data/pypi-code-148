import os
from Shynatime import ShTime
from haversine import haversine, Unit
from ShynaDatabase import Shdatabase


# cron : Add to cron job
class UpdateDistanceSpeed:
    s_data = Shdatabase.ShynaDatabase()
    s_time = ShTime.ClassTime()
    result = []
    latitude_List = []
    longitude_list = []
    count = []
    time_list = []

    def update_distance_with_haversine(self):
        try:
            home = self.get_home_coordinates()
            self.s_data.default_database = os.environ.get('location_db')
            self.s_data.query = "SELECT count, new_time, new_latitude, new_longitude FROM shivam_device_location where " \
                                "status = 'False' order by count DESC"
            self.result = self.s_data.select_from_table()
            for item in self.result:
                self.count.append(item[0])
                self.time_list.append(item[1])
                self.latitude_List.append(item[2])
                self.longitude_list.append(item[3])
            for i in range(len(self.count) - 1):
                # print(self.count[i])
                distance_difference = haversine(point1=(float(self.latitude_List[i]), float(self.longitude_list[i])),
                                                point2=(
                                                    float(self.latitude_List[i + 1]),
                                                    float(self.longitude_list[i + 1])),
                                                unit=Unit.METERS)
                time_diff = (self.s_time.string_to_time_with_date(
                    self.time_list[i]) - self.s_time.string_to_time_with_date(self.time_list[i + 1])).seconds
                speed = distance_difference / time_diff
                speed_km = 3.6 * float(speed)
                if str(home).lower().__eq__('false'):
                    hom_dis = 0.0
                else:
                    hom_dis = haversine(point2=(float(home[0]), float(home[1])),point1=(float(self.latitude_List[i]),
                                                                                        float(self.longitude_list[i])),
                                        unit=Unit.KILOMETERS)
                # print(distance_difference, time_diff, speed)
                self.s_data.query = "UPDATE shivam_device_location SET shivam_distance_from_previous='" \
                                    + str(distance_difference) + "' , shivam_speed='" + str(speed) + \
                                    "', shivam_speed_in_km='" + str(speed_km) + "' ,diff_from_home='" + str(hom_dis) + \
                                    "' ,status='True' WHERE count='" + str(self.count[i]) + "';"
                print(self.s_data.query)
                self.s_data.create_insert_update_or_delete()
        except Exception as e:
            print(e)
            pass

    def get_home_coordinates(self):
        try:
            self.s_data.default_database = os.environ.get('location_db')
            self.s_data.query = "Select latitude, longitude from shivam_standard_location_long_lat where " \
                                "loc_name='boss home'"
            self.result = self.s_data.select_from_table()
            if str(self.result[0]).lower().__eq__('empty'):
                return False
            else:
                print(self.result[0])
                return self.result[0]
        except Exception as e:
            print(e)


if __name__ == '__main__':
    UpdateDistanceSpeed().update_distance_with_haversine()
