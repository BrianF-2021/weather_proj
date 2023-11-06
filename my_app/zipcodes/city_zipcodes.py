import pandas as pd
from faker import Faker


class Pandas_Query:
    def __init__(self, data=None, import_format=None):
    	self.file_format = import_format
    	self.data_file = None
    	self.random_user_dataset = self.create_random_user_dataset() 
    	self.data = data
    	self.df = None
    	self.columns = []
    	
    	
    def set_import_format(self, file_format):
    	self.file_format = file_format


    def set_df(self, data, file_format):
    	self.set_import_format(file_format)
    	self.data = data
	
    	if self.data:
    		if self.file_format == "json":
    			self.df = pd.read_json(data)
#    			print(self.df[self.df["zip"]==3055])
    			return self.df
    		if self.file_format == "csv":
    			self.df = pd.read_csv(data)
    			return self.df
    		if self.file_format == "excel":
    			self.df = pd.read_excel(data)
    			return self.df
    	self.data = data
    	self.df = pd.DataFrame(self.data)

    	return self.df
    	
    	
    def create_random_user_dataset(self):
    	f = Faker()
    	self.random_user_dataset = {"name":{}, "address":{}, "number":{}, "email":{}}
    	for indx in range(1,6):
    		name = f.unique.name()
    		address = f.address()
    		number = f.phone_number()
    		email = f.email()
    		self.random_user_dataset["name"][indx] = name
    		self.random_user_dataset["address"][indx] = address
    		self.random_user_dataset["number"][indx] =number
    		self.random_user_dataset["email"] = email
 #   	print(self.random_user_dataset)

    	return self.random_user_dataset
    	
    	
    def get_val_in_col(self, col, data, return_key_col=None):
#    	print(self.df.columns)
    	try:
    		full_result = self.df[self.df[col]==data]
    	except Exception as e:
    		print(f"Error in  'get_val_in_col': {e}")
    		return
    	if return_key_col:
    		print(return_key_col)
    		key_result = list(full_result[return_key_col])
    		print(full_result)
    		print(key_result[0])
    		return key_result
    	print(full_result)
    	return full_result

  	

def main():
	csv_path = "/storage/emulated/0/Download/my_data/coding/coding_documents/csv/contacts.csv"

	excel_path = "/storage/emulated/0/Download/my_data/coding/coding_documents/excel/zip_codes.xls"

	json_path = "/storage/emulated/0/Download/my_data/coding/coding_documents/json/zip_codes.json"
	city = "city"
	state = "state"
	zipcode = "zip"
	test = "adjunskdhes"
	city_val = "adjuntas"
	city_val2 = "lexington"
	zip_val = 76109
	
	pd_query = Pandas_Query()
	pd_query.set_df(json_path, "json")
	
	#get zip from city input
#	result = pd_query.get_val_in_col(city,city_val2, zipcode)

#	get city from zip input
	result = pd_query.get_val_in_col(zipcode, zip_val, city)
	print(type(result[1]))



if __name__ == "__main__":
	main()
	


csv_path = "/storage/emulated/0/Download/my_data/coding/coding_documents/csv/contacts.csv"

excel_path = "/storage/emulated/0/Download/my_data/coding/coding_documents/excel/zip_codes.xls"

json_path = "/storage/emulated/0/Download/my_data/coding/coding_documents/json/zip_codes.json"






#df = pd.read_excel(excel_path)
#print(type(excel_file))
#print(df["DELIVERY ZIPCODE"])
#df["PHYSICAL CITY"] = df["PHYSICAL CITY"].str.lower()
#zip_codes = df[["PHYSICAL STATE", "PHYSICAL CITY", "PHYSICAL ZIP"]]
#zip_codes = df[["PHYSICAL STATE", "PHYSICAL CITY", "DELIVERY ZIPCODE"]]
#zip_codes.columns = ["state", "city", "zip"]
#zip_codes = zip_codes.drop_duplicates(subset=["zip"])

#print(zip_codes.columns)


#zip_codes.to_json(json_path, orient="records")

