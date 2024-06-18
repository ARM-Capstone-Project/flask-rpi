from models.sensors.temperature import Temperature

class TemperatureController:
    def get_all_records():
        return Temperature.get_all_records()

    def get_single_record(id):
        return Temperature.get_single_record(id)

    def create_record(data):
        return Temperature.create_record(data)
