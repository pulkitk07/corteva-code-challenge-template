import unittest
import requests
import json

class TestWeatherAPI(unittest.TestCase):

    def setUp(self):
        self.base_url = 'http://127.0.0.1:5000/api/weather'


    def test_get_weather_by_date(self):
        # Test getting weather data by date
        response = requests.get(self.base_url + '?date=19850102')
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.text)
        self.assertGreater(len(results), 0)
        for result in results:
            self.assertEqual(result['date'], '19850102')
        
        

    def test_get_weather_by_station_ID(self):
        # Test getting weather data by station ID
        response = requests.get(self.base_url + '?station_id=1')
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.text)
        self.assertGreater(len(results), 0)
        for result in results:
            self.assertEqual(result['station_id'], 1)


    def test_get_weather_stats_by_station_ID(self):
        # Test getting weather data by station ID
        response = requests.get(self.base_url + '/stats?station_id=1')
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.text)
        self.assertGreater(len(results), 0)
        for result in results:
            self.assertEqual(result['station_id'], 1)


if __name__ == '__main__':
    unittest.main()
