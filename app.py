import csv

class HealthcarePlanMarketplace:
    """ Class representing the marketplace for healthcare plans. """

    def __init__(self, zipCodeFile, planFile):
        self.zipCodeToRateArea = self.mapZipCodeToRateArea(zipCodeFile)        
        self.planData = self.mapPlanToRateArea(planFile)


    def readCSV(self, filepath):
        with open(filepath, mode='r') as infile:
            reader = csv.DictReader(infile)
            return [row for row in reader]        


    def mapZipCodeToRateArea(self,zipCodeFile):
        """ Create mapping from zipcode to the corresponding rate area.
        This function needs to handle multiple entries (rate_areas) per zipcode. 
        Example return array
        {
           "36749": [
            {"rate_area": "11","state": "AL","county_code": "01001","name": "Autauga"},
            {"rate_area": "13","state": "AL","county_code": "01047","name": "Dallas"}]
        } """        
        zipCodeData = self.readCSV(zipCodeFile)  
        zipCodeToRateArea = {}
        for row in zipCodeData:
            entry = {
                'rate_area': row['rate_area'],
                'state': row['state'],
                'county_code': row['county_code'],
                'name': row['name']
            }

            if row['zipcode'] in zipCodeToRateArea:
                # Append to existing list if the zipcode already has an entry
                zipCodeToRateArea[row['zipcode']].append(entry)
            else:
                # Create a new entry
                zipCodeToRateArea[row['zipcode']] = [entry]           

        return zipCodeToRateArea


    def mapPlanToRateArea(self, planFile):
        """ Create mapping from rateArea, state and metalLevel to rate.
        This function uses a simple mapping for each row in the input file. """
        return self.readCSV(planFile)


    def getAreaRate(self,zipCode):
        """ Return area rate for a given zip code. 

        A ZIP code can potentially be in more than one county. 
        If the county can not be determined definitively by the ZIP code, 
        it may still be possible to determine the rate area for that ZIP code. 
        ??

        A ZIP code can also be in more than one rate area. 
        In that case, the answer is ambiguous and should be left blank. 
        
        The function first gets a list of entries using the zip code,
        from the zipCodeToRateArea map.
        The happy path example, we would have a single entry 
         [{'rate_area': '3', 'state': 'MO', 'county_code': '29095', 'name': 'Jackson'}]
        in this case, we return 3

        or, multiple entries with a common rate_area         
            [{'rate_area': '4', 'state': 'KS', 'county_code': '20051', 'name': 'Ellis'},
             {'rate_area': '4', 'state': 'KS', 'county_code': '20141', 'name': 'Osborne'},
             {'rate_area': '4', 'state': 'KS', 'county_code': '20163', 'name': 'Rooks'}, 
             {'rate_area': '4', 'state': 'KS', 'county_code': '20167', 'name': 'Russell'}]
        in this case, we return 4

        The ambiguous path would be cause by multiple entries, with different rate_area values
            [{'rate_area': '15', 'state': 'WI', 'county_code': '55047', 'name': 'Green Lake'}, 
            {'rate_area': '11', 'state': 'WI', 'county_code': '55137', 'name': 'Waushara'}, 
            {'rate_area': '11', 'state': 'WI', 'county_code': '55139', 'name': 'Winnebago'}]
        in this case (and similar variations), we return None.

        The multiple entries handling takes care of the zip in more than on county. """     
        entries = self.zipCodeToRateArea.get(zipCode)

        if entries is None:
            return None  # zipcode not found

        # Check if all entries have the same state and rate_area
        if all(entry['rate_area'] == entries[0]['rate_area'] and
               entry['state'] == entries[0]['state'] for entry in entries):
            # All entries have the same state and rate_area
            return entries[0]['rate_area'], entries[0]['state']
        else:
            # Different rate_areas or states found, return None for ambiguity
            return None

         
    def getPlans(self, rateArea, state, metalLevel):
        """ returns all plan rates for a given rate area, state and metal level.
        Example return data
        [{"plan_id": "78421VV7272023","state": "MO","metal_level": "Silver","rate": "290.05","rate_area": "3"},
         {"plan_id": "35866RG6997149","state": "MO","metal_level": "Silver","rate": "234.6","rate_area": "3"},
         {"plan_id": "28850TB6621800","state": "MO","metal_level": "Silver","rate": "265.82","rate_area": "3"},]
        """
        return [plan for plan in self.planData 
                if plan['rate_area'] == rateArea and 
                state == plan['state'] and plan['metal_level'] == metalLevel]
               

    def determineSLCSP(self,zipCode):
        """ determine the second lowest cost silver plan (SLCSP) for a ZIP code.
        This function first gets the state and rate area for a given zipcode.
        Then gets the compatible plans for the zipcode and state, sorts them,
        and return the second lowest. """
        result = self.getAreaRate(zipCode)
        if result is None:
            return None

        rateArea, state = result
        plans = self.getPlans(rateArea, state, 'Silver')

        # Sort plans by rate and return the second lowest cost rate plan 
        sorted_plans = sorted(plans, key=lambda x: float(x['rate']))
        return sorted_plans[1]['rate'] if len(sorted_plans) >= 2 else None           


def main():
    zipCodeFile = 'zips.csv'
    planFile = 'plans.csv'
    customerZipCodes = 'slcsp.csv'

    hpm = HealthcarePlanMarketplace(zipCodeFile,planFile)
    
    # Buffered reader of zip codes
    with open(customerZipCodes, mode='r') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            zipcode = row['zipcode']
            rate = hpm.determineSLCSP(zipcode)            
            rate = '' if rate is None else rate            
            print(f"{zipcode},{rate}")


if __name__ == "__main__":
    main()