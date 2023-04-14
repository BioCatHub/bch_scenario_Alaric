import libcombine
import pandas as pd
import numpy as np


class PrimaryDataExtractor:

    def __init__(self, path, column):
        self.path = path
        self.column = column

        '''
        Parameters
        ----------
        Path: String
            Path to the xlsx file containing the measurement data
        '''


    def build_dataframe(self):

        '''
        Builds a dataframe for every measurement based on an array of reference and sample data

        Parameters
        ----------
        None

        Returns
        -------
        measurement_dataframe: DataFrame
            Data frame containing:
            x_values: time in minutes
            refenrence : absorption data
            sample: absorption data
        '''

        samples = self.extract_data_from_xlsx()
        x_values = self.extract_x_values()
        result = pd.concat([x_values, samples], axis=1)
        return result


    def extract_data_from_xlsx(self):

        '''
        Extracts the measurement values from the input excel file. The refence and sample values are arranged by the spectrometer in one list.

        Parameters
        ----------
        column_name: Name of the column in which the data is listed

        Returns
        -------
        data_frame_measurements: DataFrame containing the reference and measurement data sets
        '''

        df = pd.read_excel(r"data/Mappe11.xlsx")
        df_cleared = df.drop(df.columns[[0,1]], axis=1)
        dff = df_cleared.drop([0,1])
        column3 = dff[self.column]
        #print(column3)
        arcl3 = np.array(column3)
        n = arcl3.size
        m = n/3
        column_before_divide = arcl3.reshape((42, 3))
        column_reshaped = column_before_divide
        array_sample = []
        array_reference = []

        for i in range(42):
            if i%2 == 0:
                array_sample.append(column_reshaped[i])
            else:
                array_reference.append(column_reshaped[i])

        newarray = np.array(array_sample)
        newarray_reference = np.array(array_reference)
        df_test = pd.DataFrame(newarray, columns=['ref1', 'ref2', 'ref3'])
        df_test1 = pd.DataFrame(newarray_reference, columns=['sample1', 'sample2', 'sample3'])
    
        dff_final = pd.concat([df_test,df_test1], axis=1)

        return dff_final


    def extract_x_values(self):

        '''
        Extracts the x_values from the excel file.

        Parameters
        ----------
        None

        Returns
        data_frame_x_values = Dataframe containting time values
        '''

        df = pd.read_excel(r"data/Mappe1.xlsx")

        x_values = df["Column1"]
        x_values_cleared = x_values.dropna()
        array = np.array(x_values_cleared)

        time = array[5]

        x_values_time = []

        for i in array:
            minutes = i.minute*60
            seconds = i.second
            #print((minutes+seconds)/60)
            x_values_time.append((minutes+seconds)/60)
        
        df_x_values = pd.DataFrame(x_values_time, columns=["x_values"])

        return df_x_values


new = PrimaryDataExtractor("any", "Column1")
new.build_dataframe()


