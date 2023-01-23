#from itertools import product
#import itertools
import random
from wammodels.descomp import Descomp
import pandas as pd
import time

class Combination:
	def __init__(self,range_list):
		self.range_list = range_list
		self.list_comb = self.create_combination()
		self.descomp = Descomp()
		self.list_comb_save = []
		self.method_cross = []
		self.time_stop = 0
		self.comb_min = None
		self.comb_mid = None 
		self.comb_max = None

	def create_combination(self):
		combinations = {}
		for key,i in enumerate(self.range_list):
			combinations[key]   =   []
			coef = ""

			if len(i) > 1:
				settings_var    =   i[1]
				lag = 0
				

				if "coef" in settings_var:
					coef = settings_var["coef"][0]

				if "adstock_rate" in settings_var:
					adstock_rate   =  settings_var["adstock_rate"]
					min = int(adstock_rate[0]*100)
					if len(adstock_rate) > 1:
						max = int(adstock_rate[1]*100)
						freq = int(adstock_rate[2]*100)
					else:
						max = min+1
						freq = min
					for range_adstock_rate in range(min,max+1,freq):
						range_adstock_rate = range_adstock_rate/100.0
						if "v" in settings_var:
							v   =   settings_var["v"]
							min_v = int(v[0]*100)
							if len(v) > 1:
								max_v = int(v[1]*100)
								freq_v = int(v[2]*100)
							else:
								max_v = min_v+1
								freq_v = min_v
							for range_v in range(min_v,max_v+1,freq_v):
								range_v = range_v/100.0
								if "rho" in settings_var:
									rho  =  settings_var["rho"]
									min_rho = int(rho[0]*100)
									
									if len(rho) > 1:
										max_rho = int(rho[1]*100)
										freq_rho = int(rho[2]*100)
									else:
										max_rho = min_rho+1
										freq_rho = min_rho
									for range_rho in range(min_rho,max_rho+1,freq_rho):
										range_rho = range_rho/100.0

										if "lag" in settings_var:
											lag = settings_var["lag"]
											min_lag = int(lag[0])
											if len(lag) > 1:
												max_lag = int(lag[1])
												freq_lag = int(lag[2])
											else:
												max_lag = min_lag+1
												freq_lag = min_lag

											for range_lag in range(min_lag,max_lag+1,freq_lag):
												dict_adstrock_rage = dict([("adstock_rate",range_adstock_rate),("v",range_v),("rho",range_rho),("lag",range_lag),("coef",coef)])
												combinations[key].append([i[0],dict_adstrock_rage])
										else:
											dict_adstrock_rage = dict([("adstock_rate",range_adstock_rate),("v",range_v),("rho",range_rho),("lag",lag),("coef",coef)])
											combinations[key].append([i[0],dict_adstrock_rage])
						else:
							if "lag" in settings_var:
								lag = settings_var["lag"]
								min_lag = int(lag[0])
								if len(lag) > 1:
									max_lag = int(lag[1])
									freq_lag = int(lag[2])
								else:
									max_lag = min_lag+1
									freq_lag = min_lag

								for range_lag in range(min_lag,max_lag+1,freq_lag):
									dict_adstrock_rage = dict([("adstock_rate",range_adstock_rate),("lag",range_lag),("coef",coef)])
									combinations[key].append([i[0],dict_adstrock_rage])
							else:
								dict_adstrock_rage = dict([("adstock_rate",range_adstock_rate),("lag",lag),("coef",coef)])
								combinations[key].append([i[0],dict_adstrock_rage])
										
				elif "diff" in settings_var:
					diff  =  settings_var["diff"]
					min_diff = int(diff[0])
					if len(diff) > 1:
						max_diff = int(diff[1])
						freq_diff = int(diff[2])
					else:
						max_diff = min_diff+1
						freq_diff = min_diff
					for range_diff in range(min_diff,max_diff+1,freq_diff):
						dict_diff_rage = dict([("diff",range_diff),("lag",lag),("coef",coef)])
						combinations[key].append([i[0],dict_diff_rage])
				else:
					if "lag" in settings_var:
						lag = settings_var["lag"]
						min_lag = int(lag[0])
						if len(lag) > 1:
							max_lag = int(lag[1])
							freq_lag = int(lag[2])
						else:
							max_lag = min_lag+1
							freq_lag = min_lag

						for range_lag in range(min_lag,max_lag+1,freq_lag):
							dict_lag_rage = dict([("lag",range_lag),("coef",coef)])
							combinations[key].append([i[0],dict_lag_rage])
					else:
						dict_lag_rage = dict([("coef",coef)])
						combinations[key].append([i[0],dict_lag_rage])
			else:
				combinations[key].append([i[0]])
		
		#variable = list(combinations.values())
		#combined_list = list(product(*variable))
		return combinations

	def get_combination_list(self):
		return self.list_comb

	def get_combination_group(self):
		variable = list(self.list_comb.values())
		combined_list = list(product(*variable))
		return combined_list

	def search_combinations(self,max_comb=0,pvalor=0.11,time_stop = 0,method = "default",max_save_unique = 30,show_count_comb=True):
		self.list_comb_save = []
		self.method_cross = []
		start_time = time.time()


		method_other =  [
			"default",
			"cross",
			"min",
			"max",
			"mid",
					]
		if method in method_other:
			if method != "default":
				self.cross_algorithm_random(max_save_unique)
			print(f"Loading method [algorithm_random - {method}]")

		if max_comb != 0:
			while len(self.list_comb_save) < max_comb:
				if time_stop != 0:
					if time.time() - start_time > time_stop:
						print("Timed out search for combinations. (Stop Search Combination)")
						break

				if self.search_method(method,max_comb,time_stop,pvalor,show_count_comb) == False:
					break

				if len(self.list_comb_save) >= max_comb:
					break

		elif time_stop != 0 and max_comb <= 0:
			while time.time() - start_time < time_stop:
				if self.search_method(method,max_comb,time_stop,pvalor,show_count_comb) == False:
					break

		if not show_count_comb:		
			print("Combinations found.")


	def search_method(self,method,max_comb,time_stop,pvalor,show_count_comb):
		list_not_repeat = []

		if method == "default":
			(comb_random,list_index) = self.get_comb_rand()
			while list_index in list_not_repeat:
				(comb_random,list_index) = self.get_comb_rand()
			list_not_repeat.append(list_index)

			self.func_search_combination(comb_random,max_comb,pvalor,show_count_comb)

		elif method == "min":
			(comb_random,list_index) = self.get_comb_rand_min()
			while list_index in list_not_repeat:
				(comb_random,list_index) = self.get_comb_rand_min()
			list_not_repeat.append(list_index)
			self.func_search_combination(comb_random,max_comb,pvalor,show_count_comb)

		elif method == "max":
			(comb_random,list_index) = self.get_comb_rand_max()
			while list_index in list_not_repeat:
				(comb_random,list_index) = self.get_comb_rand_max()
			list_not_repeat.append(list_index)
			self.func_search_combination(comb_random,max_comb,pvalor,show_count_comb)

		elif method == "mid":
			(comb_random,list_index) = self.get_comb_rand_mid()
			while list_index in list_not_repeat:
				(comb_random,list_index) = self.get_comb_rand_mid()
			list_not_repeat.append(list_index)
			self.func_search_combination(comb_random,max_comb,pvalor,show_count_comb)

		elif method == "cross":
			func_list = [self.get_comb_rand_min,self.get_comb_rand_mid,self.get_comb_rand_max,self.get_comb_rand_min_mid,self.get_comb_rand_mid_max,self.get_comb_rand_min_max,self.get_comb_rand]
			start_time = time.time()
			time_change =  60*5 # 7 minutos por combinaciones , default not time value
			if time_stop != 0:
				time_change = time_stop / len(func_list)
			func_index = 0
			while func_index < len(func_list):
				list_not_repeat = []
				while time.time() - start_time < time_change:
					(comb_random,list_index) = func_list[func_index]()
					while list_index in list_not_repeat:
						(comb_random,list_index) = func_list[func_index]()
					list_not_repeat.append(list_index)
					self.func_search_combination(comb_random,max_comb,pvalor,show_count_comb,cross_index=func_index)

					if max_comb != 0:
						if len(self.list_comb_save) >= max_comb:
							break
				start_time = time.time()
				func_index += 1
			return False
		return True

	def change_value_cross(self,value):
		func_list = ["min","mid","max","min-mid","mid-max","min-max","rand"]
		return func_list[value]

	def info_combination_cross(self):
		df = pd.DataFrame(self.method_cross, columns=['algorithm'])
		result = df.groupby('algorithm').size().reset_index(name='results')
		result["algorithm"] = result["algorithm"].apply(self.change_value_cross)
		return result

	def func_search_combination(self,comb_random,max_comb,pvalor,show_count_comb,cross_index = -1):
		(get_var_prepare) = self.descomp.prepare_var(comb_random)
		(df,formula) = self.descomp.create_df_formula(*get_var_prepare)
		(EQ1,X_Model) = self.descomp.create_model(formula,df)
		p_valor =  EQ1.pvalues.lt(pvalor).sum()
		if (len(EQ1.pvalues) == p_valor):
			coef_get   	=  [i[1]["coef"] if len(i) > 1 and "coef" in i[1] else "" for i in get_var_prepare]
			if self.get_check_coef(coef_get,EQ1.params):
				one_v   	=  [i[1]["adstock_rate"] if len(i) > 1 and "adstock_rate" in i[1] else 0 for i in get_var_prepare]
				v_v     	=  [i[1]["v"] if len(i) > 1 and "v" in i[1] else 0 for i in get_var_prepare]
				rho_v   	=  [i[1]["rho"] if len(i) > 1 and "rho" in i[1] else 0 for i in get_var_prepare]
				diff    	=  [i[1]["diff"] if len(i) > 1 and "diff" in i[1] else 0 for i in get_var_prepare]
				lag    		=  [i[1]["lag"] if len(i) > 1 and "lag" in i[1] else 0 for i in get_var_prepare]
								
				self.list_comb_save.append([EQ1,X_Model,[one_v,v_v,rho_v,diff,lag,coef_get]])
				if show_count_comb and max_comb != 0:
					print("Combinations found successfully {} ~ {}".format(len(self.list_comb_save),max_comb))
					if cross_index != -1:
						self.method_cross.append([cross_index])
				else:
					print("Combinations found successfully {}".format(len(self.list_comb_save)))
					if cross_index != -1:
						self.method_cross.append([cross_index])


	def get_check_coef(self,coef_get,coef):
		count_total_coef = 0
		for count,value in enumerate(coef_get):
			if value != "":
				if value == "+" and coef[count] > 0:
					count_total_coef += 1
				elif value == "-" and coef[count] <0:
					count_total_coef +=1
		non_empty_values = [val for val in coef_get if val != '']
		count32 = len(non_empty_values)
		if count32 == count_total_coef:
			return True

		return False
	def get_descomp(self):
		return self.descomp

	def get_size_comb(self):
		return len(self.list_comb_save)

	def get_eq1_comb(self,index):
		if index >= len(self.list_comb_save):
			return "Error max lenght list : {} max".format(len(self.list_comb_save))
		return self.list_comb_save[index][0]

	def get_df_comb(self,index):
		if index >= len(self.list_comb_save):
			return "Error max lenght list : {} max".format(len(self.list_comb_save))
		return self.list_comb_save[index][1]

	def get_var_comb(self,index,format_v="dataframe"):
		if index >= len(self.list_comb_save):
			return "Error max lenght list : {} max".format(len(self.list_comb_save))

		if "dataframe" in format_v:
			df = pd.DataFrame(self.list_comb_save[index][2]).T
			df.columns = ["adstock_rate","v","rho","diff","lag","coef_restric"]
			return df

		return self.list_comb_save[index][2]

	def get_var_cp(self,index):
		if index >= len(self.list_comb_save):
			return "Error max lenght list : {} max".format(len(self.list_comb_save))

		coef_get = self.list_comb_save[index][0].params
		p_value_get = self.list_comb_save[index][0].pvalues

		p_value_formatted = [format(x, '.7f') for x in p_value_get]
		df = pd.DataFrame([coef_get.values,p_value_formatted]).T
		df.columns = ["coef","pvalor"]
		return df

	def get_var_all(self,index):
		if index >= len(self.list_comb_save):
			return "Error max lenght list : {} max".format(len(self.list_comb_save))

		var_df = self.get_var_comb(index)
		df_cp =  self.get_var_cp(index)

		df_final = pd.concat([var_df,df_cp],axis=1)
		return df_final

	def change_format(self,value):
		return format(value,".2f")

	def get_describe_comb(self,describe="all"):
		if self.get_size_comb() <= 0:
			print("you have no combinations.")
			return

		data_get = self.get_var_all(0)
		for a in range(1,self.get_size_comb()):
			data_get = pd.concat([data_get,self.get_var_all(a)],axis=1)
		data_get = data_get.reset_index(drop=True)

		data_get = data_get[["adstock_rate","v","rho","diff","lag"]]

		min_adstock_rate = data_get["adstock_rate"].min()
		min_adstock_rate = data_get["adstock_rate"].max()
		promedio_adstrock_rate = data_get["adstock_rate"].mean()

		min_var  = []
		max_var  = []
		mean_var = []

		for a in data_get.columns.unique():
			min_var.append({f"{a}_min":data_get[a].min(axis=1)})
			max_var.append({f"{a}_max":data_get[a].max(axis=1)})
			mean_var.append({f"{a}_mean":data_get[a].mean(axis=1)})

		df = pd.DataFrame()
		for a in range(0,len(data_get.columns.unique())):
			df = pd.concat([df, pd.DataFrame(min_var[a]) ,pd.DataFrame(max_var[a]) ,pd.DataFrame(mean_var[a])],axis=1)

		min_df =  pd.DataFrame()
		for a in range(0,len(data_get.columns.unique())):
			min_df = pd.concat([min_df,pd.DataFrame(min_var[a])],axis=1)
		min_df

		max_df =  pd.DataFrame()
		for a in range(0,len(data_get.columns.unique())):
			max_df = pd.concat([max_df,pd.DataFrame(max_var[a])],axis=1)
		max_df
		mean_df =  pd.DataFrame()
		for a in range(0,len(data_get.columns.unique())):
			mean_df = pd.concat([mean_df,pd.DataFrame(mean_var[a])],axis=1)
		mean_df["adstock_rate_mean"] = mean_df["adstock_rate_mean"].apply(self.change_format)

		if describe == "all":
			display(min_df)
			display(max_df)
			display(mean_df)
		elif describe == "min":
			return min_df
		elif describe == "max":
			return max_df
		elif describe == "mean":
			return mean_df

	def get_comb_rand(self):
		comb_send = []
		save_comb = []

		for i in range(0,len(self.list_comb)):
			number = random.randint(0, len(self.list_comb[i])-1)
			comb_send.append(self.list_comb[i][number])
			save_comb.append(number)

		return (comb_send,save_comb)

	def get_comb_rand_min(self):
		save_comb = []
		comb_send = []
		for index,i in enumerate(self.comb_min.values()):
			number = random.randint(0, len(i)-1)
			comb_get = self.comb_min[index][number]
			comb_send.append(self.list_comb[index][comb_get])
			save_comb.append(comb_get)
		return (comb_send,save_comb)

	def get_comb_rand_mid(self):
		save_comb = []
		comb_send = []
		for index,i in enumerate(self.comb_mid.values()):
			number = random.randint(0, len(i)-1)
			comb_get = self.comb_mid[index][number]
			comb_send.append(self.list_comb[index][comb_get])
			save_comb.append(comb_get)
		return (comb_send,save_comb)

	def get_comb_rand_max(self):
		save_comb = []
		comb_send = []
		for index,i in enumerate(self.comb_max.values()):
			number = random.randint(0, len(i)-1)
			comb_get = self.comb_max[index][number]
			comb_send.append(self.list_comb[index][comb_get])
			save_comb.append(comb_get)
		return (comb_send,save_comb)

	def get_comb_rand_min_mid(self):
		save_comb = []
		comb_send = []
		for index,i in enumerate(self.comb_min.values()):
			number = random.randint(0, len(i)-1)
			rand_list = [self.comb_min[index][number],self.comb_mid[index][number]]
			number_rand_comb = random.randint(0, len(rand_list)-1)
			comb_get = rand_list[number_rand_comb]
			comb_send.append(self.list_comb[index][comb_get])
			save_comb.append(comb_get)
		return (comb_send,save_comb)

	def get_comb_rand_mid_max(self):
		save_comb = []
		comb_send = []
		for index,i in enumerate(self.comb_mid.values()):
			number = random.randint(0, len(i)-1)
			rand_list = [self.comb_mid[index][number],self.comb_max[index][number]]
			number_rand_comb = random.randint(0, len(rand_list)-1)
			comb_get = rand_list[number_rand_comb]
			comb_send.append(self.list_comb[index][comb_get])
			save_comb.append(comb_get)
		return (comb_send,save_comb)	

	def get_comb_rand_min_max(self):
		save_comb = []
		comb_send = []
		for index,i in enumerate(self.comb_min.values()):
			number = random.randint(0, len(i)-1)
			rand_list = [self.comb_min[index][number],self.comb_max[index][number]]
			number_rand_comb = random.randint(0, len(rand_list)-1)
			comb_get = rand_list[number_rand_comb]
			comb_send.append(self.list_comb[index][comb_get])
			save_comb.append(comb_get)
		return (comb_send,save_comb)	


	def cross_algorithm_random_new(self,max_save_random):
		comb_min = {}
		comb_max = {}
		comb_mid = {}
		for i in range(0,len(self.list_comb)):
			len_list_comb = len(self.list_comb[i])
			comb_min[i] = []
			comb_max[i] = []
			comb_mid[i] = []
			
			min = (len_list_comb//3)
			mid = (len_list_comb//2)
			max = (len_list_comb)-min
			
			list_not_repeat_min = []
			list_not_repeat_max = []
			list_not_repeat_mid = []

			if len_list_comb > 1:
				for number_min in range(0,min):
					comb_min[i].append(number_min)
				for number_max in range(max,len_list_comb):
					comb_max[i].append(number_max)
				for number_mid in range(min, max):
					comb_mid[i].append(number_mid)
			else:
				comb_min[i].append(0)
				comb_max[i].append(0)
				comb_mid[i].append(0)

		self.comb_min =  comb_min
		self.comb_max =  comb_max
		self.comb_mid =  comb_mid

	def cross_algorithm_random(self,max_save_random):
		comb_min = {}
		comb_max = {}
		comb_mid = {}
		for i in range(0,len(self.list_comb)):
			len_list_comb = len(self.list_comb[i])
			comb_min[i] = []
			comb_max[i] = []
			comb_mid[i] = []
			
			min = (len_list_comb//3)
			mid = (len_list_comb//2)
			max = (len_list_comb)-min
			
			list_not_repeat_min = []
			list_not_repeat_max = []
			list_not_repeat_mid = []

			if len_list_comb > 1:
				for a in range(min+max_save_random):
					number_min = random.randint(0, min)
					number_max = random.randint(max, len_list_comb-1)
					number_mid = random.randint(min, max)
							
					if len_list_comb >= 6:
						if len(list_not_repeat_min) < min:
							while number_min in list_not_repeat_min:
								number_min = random.randint(0, min)
							comb_min[i].append(number_min)
							list_not_repeat_min.append(number_min)
						else:
							comb_min[i].append(number_min)
						
						if len(list_not_repeat_max) < (len_list_comb-max):
							while number_max in list_not_repeat_max:
								number_max = random.randint(max, len_list_comb-1)
							comb_max[i].append(number_max)
							list_not_repeat_max.append(number_max)
						else:
							comb_max[i].append(number_max)
						
						if len(list_not_repeat_mid) < (max-min):
							while number_mid in list_not_repeat_mid:
								number_mid = random.randint(min, max)
							comb_mid[i].append(number_mid)
							list_not_repeat_mid.append(number_mid)
						else:
							comb_mid[i].append(number_mid)
						   
					else:
						comb_min[i].append(number_min)
						comb_max[i].append(number_max)
						comb_mid[i].append(number_mid)
			else:
				comb_min[i].append(0)
				comb_max[i].append(0)
				comb_mid[i].append(0)

		self.comb_min =  comb_min
		self.comb_max =  comb_max
		self.comb_mid =  comb_mid
