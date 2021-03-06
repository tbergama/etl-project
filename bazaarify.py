# dependencies

# etl modules
import extract
import transform
import load


if __name__ == '__main__':

	# ----- 1. parse user input -----

	# phrase to search for on each marketplace
	search_term = input("What would you like to search for?......BEAUTIFUL: ")  
	
	# terms that if conained in title, listing should be ignored
	exclusion_terms = input("Are there any terms you would like to exclude (separate by commas)? ").lower().split(',')
	exclusion_terms = [term.strip() for term in exclusion_terms]

	# max number of results from each marketplace
	result_limit = int(input("How many results from each site would you like? "))

	# ----- 2. Extract: scrape from each site -----

	print("Scraping craigslist...")
	craigslist_data = extract.craigslist.scrape(search_term, result_limit)
	print("Done.")
	print("Scraping offerup...")
	offerup_data = extract.offerup.scrape(search_term, result_limit)
	print("Done.")
	print("Scraping ebay...")
	ebay_data = extract.ebay.scrape(search_term, result_limit)
	print("Done.")

	# ----- 3. Transform: clean data from each site and filter -----

	# clean data
	clean_craigslist_data = transform.craigslist.clean(craigslist_data)
	clean_offerup_data = transform.offerup.clean(offerup_data)
	clean_ebay_data = transform.ebay.clean(ebay_data)

	# create a list of all cleaned data
	cleaned_data = []

	# print(clean_craigslist_data)
	# print(clean_offerup_data)
	# print(clean_ebay_data)
	
	cleaned_data.extend(clean_craigslist_data)
	cleaned_data.extend(clean_offerup_data)
	cleaned_data.extend(clean_ebay_data)

	# filter data
	filtered_data = transform.filter.drop_listings(cleaned_data,exclusion_terms)

	# ----- 4. Load: load data into mongo database ------

	mongo_loaded = load.to_mongo(filtered_data)
	print('MongoDB Load Successful!') if mongo_loaded == True else print(f'Load Failed: {mongo_loaded}')