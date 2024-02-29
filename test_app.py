import unittest
from unittest.mock import patch, mock_open
from app import HealthcarePlanMarketplace

class TestHealthcarePlanMarketplace(unittest.TestCase):

    mock_zip_data = [
        {'zipcode': '12345', 'rate_area': '1', 'state': 'TX', 'county_code': '001', 'name': 'Harris'},
        {'zipcode': '12345', 'rate_area': '1', 'state': 'TX', 'county_code': '002', 'name': 'Dallas'},
    ]

    mock_plan_data = [
        {'plan_id': 'plan1', 'state': 'TX', 'metal_level': 'Silver', 'rate': '100', 'rate_area': '1'},
        {'plan_id': 'plan2', 'state': 'TX', 'metal_level': 'Silver', 'rate': '200', 'rate_area': '1'},
        {'plan_id': 'plan3', 'state': 'TX', 'metal_level': 'Gold', 'rate': '300', 'rate_area': '2'},
        {'plan_id': 'plan4', 'state': 'CA', 'metal_level': 'Silver', 'rate': '400', 'rate_area': '1'},        
    ]


    @patch('app.HealthcarePlanMarketplace.readCSV')
    def test_initialization_and_mapping(self, mock_readCSV):
        """Check HealthcarePlanMarketplace class is initialized correctly and
        both zipCodeToRateArea and planData have been mapped correctly."""
        # Mock data for each call of readCSV
        mock_readCSV.side_effect = [self.mock_zip_data, self.mock_plan_data]
        
        # Instantiate with dummy file paths
        hpm = HealthcarePlanMarketplace('dummy_zip.csv', 'dummy_plan.csv')
        
        # Test zipCodeToRateArea mapping
        zip_result = hpm.zipCodeToRateArea['12345']
        # Check if two entries are mapped to zipcode '12345'
        self.assertEqual(len(zip_result), 2)  
        # Check the state of the first entry
        self.assertEqual(zip_result[0]['state'], 'TX')  
        
        # Test planData mapping
        # check if planData matches mock_plan_data
        self.assertEqual(len(hpm.planData), len(self.mock_plan_data))
        for plan in self.mock_plan_data:
            self.assertIn(plan, hpm.planData)


    @patch('app.HealthcarePlanMarketplace.readCSV')
    def test_getAreaRate(self, mock_readCSV):
        """ Test getAreaRate returns correct rateArea and state """
        # mock data for each call of readCSV
        mock_readCSV.side_effect = [self.mock_zip_data, self.mock_plan_data]

        # Instantiate with dummy file paths
        hpm = HealthcarePlanMarketplace('dummy_zip.csv', 'dummy_plan.csv')

        # Check correct rateArea and state returned for zipcode
        rateArea, state = hpm.getAreaRate('12345')
        self.assertEqual(rateArea, '1')
        self.assertEqual(state, 'TX')


    @patch('app.HealthcarePlanMarketplace.readCSV')
    def test_getPlans(self, mock_readCSV):
        """Test the getPlans method filters plan rates correctly for a given rate area, state, and metal level."""
        mock_readCSV.side_effect = [self.mock_zip_data, self.mock_plan_data]
        
        # Instantiate with dummy file paths
        hpm = HealthcarePlanMarketplace('dummy_zip.csv', 'dummy_plan.csv')
        
        # Testing for TX, rate area 1, Silver plans
        silver_plans_tx = hpm.getPlans('1', 'TX', 'Silver')
        
        # Check that we get the correct plans back
        self.assertEqual(len(silver_plans_tx), 2)
        self.assertTrue(all(plan['state'] == 'TX' for plan in silver_plans_tx))
        self.assertTrue(all(plan['metal_level'] == 'Silver' for plan in silver_plans_tx))
        self.assertTrue(all(plan['rate_area'] == '1' for plan in silver_plans_tx))
        
        # Check the rates to ensure correct plans are returned
        rates = [plan['rate'] for plan in silver_plans_tx]
        self.assertIn('100', rates)
        self.assertIn('200', rates)
    

    @patch('app.HealthcarePlanMarketplace.readCSV')
    def test_determineSLCSP(self, mock_readCSV):
        """Test the determineSLCSP method returns the second lowest cost Silver plan rate for a given ZIP code."""
        # Setup mock data for ZIP code mappings and plan data
        mock_readCSV.side_effect = [self.mock_zip_data, self.mock_plan_data]
        
        # Instantiate the class with dummy file paths
        hpm = HealthcarePlanMarketplace('dummy_zip.csv', 'dummy_plan.csv')
        
        # the expected rate area and state for the given ZIP code (from mock_zip_data)
        expected_rate_area = '1'
        expected_state = 'TX'
        
        # expected plans that match the rateArea, state and metal_level (from mock_plan_data)
        expected_plans = [
            {'plan_id': 'plan1', 'state': 'TX', 'metal_level': 'Silver', 'rate': '100', 'rate_area': '1'},
            {'plan_id': 'plan2', 'state': 'TX', 'metal_level': 'Silver', 'rate': '200', 'rate_area': '1'}
        ]
        
        # Sort plans by rate to determine the expected second lowest cost
        expected_plans_sorted = sorted(expected_plans, key=lambda x: float(x['rate']))
        expected_slcsp_rate = expected_plans_sorted[1]['rate']
        
        # Call determineSLCSP with the test zipcode
        actual_slcsp_rate = hpm.determineSLCSP('12345')
        
        # Check the returned rate matches the expected second lowest cost
        self.assertEqual(actual_slcsp_rate, expected_slcsp_rate)    


if __name__ == '__main__':
    unittest.main()