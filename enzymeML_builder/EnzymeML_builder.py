import libcombine 
import pandas as pd
#from primary_data_extractor import PrimaryDataExtractor
import json
from enzymeML_builder.primary_data_extractor_thermo import PrimaryDataExtractor


class EnzymeMLBuilder(PrimaryDataExtractor):

    def __init__(self, path, column, concentration):
        self.concentration = concentration
        super().__init__(path, column)

    
    
    def build_measurements_list(self):
        
        measurements_list = []

        #measurement_references = self.annotate_measurement(self.build_measurement("ref"), "reference")
        #measurement_samples = self.annotate_measurement(self.build_measurement("sample"), "samples")

        measurement_references = self.annotate_measurement(self.build_measurement("ref"), "samples")
        measurement_samples = self.annotate_measurement(self.build_measurement("sample"), "reference")
        

        measurements = {"measurements":[measurement_references, measurement_samples]}

        json_template = open("biocathub-import.json",)
        template = json.load(json_template)

        template["enzymes"][0]["reaction"]["educts"][0]["concentration"] = self.concentration
        print(template)


        json_file = {}

        '''
        json_file["title"] = "test"
        json_file["vessel"] = {"type":"96 well plate", "volume":"100", "unit":"uL", "others":[]}
        json_file["experimentalData"] = measurements
        '''
        template["title"] = "test"
        template["vessel"] = {"type":"96 well plateeeeeee", "volume":"100", "unit":"uL", "others":[]}
        template["experimentalData"] = measurements
        with open("biocathub.json", "w") as outfile:
            bch_model_json = json.dumps(template)
            outfile.write(bch_model_json)

        archive=libcombine.CombineArchive()
        archive.addFile("./biocathub.json", "biocathub.json",libcombine.KnownFormats_lookupFormat("json"))
        archive.writeToFile("A540nm/AlaricnoEnzml"+str(self.concentration)+"mmolL.omex")

        
    
    
    def extract_dataframe(self):
        data = self.build_dataframe()
        #print(data)
        return data

    def build_measurement(self, name):
        
        measurement_dataframe = self.extract_dataframe()
        measurements = []
        measurement = {}
        replicates = []

        x_values_df = measurement_dataframe["x_values"]
        x_values = x_values_df.to_list()
        references = measurement_dataframe[[name+"1",name+"2",name+"3"]]
        dat = references.iloc[:, 0]
        for i in x_values:
            #print("data", i)
            replicate = {}
            replicate["x_value"] = i
            y_values = []


            for j in range(3):
                data = references.iloc[:, j]
                index = x_values.index(i)
                insert = data[index]
                y_values.append(insert)
            replicate["y_values"] = y_values
            replicates.append(replicate)

        measurement["replicates"] = replicates

        return measurement

    def annotate_measurement(self, measurement, sample):


        measurement["x_unit"] = "s"
        measurement["x_name"] = "time"
        measurement["y_unit"] = "A540"
        measurement["y_name"] = "Absorption"
        measurement["plotStyle"] = "point"
        measurement["reagent"] = "ABTS"
        measurement["notes"] = sample

        return measurement


        #experiment1["experimentalData"] = measurements


columns = ["Column3", "Column4","Column5","Column6"]
concentrations = [0, 1,2,3]

for i, j in zip(columns, concentrations):

    data = EnzymeMLBuilder("j", i, j).build_measurements_list()