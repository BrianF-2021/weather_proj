import json
import pandas as pd




def set_df(file, file_format):
	if file:
		if file_format == "json":
			df = pd.read_json(file)
			return df
		if file_format == "csv":
			df = pd.read_csv(file)
			return df
		if file_format == "excel":
			df = pd.read_excel(file)
			return df
		print("Check file_format. . . Must be excel, json, or csv!")
	return

def get_column_names(dataframe):
    column_names = dataframe.columns.tolist()
#    print("Column Names:")
#    for name in column_names:
#        print(name)
    return column_names

def save_columns_to_json(dataframe, column_names, out_path, out_format="json"):
	if not out_path:
		out_path = "/storage/emulated/0/Download/my_data/coding/coding_documents/json/temp.json"
	new_dataframe = dataframe[column_names]
	print(new_dataframe.head)
	if out_format == "json":
	    new_dataframe.to_json(out_path, orient='records')
		print("SUCCESS!")

def clean_zipcode_data(data_dict):
	result = {}
	
	for i, dict in enumerate(data_dict):
#		print(dict)
		city =dict["PHYSICAL CITY"]
		state = dict["PHYSICAL STATE"]
		zipcode = dict["DELIVERY ZIPCODE"]
		city_state = city+" "+state
		if city_state not in result:
			result[city_state] = []
			result[city_state].append(zipcode)
		if city_state in result and zipcode not in result[city_state]:
			result[city_state].append(zipcode)
		if i%10 == 0:
			print(city_state, result[city_state])
			input("Continue >>>")
	print("DATA CLEANED...")
	for i, key in enumerate(result.keys()):
		pass


	
	
	
def main():
	excel_path = "/storage/emulated/0/Download/my_data/coding/coding_documents/excel/20231002v_zipcodes.xls"
	json_path = "/storage/emulated/0/Download/my_data/coding/coding_documents/json/city_state_zip.json"
	columns = ["PHYSICAL CITY", "PHYSICAL STATE", "DELIVERY ZIPCODE"]
	zips_df = set_df(json_path, "json")
	get_column_names(zips_df)
	zips_dict = zips_df.to_dict(orient="records")
	clean_zipcode_data(zips_dict)
	print(zips_dict[0])

	#save_columns_to_json(zips_df, columns, out_path)
#	print(zips_df.head)
	
if __name__ == "__main__":
	main()