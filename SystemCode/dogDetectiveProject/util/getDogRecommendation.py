import pickle
import pandas as pd
import math
from scipy.spatial.distance import cdist
import json

def getDogRecommendation(request):
	if request.method == 'GET':
		df = pd.read_pickle('./data/data_dog_info.pickle')

		dogBreed = request.args.get('dogBreed')
		housing = request.args.get('housing')
		stayWithFamily = request.args.get('stayWithFamily')
		hasKids = request.args.get('hasKids')
		firstTimeOwner = request.args.get('firstTimeOwner')
		hasOtherDog = request.args.get('hasOtherDog')
		availableTime = request.args.get('availableTime')
		perferDogSize = request.args.get('perferDogSize')
		perferCost = request.args.get('perferCost')

		df = filterCleanDataset(df,dogBreed,housing,stayWithFamily,hasKids,firstTimeOwner,
			hasOtherDog,availableTime,perferDogSize,perferCost)

		resultDf = normalize(df)
		resultDf = resultDf.drop('Training_Dog_Breed', axis=1)
		resultDf = resultDf.drop('Dog_Breed', axis=1)

		similarity_list = cdist(resultDf,resultDf,'euclid')

		for index, distance in enumerate(similarity_list[len(similarity_list)-1]):
			similarityScore = 1 / (1 + distance)
			similarity_list[len(similarity_list)-1][index] = similarityScore

		new_list = list(zip(similarity_list[len(similarity_list)-1],[*range(0, len(similarity_list), 1)]))
		new_list = sorted(new_list, key=lambda x: x[0], reverse=True)

		topResult = 3

		if len(new_list) == 1:
			similar_breeds = []
		elif len(new_list)-1 < 3:
			topResult = len(new_list)-1

		similar_breeds = [score[1] for score in new_list[1:topResult+1]] # Get the top 3 similar breeds
		names = []

		for value in df.iloc[similar_breeds]['Dog_Breed']:
			names.append(value)

	return json.dumps(names)

def filterCleanDataset(df, selectedBreed, housing, stayWithFamily, hasKids, 
					  firstTimeOwner, hasOtherDog, availableTime, perferDogSize, perferCost):
	selectedRow = df.loc[df['Training_Dog_Breed'] == selectedBreed]
	
	 # filter off hard constriant
	if housing != 'Landed':
		df = df[df['apartment_friendly'].isin([5,4,3])]
	
	if stayWithFamily == 'Yes':
		df = df[df['family_friendly'].isin([5,4,3])]
		
	if hasKids == 'Yes':
		df = df[df['kid_friendly'].isin([5,4,3])]
	
	if firstTimeOwner == 'Yes':
		df = df[df['good_for_1st_time_owners'].isin([5,4,3])]
		df = df[df['trainability'].isin([5,4,3,2])]
	
	if hasOtherDog == 'Yes':
		df = df[df['friendly_to_others_dogs'].isin([5,4,3])]
	
	if availableTime == 'low':
		df = df[df['tolerates_being_alone'].isin([5,4])]
		df = df[df['energy'].isin([1,2,3])]
		df = df[df['playfulness'].isin([1,2])]
	elif availableTime == 'medium':
		df = df[df['tolerates_being_alone'].isin([5,4,3,2])]
		df = df[df['energy'].isin([1,2,3,4])]
		df = df[df['playfulness'].isin([1,2,3,4])]
		
	if perferDogSize == 'low':
		df = df[df['Dog_Size'].isin(['Small','Medium'])]
	elif perferDogSize == 'medium':
		df = df[df['Dog_Size'].isin(['Small','Medium','Large'])]
	elif perferDogSize == 'large':
		df = df[df['Dog_Size'].isin(['Medium','Large','Giant'])]
	elif perferDogSize == 'giant':
		df = df[df['Dog_Size'].isin(['Large','Giant'])]
	
	if perferCost == 'low':
		df = df[df['easy_to_groom'].isin([5,4])]
		df = df[df['overall_health'].isin([5,4,3])]
	elif perferCost == 'medium':
		df = df[df['easy_to_groom'].isin([5,4,3])]
		df = df[df['overall_health'].isin([5,4,3,2])]
	
	df = df.drop(df[df.Training_Dog_Breed == selectedBreed].index)
	df = df.append(selectedRow, ignore_index=True)
	
	df = df.drop('Unnamed: 0', axis=1)
	df = df.drop('min_height', axis=1)
	df = df.drop('max_height', axis=1)
	df = df.drop('min_weight', axis=1)
	df = df.drop('max_weight', axis=1)
	df = df.drop('min_lifespan', axis=1)
	df = df.drop('max_lifespan', axis=1)
	df = df.drop('Dog_Size', axis=1)
	df = df.drop('hdb_approved', axis=1)
	df = df.drop('breed_group', axis=1)
	df = df.drop('breed_description', axis=1)
	
	return df

def normalize(df):
	result = df.copy()
	
	for feature_name in df.columns:
		if feature_name not in ['Training_Dog_Breed','Dog_Breed', 'Giant_Dog', 'Large_Dog',
								'Medium_Dog', 'Small_Dog', 
								'group_companion_dog','group_herding_dog','group_hound_dog',
								'group_hybrid_dog','group_sporting_dog',
								'group_working_dog','group_terrier_dog']:
			result[feature_name] = result[feature_name].astype(float)
			max_value = float(df[feature_name].max())
			min_value = float(df[feature_name].min())
			if max_value != min_value:
				result[feature_name] = (df[feature_name].astype('float') - min_value) / (max_value - min_value)  
	return result
