import numpy as np
import pandas as pd


class MultipleSelection():
    def multiple_selection_other(self, df_raw, column_number, number_of_options, question_number):
        df = df_raw[column_number]

        df = pd.DataFrame(df)
        df[0] = df[column_number].str.split(',')
              # 0 is column name

        for i in range(number_of_options):
            df[i + 1] = 0

        df[0][1:] = df[0][1:].map(self.strip_space)

        ls_elm = []
        for index in df.iloc[1:, 1]:
            try:
                for elm in index:
                    if elm not in ls_elm:
                        ls_elm.append(elm)
            except:
                pass
        ls_elm.insert(0, '')

        for index in range(df.shape[0]):
            try:
                for elm in df.iloc[index + 1, 1]:
                    num_elm = ls_elm.index(elm)
                    if num_elm >= number_of_options:
                        df.iloc[index + 1, number_of_options + 1] += 1
                    else:
                        df.iloc[index + 1, num_elm + 1] += 1
            except:
                pass

        ls_elm[0] = 0

        for _ in range(number_of_options, len(ls_elm)):
            ls_elm.pop(number_of_options)

        ls_elm.insert(number_of_options, 'その他')
        ls_elm.insert(0, question_number)

        df.columns = ls_elm

        df = df.drop(0, axis=1)

        return df


    def multiple_selection(self, df_raw, column_number, number_of_options, question_number):
            df = df_raw[column_number]

            df = pd.DataFrame(df)
            df[0] = df[column_number].str.split(',')

            for i in range(number_of_options):
                df[i + 1] = 0

            df[0][1:] = df[0][1:].map(self.strip_space)

            ls_elm = []
            for index in df.iloc[1:, 1]:
                try:
                    for elm in index:
                        if elm not in ls_elm:
                            ls_elm.append(elm)
                except:
                    pass
            ls_elm.insert(0, '')

            for index in range(df.shape[0]):
                try:
                    for elm in df.iloc[index + 1, 1]:
                        num_elm = ls_elm.index(elm)
                        df.iloc[index + 1, num_elm + 1] += 1
                except:
                    pass

            ls_elm[0] = 0

            ls_elm.insert(0, question_number)

            df.columns = ls_elm

            df = df.drop(0, axis=1)

            return df

    def strip_space(self, ls):
        ls_modified = []
        try:
            for elment in ls:
                elm_modified = elment.strip()
                ls_modified.append(elm_modified)
            return ls_modified
        except:
            pass
    