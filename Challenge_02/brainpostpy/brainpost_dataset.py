import pandas as pd


class DSSBrainPostDataset():
    def __init__(self, challenge_file):
        self.data_file = challenge_file
        self.xls = pd.ExcelFile(self.data_file)
        self.sheet_names = self.xls.sheet_names
        self.non_data_sheets = ['About the Challenge','Signup Page','Page to Page Title lookup']
        
    def ds_info(self):
        print('----------------------------------------------')
        print('DSS BrainPost Web Analytics Challenge Dataset')
        print('----------------------------------------------')
        print(f'Data File:{self.data_file}')
        print(f'Sheet Count:{len(self.sheet_names)}')
        print('Functions:')
        print('\t - get_sheet_names() :  Get Sheet Names.')
        print('\t - get_data() : Returns (content_data, page_view_data), content data and page view dataframe as tuple.')
        
    
    def get_sheet_names(self):
        print(f'Sheets:')
        for sheet_name in self.sheet_names:
            tag = '[INFO]' if sheet_name in self.non_data_sheets else '[DATA]'
            print(f'\t - {tag} {sheet_name}')
            
    def get_data(self):
        full_data_df = pd.DataFrame()
        full_page_view_df = pd.DataFrame()
        data_sheets = [sheet_name for sheet_name in self.sheet_names if sheet_name not in self.non_data_sheets]
        for sheet_name in data_sheets:
            content_data_df = self.xls.parse(sheet_name, skiprows=6, skipfooter=20)
            full_data_df = full_data_df.append(content_data_df, ignore_index=True)
            page_view_df = self.xls.parse(sheet_name, skiprows=content_data_df.shape[0]+1 + 9)
            full_page_view_df = full_page_view_df.append(page_view_df.iloc[-2:,1:3], ignore_index=True)
        return full_data_df, full_page_view_df
