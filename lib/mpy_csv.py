r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     Module of operations concerning csv-files.
"""

import mpy_fct, mpy_common
import sys

from mpy_decorators import metrics, log

@metrics
def csv_read(mpy_trace: dict, app_dict: dict, src_file_path: str, delimiter: str, print_csv_dict: bool) -> dict:

    r"""
    This function reads a csv file and returns a dictionary of
    dictionaries. The header row, first row of data and delimiter
    is determined automatically.

    :param mpy_trace: Operation credentials and tracing
    :param app_dict: morPy global dictionary containing app configurations
    :param src_file_path: Path to the csv file.
    :param delimiter: Delimiters used in the csv. None = Auto detection
    :param print_csv_dict: If true, the csv_dict will be printed to console. Should only
        be used for debugging with small example csv files. May take very long to complete.

    :return: dict
        mpy_trace: Operation credentials and tracing
        check: Indicates whether the function ended without errors
        csv_dict: Dictionary containing all tags. The line numbers of data are
            the keys of the parent dictionary, and the csv header consists of
            the keys of every sub-dictionary.
            Pattern:
                {DATA1 :
                     delimiter : [str]
                     header : [tuple] (header(1), header(2), ...)
                     columns : [int] header columns
                     rows : [int] number of rows in data
                     ROW1 : [dict]
                         {header(1) : data(1, 1),
                          header(2) : data(2, 1),
                          ...}
                     ROW2 : [dict]
                         {header(1) : data(1, 2),
                         header(2) : data(2, 2),
                                 ...}
                 DATA2 :
                     ...
                 }

    :example:
        src_file_path = 'C:\myfile.csv'
        delimiter = '' # Delimiter auto detection
        print_csv_dict = True # Print data tables to console
        csv_dict = mpy_csv.csv_read(mpy_trace, app_dict, src_file_path, delimiter, print_csv_dict=False)
    """

    # Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_csv'
    operation = 'csv_read(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

    check = False
    csv_copy_dict = {}
    csv_dict = {}
    header = ()
    columns = 0
    header_row = -1
    data_row = -1
    data_rows = 0 # Sum of data rows in a data table
    r_data = 0 # Row counter for file processing
    delim_check = False # True, if delimiter identified
    header_cnt_delimiters = -1 # Number of determined columns in header
    data_cnt_delimiters = -1 # Number of determined columns in data
    data_subdict_nr = 0
    data_cnt_row = 0 # Counter for printing the data row sub-dictionary

    try:
        # Started processing CSV-file.
        log(mpy_trace, app_dict, "info",
        lambda: f'{app_dict["loc"]["mpy"]["csv_read_start"]}\n'
                f'{app_dict["loc"]["mpy"]["csv_read_file_path"]}: {src_file_path}')

        # Delimiter auto detection
        delimiters = (delimiter,) if delimiter else ('";"', '","', ';', ',', '"\t"', '\t', '":"', ':')

        src_file_dict = mpy_fct.pathtool(mpy_trace, src_file_path)
        src_file_path = src_file_dict["out_path"]
        src_file_isfile = src_file_dict["is_file"]
        src_file_exists = src_file_dict["file_exists"]
        src_file_ext = src_file_dict["file_ext"]

        if (src_file_isfile and src_file_exists and src_file_ext == ".csv"):
            r_tot = 0 # Total row counter
            # Import the csv file as is
            with open(src_file_path, 'r') as csv_file:
                for line in csv_file:
                    r_tot +=1
                    csv_copy_dict[f'{r_tot}'] = line

            # Track progress
            prog_total = len(delimiters) * r_tot
            csv_read_progress = mpy_common.cl_progress(mpy_trace, app_dict, description='CSV Read Progress', total=prog_total, ticks=10)

            # Determine delimiters, header and data rows
            for d in delimiters:
                r_det = 0 # Row counter for delimiter check
                for row, line in csv_copy_dict.items():
                    r_det +=1
                    csv_read_progress.update(mpy_trace, app_dict, current=r_det)
                    line = line.rstrip()
                    if d in line:
                        # Check, if header needs to be found
                        if header_row < 0:
                            header_row = r_det
                            header = tuple(map(lambda x: x.strip('"\''), line.split(d)))
                            header_cnt_delimiters = len(header)
                            columns = header_cnt_delimiters + 1
                        # If header was assigned, check for data row
                        else:
                            data = tuple(map(lambda x: x.strip('"\''), line.split(d)))
                            data_cnt_delimiters = len(data)
                            data_row = r_det
                            r_data += 1
                            # If header and data got the same amount of columns, data table found.
                            if header_cnt_delimiters == data_cnt_delimiters:
                                # Check, if new data table
                                if data_row == header_row + 1:
                                    delim_check = True
                                    data_subdict_nr += 1
                                    data_table = f'DATA{data_subdict_nr}'
                                    csv_dict[f'{data_table}'] = {}
                                    csv_dict[f'{data_table}']["delimiter"] = d
                                    csv_dict[f'{data_table}']["header"] = header
                                    csv_dict[f'{data_table}']["columns"] = columns
                                    csv_dict[f'{data_table}']["rows"] = data_rows
                                csv_dict[f'{data_table}'][f'{r_data}'] = dict(zip(header, data))
                                data_rows += 1
                                csv_dict[f'{data_table}']["rows"] = data_rows
                            # Set current line as header for next iteration of determination
                            else:
                                header_row = r_det
                                header_cnt_delimiters = data_cnt_delimiters
                                header = tuple(map(lambda x: x.strip(), line.split(d)))
                                columns = header_cnt_delimiters + 1
                                data_rows = 0
                                data_cnt_delimiters = -1
                                r_data = 0
                    else:
                        header_row = -1
                        header_cnt_delimiters = -1
                        data_cnt_delimiters = -1
                        data_rows = 0
                        r_data = 0
                        header = ()
                        data = ()

            # Process CSV into dictionary
            if delim_check:
                # CSV file processed. Dictionary contains ## rows.
                log(mpy_trace, app_dict, "info",
                lambda: f'{app_dict["loc"]["mpy"]["csv_read_done"]}: {data_rows}')

                # Print csv_dict to console for debugging.
                if print_csv_dict:
                    # Start printing returned dictionary to console.
                    log(mpy_trace, app_dict, "info",
                    lambda: f'{app_dict["loc"]["mpy"]["csv_read_done"]}: {data_rows}')

                    for data_table_name in csv_dict.keys():
                        print(f'{0*" "}{data_table_name}: {{')
                        for meta, meta_val in csv_dict[data_table_name].items():
                            # Check, if meta holds data and therefore a dictionary
                            if isinstance(meta_val, dict):
                                data_cnt_row +=1
                                print(f'{3*" "}ROW{data_cnt_row}: {{')
                                for dat_col, dat_row in meta_val.items():
                                    print(f'{6*" "}{dat_col} : {dat_row}')
                                print(f'{3*" "}}}')
                            else:
                                print(f'{3*" "}{meta} : {meta_val}')
                        print(f'{0*" "}}}\n')
                        data_cnt_row = 0

                    # Finished printing returned dictionary to console.
                    log(mpy_trace, app_dict, "info",
                    lambda: f'{app_dict["loc"]["mpy"]["csv_read_done"]}: {data_rows}')

            else:
                # Delimiters could not be determined or data is corrupted. No return dictionary created.
                log(mpy_trace, app_dict, "warning",
                lambda: f'{app_dict["loc"]["mpy"]["csv_read_no_return"]}\n'
                        f'{app_dict["loc"]["mpy"]["csv_read_file_path"]}: {src_file_path}')

        else:
            # File does not exist or is not a CSV file.
            log(mpy_trace, app_dict, "warning",
            lambda: f'{app_dict["loc"]["mpy"]["csv_read_not_done"]}\n'
                    f'{app_dict["loc"]["mpy"]["csv_read_file_exist"]}: {src_file_exists}\n'
                    f'{app_dict["loc"]["mpy"]["csv_read_isfile"]}: {src_file_isfile}\n'
                    f'{app_dict["loc"]["mpy"]["csv_read_file_ext"]}: {src_file_ext}\n'
                    f'{app_dict["loc"]["mpy"]["csv_read_file_path"]}: {src_file_path}')

        check = True

    except Exception as e:
        log(mpy_trace, app_dict, "error",
        lambda: f'{app_dict["loc"]["mpy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{app_dict["loc"]["mpy"]["err_excp"]}: {e}')

    return{
        'mpy_trace' : mpy_trace,
        'check' : check,
        'csv_dict' : csv_dict
        }