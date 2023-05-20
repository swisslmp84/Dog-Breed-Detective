import pickle
import pandas as pd

def getDogInfo(request):
	if request.method == 'GET':
		df = pd.read_pickle('./data/data_dog_info.pickle')

		dogBreed = request.args.get('dogBreed')
		nameType = request.args.get('nameType')
		df = df[df[nameType] == dogBreed]
		

		dfnew = pd.DataFrame()
		dfnew['breed_group'] = df['breed_group']
		dfnew['apartment_friendly'] = df['apartment_friendly']
		dfnew['avg_height'] = df['avg_height'].astype('string') + " inchs"
		dfnew['avg_weight'] = df['avg_weight'].astype('string') + " pounds"
		dfnew['avg_lifespan'] = df['avg_lifespan'].astype('string') + " years"
		dfnew['overall_health'] = df['overall_health']
		dfnew['easy_to_groom'] = df['easy_to_groom']
		dfnew['Dog_Size'] = df['Dog_Size']
		dfnew['family_friendly'] = df['family_friendly']
		dfnew['kid_friendly'] = df['kid_friendly']
		dfnew['friendly_to_others_dogs'] = df['friendly_to_others_dogs']
		dfnew['good_for_1st_time_owners'] = df['good_for_1st_time_owners']
		dfnew['intelligence'] = df['intelligence']
		dfnew['playfulness'] = df['playfulness']
		dfnew['breed_description'] = df['breed_description']

	return dfnew.to_json(orient='records', lines=True)

