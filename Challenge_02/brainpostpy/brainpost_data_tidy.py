from urllib.parse import urlparse, parse_qs


def tidy_column_names(content_data_df):
    '''
    Rename the columns
    '''
    new_names = [column_name.lower().replace(' / ','_').replace('. ','_').replace(' ','_').replace('%', 'percent') for column_name in content_data_df.columns]
    return content_data_df.rename(columns = dict(zip(content_data_df.columns, new_names)))

def check_query_keys(page_vals):
    '''
    a list of pages 
    check query keys
    '''
    query_keys = set()
    for page_val in page_vals:
        query_keys, _ = get_query_key_val(page_val)
    print(query_keys)


def get_query_key_val(q):
    '''
    get query keys and values
    '''
    query_key = q[:q.find('=')]
    value = q[q.find('=')+1:]
    return query_key, value


def time_hhmmss_to_sec(hhmmss):
    hh, mm, ss = hhmmss.split(':')
    return int(hh) * 3600 + int(mm) * 60 + int(ss)


def extend_data_with_info_from_page(content_data_df):
    none_list = [None for height in range(content_data_df.shape[0])]
    content_data_df['paths'] = none_list
    content_data_df['from_google'] = none_list
    content_data_df['from_facebook'] = none_list
    content_data_df['platform'] = none_list
    content_data_df['google_keyword'] = none_list
    content_data_df['search_keyword'] = none_list
    content_data_df['sqsscreenshot'] = none_list
    for index, row in content_data_df.iterrows():
        parsed_page = urlparse(row["page"])
        content_data_df.loc[index, 'path'] = parsed_page.path
        if len(parsed_page.query) > 0:
            k, v = get_query_key_val(parsed_page.query)
            if k in ['back']:
                content_data_df.loc[index, 'google_keyword'] = parse_qs(parsed_page.query)['as_q'][0]
                content_data_df.loc[index, 'from_google'] = True
            elif k in ['q']:
                # this is when search was done store the keyword
                if v[:6] not in ['cache:']: 
                    content_data_df.loc[index, 'search_keyword'] = v
            elif k in ['rq']:
                # this is from search results store the keyword
                v = v.strip()
                if v.find(':') == 0:
                    v = v[1:].strip()
                if v[-1] in [',']:
                    v = v[:-1]
                content_data_df.loc[index, 'search_keyword'] = v
                pass
            elif k in ['fbclid']:
                # this is related to facebook not sure what it means
                content_data_df.loc[index, 'from_facebook']= True
                pass
            elif k in ['offset']:
                # this is when pagination is clicked Let's skip this for now
                pass
            elif k in ['platform']:
                # get the platform name
                content_data_df.loc[index, 'platform'] = v
                pass
            elif k in ['depth']:
                # not sure what it means, Let's skip it for now
                pass
            elif k in ['month']:
                # not sure what it means Let's skip it for now
                pass
            elif k in ['donatePageId']:
                # not sure what to do with this info, Let's skip it for now
                pass
            elif k in ['sqsscreenshot']:
                # not sure what to do with this info
                content_data_df.loc[index, 'sqsscreenshot'] = True
                pass
            elif k in ['url']:
                # not sure what to do with this info, Let's skip it for now
                pass

    return content_data_df
