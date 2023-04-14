import libcombine
import pandas as pd
import numpy as np
import re


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
        #result = pd.concat([x_values, samples], axis=1)
        #return result


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

        df = pd.read_csv(r"Thermo plate reader/ABTS_reaction.csv", delimiter=r';')
        
        rows_deleted = df.drop(df.index[0:4])
        first_column = rows_deleted["Column2"]
        na_cleared = first_column.dropna()
        na_deleted = first_column.dropna()

        text = "Interation"

        list= []

        for i in na_deleted:
            test = re.search("^Iteration", i)
            if test:
                pass
            elif test==None:
                list.append(i)
            else:
        #        except Exception as error:
                    print("sorting error")
                    raise
            
        liste1 = list[0:180]

        array = np.array(liste1)

        reshaped = array.reshape((60, 3))

        #print(reshaped)

        array_sample = []
        array_reference = []

        for i in range(60):
            if i%2 == 0:
                array_sample.append(reshaped[i])
            else:
                array_reference.append(reshaped[i])

        newarray = np.array(array_sample)
        newarray_reference = np.array(array_reference)
        df_test = pd.DataFrame(newarray, columns=['ref1', 'ref2', 'ref3'])
        df_test1 = pd.DataFrame(newarray_reference, columns=['sample1', 'sample2', 'sample3'])

        df_concat = pd.concat([df_test, df_test1], axis=1)

        print(df_concat)

        
            
        



    def extract_x_values(self):

        '''
        Extracts the x_values from the excel file.

        Parameters
        ----------
        None

        Returns
        data_frame_x_values = Dataframe containting time values
        '''

        x_values = []
        for i in range(30):

            if len(x_values) == 0:
                x_values.append(0)
            elif len(x_values) != 0:
                last_value = x_values[i-1]
                x_values.append(last_value+1.5)

        
        df_x_values = pd.DataFrame(x_values, columns=["x_values"])
        print(df_x_values)



new = PrimaryDataExtractor("Thermo plate reader/ABTS_reaction.csv", "columns")
new.build_dataframe()